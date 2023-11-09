from data.getData import cookies2client, graphql2payload, pull_data
import asyncio
import aiofiles
import logging
from pprint import pformat
import sys

log = logging.getLogger('loot_fgwp.py')
fh = logging.FileHandler('app/data/loot_fgwp.log',mode='w')
sh = logging.StreamHandler(sys.stdout)

log.setLevel(logging.INFO)
log.addHandler(fh)
log.addHandler(sh)

async def claim(offer_id,item):
    cookies2client_task = asyncio.create_task(cookies2client('app/cookies.txt'))
    payload_task = asyncio.create_task(
        graphql2payload('app/data/graphql/claim_fgwp.graphql'
            ,variables={
                "input":{
                    "offerIds": [offer_id],
                    "attributionChannel": '{"eventId":"ItemDetailRootPage:' + offer_id + '","page":"ItemDetailPage"}',
                }
            }))

    client,header = await cookies2client_task
    payload = await payload_task
    try :
        data_pull_task = asyncio.create_task(pull_data(client,header,payload))
    except Exception as ex: logging.exception


    data = await data_pull_task
    if 'error' not in data:
        log.info(f"Claimed *{item['game']['assets']['title']}*")
        if 'gog' in item['assets']['claimInstructions'].lower():
            log.info(f"GOG\| [claimLink]({item['assets']['externalClaimLink']})")
    else:
        log.error('Mutation on PrimeGaming Database returned error')
        log.error('Returned payload: ')
        for i in pformat(data).split('\n'): log.error(i)
    

async def main(cookies_file: 'file'):
    try:
        cookies2client_task = asyncio.create_task(cookies2client(cookies_file))
        graphql2payload_task = asyncio.create_task(graphql2payload('app/data/graphql/offers_fgwp.graphql',variables={
                'pageSize': 9999
            }))
    except FileNotFoundError as err:
        log.error(err.strerror)
        log.error('Breaking exception: Cannot Continue')
        fh.close()
        return
    except Exception as ex:
        log.error('Unknown exception')
        logging.exception(ex)
        fh.close()
        return
    
    cliente, headers = await cookies2client_task
    payload = await graphql2payload_task
    pull_data_task = asyncio.create_task(pull_data(cliente,headers,payload))

    try:
        offers_id = []
        data = await pull_data_task
        for item in data['data']['Games']['items']:
            for offer in item['offers']:
                if offer['offerSelfConnection']['eligibility']['isClaimed'] :
                    log.info(f"*{item['game']['assets']['title']}* is already Claimed")
                else: offers_id.append(offer['id'])

        await asyncio.gather(
            *[claim(offer_id,item) for offer_id,item in zip(offers_id,data['data']['Games']['items'])]
        )

    except Exception as ex:
        log.error('Unknown exception')
        logging.exception(ex)
        fh.close()
        return
    
    fh.close()

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('app/cookies.txt'))