from data.getData import cookies2client,graphql2payload, pull_data
import logging


log = logging.getLogger('pull')
fh = logging.FileHandler('app/data/pull.log',mode='w')

log.setLevel(logging.INFO)
log.addHandler(fh)

async def pull_orders_info(fdata: dict = None):
    if fdata is None: fdata = {}
    
    try:
        client,headers = await cookies2client('app/cookies.txt')
        payload = graphql2payload('app/data/graphql/claimed_items_info.graphql',variables={
            'pageSize': 9999
        })
        data = await pull_data(client,headers,payload)
    except FileNotFoundError as err:
        log.error('Breaking exception: Cannot Continue')
        fh.close()
        return
    except Exception as ex:
        log.error('Unknown exception')
        logging.exception(ex)
        fh.close()
        return

    try:
        items = data['data']['inGameLoot']['items']
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
        log.error(data)
        fh.close()
        return
    
    fh.close()



if __name__ == '__main__':
    import asyncio
    def run_async_pullInfoClaimed():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(pull_orders_info())
        
    run_async_pullInfoClaimed()