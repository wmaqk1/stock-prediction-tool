import xapi
import time

# function to buy stock 
async def Buy_Stock(login_data, stock, quantity):
    try:
        async with await xapi.connect(**login_data) as login:
            response = await login.socket.tradeTransaction(
                symbol = stock,
                cmd = xapi.TradeCmd.BUY,
                type = xapi.TradeType.OPEN,
                price = 1,
                volume = quantity
            )
            if response['status'] == True:
                return True
    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return False
    except xapi.ConnectionClosed as c:
        print(f"Connection closed: {c}")
        return False


# function to sell stock if it exists
async def Sell_Stock(login_data, stock, quantity):
    try:
        async with await xapi.connect(**login_data) as login:
            response = await login.socket.tradeTransaction(
                symbol = stock,
                cmd = xapi.TradeCmd.SELL,
                type = xapi.TradeType.OPEN,
                price = 1,
                volume = quantity
            )
        if response['status']:
            return True
    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return False
    except xapi.ConnectionClosed as c:
        print(f"Connection closed: {c}")
        return False

# function to return informations about certain stock and None if not existing
async def Stock_Enquiry(login_data, stock):
    try:
        async with await xapi.connect(**login_data) as login:
            portfolio_data = await login.socket.getTrades()

            for element in portfolio_data['returnData']:
                if element['symbol'] == stock:
                    return element
        
    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return None
    except xapi.ConnectionClosed as c:
        print(f"Connection closed: {c}")
        return None

# function allowing to clear portfolio
async def Clear_Portfolio(login_data):
    try:
        async with await xapi.connect(**login_data) as login:
            portfolio_data = await login.socket.getTrades()
            
            for element in portfolio_data['returnData']:
                if await Sell_Stock(login_data, element['symbol'], element['volume']) == False:
                    print(f"Selling {element['symbol']} stock failed")

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return None
    except xapi.ConnectionClosed as c:
        print(f"Connection closed: {c}")
        return None

# Function to get information about current credit
async def Credit(login_data):
    try:
        async with await xapi.connect(**login_data) as login:
            await login.stream.getBalance()
            
            async for message in login.stream.listen():
                credit = message['data']['marginFree']
                await login.stream.stopBalance()
                return credit

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return False
    except xapi.ConnectionClosed as c:
        print(f"Connection closed: {c}")
        return False

# Minimum purchase amount
async def Minimum_purchase(login_data, stock_name):
    try:
        async with await xapi.connect(**login_data) as login:
            stock = await login.socket.getTickPrices(stock_name, int(time.time()))

        if stock['status']:
            return stock['returnData']['quotations'][0]['ask']

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")
        return None
    except xapi.ConnectionClosed as c:
        print(f"Connection closed: {c}")
        return None