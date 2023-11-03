from data.getData import cookies2client,graphql2payload

async def pull_orders_info():
    client,headers = cookies2client('app/cookies.txt')