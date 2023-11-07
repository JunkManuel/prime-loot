from data.getData import cookies2client,graphql2payload, pull_data
from pprint import pformat
import logging
import asyncio


log = logging.getLogger('pull')
fh = logging.FileHandler('app/data/pull.log',mode='w')

log.setLevel(logging.INFO)
log.addHandler(fh)

async def pull_orders_info(**fdata):
    # Declare defaults
    try:
        cookies2client_task = asyncio.create_task(cookies2client('app/cookies.txt'))
        graphql2payload_task = asyncio.create_task(graphql2payload('app/data/graphql/claimed_items_info.graphql',variables={
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
    
    if 'key' not in fdata: fdata |= {
        'key': None
    }

    client,headers = await cookies2client_task
    payload = await graphql2payload_task
    pull_data_task = asyncio.create_task(pull_data(client,headers,payload))

    try:
        data = await pull_data_task
        items = data['data']['inGameLoot']['items']
        items = sorted(items,key=lambda i: bool(i['offers'][0]['offerInfo']['orderInformation']))
        if fdata['key']: 
            items = (item for item in items if fdata['key'] in item['game']['gameAssets']['title'])
            log.info(f"Keyword = {fdata['key']}")
        
        for item in items:
            if item['offers'][0]['offerInfo']['eligibility']['isClaimed']:
                gameAssets = item['game']['gameAssets']
                itemAssets = item['itemAssets']
                orderInformation = item['offers'][0]['offerInfo']['orderInformation']

                log.info(f"* {gameAssets['title']} *")
                log.info(f"``` {itemAssets['title']} ```")
                
                if orderInformation is not None:
                    orderInformation = orderInformation[0]
                    if orderInformation['claimCode'] is not None:
                        orderInformation['claimCode'] = orderInformation['claimCode'].replace('-','\\-')
                        log.info(f"||[{orderInformation['claimCode']}]({itemAssets['externalClaimLink']})||")

                # log.info(f"isClaimed -> {item['offers'][0]['offerInfo']['eligibility']['isClaimed']}")
            log.info('')

    except KeyError as err:
        log.error('Data does not contain expected information')
        if 'error' in data: log.error(data['error'])
        logging.exception(pformat(data))
        fh.close()
        return
    
    fh.close()



if __name__ == '__main__':
    def run_async_pullInfoClaimed():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(pull_orders_info())

    run_async_pullInfoClaimed()