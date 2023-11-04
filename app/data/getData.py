import httpx
import json
import asyncio
import re
import logging
import http.cookiejar as cookiejar

def graphql2payload(file,variables = {},extensions = {}):
    with open(file,'r') as f: query = f.readlines()
    op_name = query[0].split(' ')[1].split('(')[0]
    query = "".join(query)

    payload = {
        "operationName": op_name,
        "variables": variables,
        "extensions": extensions,
        "query": query,
    }
    return payload

async def cookies2client(cookie_file):
    jar = cookiejar.MozillaCookieJar(cookie_file)
    jar.load()
    client = httpx.AsyncClient()
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
    
    return client,json_headers

async def pull_data(client,headers,payload):
    gql_url = "https://gaming.amazon.com/graphql"
    response = await client.post(gql_url, headers=headers, data=json.dumps(payload))
    await  client.aclose()
    return response.json()


if __name__ == '__main__':
    async def main():
        from pprint import pp
        import logging
        import traceback

        logging.basicConfig(
            # format="%(asctime)s [%(levelname)s] %(msg)s",
            format="({name}) {asctime} [{levelname}] {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        log = logging.getLogger('test')
        log.setLevel(logging.INFO)

        try: cliente,headers = await cookies2client('app/cookie.txt')
        except FileNotFoundError as ex:
            log.exception(ex)
            return

        p = graphql2payload('app/data/graphql/claimed_items_info.graphql')

        # data = await pull_data(cliente,headers,p)

        # data = data['data']['inGameLoot']['items']
        # pp(data,indent=2,compact=True)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())