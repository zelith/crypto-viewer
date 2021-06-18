from binance.client import Client


class BinanceHelper:
    def __init__(self, key, secret):
        self._apiKey = key
        self._api_secret = secret
        self._client = Client(self._apiKey, self._api_secret)

        self._accountSnapshot = self._client.get_account_snapshot(type='SPOT')
        self._assetDetails = self._client.get_asset_details()
        self._tickers = self._client.get_all_tickers()

    def getFilledOrders(self, targetCoin, stableCoin='USDT'):
        symbol = targetCoin + stableCoin
        return [dict(orderId=order['orderId'],
                     quantity=float(order['executedQty']),
                     price=float(order['price']),
                     side=order['side'])
                for order in self._client.get_all_orders(symbol=symbol) if order['status'] == 'FILLED']

    def getCurrentCoins(self):
        pass

    def getCurrentCoinPrice(self, coin, stableCoin = 'USDT'):
        priceList = self._tickers
        symbol = coin + stableCoin
        for coinPrice in priceList:
            if coinPrice['symbol'] == symbol:
                return float(coinPrice['price'])
        return None

    def getSpotBalance(self):
        return [(x['asset'], float(x['free']) + float(x['locked'])) for x in
                self._accountSnapshot['snapshotVos'][-1]['data']['balances'] if
                (x['free'] != '0' or x['locked'] != '0')]

    def getCoinsList(self):
        return [coin['asset'] for coin in
                self._accountSnapshot['snapshotVos'][-1]['data']['balances'] if
                (coin['free'] != '0' or coin['locked'] != '0')]

    def getTotalCoinsPrice(self, coin):
        orders = self.getFilledOrders(coin)
        totalPrice = 0
        for order in orders:
            totalPrice += order['quantity'] * order['price'] * (-1 if order['side'] == 'SELL' else 1)
        return totalPrice

    def getAverageBuyingPrice(self, coin):
        orders = self.getFilledOrders(coin)
        totalCoins = 0
        totalCoinsPrice = 0
        for order in orders:
            if order['side'] == 'BUY':
                totalCoinsPrice += order['quantity'] * order['price']
                totalCoins += order['quantity']

        return totalCoinsPrice / totalCoins



    def getTotalCoinsQty(self, coin):
        balance = self.getSpotBalance()
        for c, qty in balance:
            if coin == c:
                return qty
        return 0


if __name__ == '__main__':
    helper = BinanceHelper()
    print(helper.getSpotBalance())

    for coin in helper.getCoinsList():
        if coin == 'USDT':
            continue
        currentPrice = helper.getCurrentCoinPrice(coin)
        totalCoinsPrice = helper.getTotalCoinsPrice(coin)
        totalCoinsQty = helper.getTotalCoinsQty(coin)
        currentProfit = (currentPrice * totalCoinsQty) - totalCoinsPrice
        avgBuyPrice = helper.getAverageBuyingPrice(coin)
        print('coin: {coin} | currentPrice: {currentPrice} | ave buying price: {avgBuyPrice} '.format(coin=coin, currentPrice=currentPrice, avgBuyPrice=avgBuyPrice))

