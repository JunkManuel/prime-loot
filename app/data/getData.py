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

async def pull_data(client,url,headers,payload):
    response = await client.post(url, headers=headers, data=json.dumps(payload))
    client.aclose()
    return response.json()


async def main():
    from pprint import pp

    gql_url = "https://gaming.amazon.com/graphql"
    p = graphql2payload('app/data/graphql/offers.graphql')
    
    cliente,headers = await cookies2client('app/cookies.txt')
    data = await pull_data(cliente,gql_url,headers,p)

    pp(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())