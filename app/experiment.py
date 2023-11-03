import httpx
import json
import asyncio
import re
import logging
import http.cookiejar as cookiejar

gql_url = "https://gaming.amazon.com/graphql"

logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger()

with open('./data/graphql_operations/offers.graphql','r') as f: query = f.readlines()
query_offers = "".join(query)

offers_payload = {
    "operationName": "OffersContext_Offers_And_Items",
    "variables": {"pageSize": 999},
    "extensions": {},
    "query": query_offers,
}


async def claim_offer(offer_id: str, item: dict, client: httpx.AsyncClient, headers: dict) -> True:
    if not item["offers"][0]["offerSelfConnection"]["eligibility"]["isClaimed"]:
        if (
            item["offers"][0]["offerSelfConnection"]["eligibility"]["canClaim"] is False
            and item["offers"][0]["offerSelfConnection"]["eligibility"]["missingRequiredAccountLink"] is True
        ):
            log.error(f"Cannot collect game `{item['game']['assets']['title']}`, account link required.")
            return
        log.info(f"Collecting offer for {item['game']['assets']['title']}")
        
        with open('./data/graphql_operations/claim.graphql','r') as f: query = f.readlines()
        query_claim = "".join(query)
        
        claim_payload = {
            "operationName": "placeOrdersDetailPage",
            "variables": {
                "input": {
                    "offerIds": [offer_id],
                    "attributionChannel": '{"eventId":"ItemDetailRootPage:' + offer_id + '","page":"ItemDetailPage"}',
                }
            },
            "extensions": {},
            "query": query_claim
        }

        response = await client.post(gql_url, headers=headers, data=json.dumps(claim_payload))
        data = response.json()["data"]

        if item["grantsCode"]: log.info(f"\nGranted code {data['placeOrders']['orderInformation']['claimCode']}")

        if data["placeOrders"]["error"] is not None:
            log.error(f"Error: {data['placeOrders']['error']}")
    # else: log.info(f"{item['offers'][0]['offerSelfConnection']['claimInstructions']}") debugin data


async def primelooter(cookie_file):
    jar = cookiejar.MozillaCookieJar(cookie_file)
    jar.load()
    async with httpx.AsyncClient() as client:
        base_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        }

        json_headers = base_headers | {
            "Content-Type": "application/json",
        }
        for _c in jar:
            client.cookies.jar.set_cookie(_c)

        html_body = (await client.get("https://gaming.amazon.com/home", headers=base_headers)).text
        matches = re.findall(r"name='csrf-key' value='(.*)'", html_body)
        json_headers["csrf-token"] = matches[0]

        response = await client.post(gql_url, headers=json_headers, data=json.dumps(offers_payload))
        data = response.json()["data"]["inGameLoot"]["items"]

        # although insanely low, python WILL garbage collect running coroutines if their references
        # aren't stored somewhere, therefore we noqa the Flake8 issue yelling at us about it.
        coros = await asyncio.gather(  # noqa: F841
            *[claim_offer(item["offers"][0]["id"], item, client, json_headers) for item in data]
        )
