from binance.client import Client
import time

class BinanceModel:
    def __init__(self, key: str, secret: str):
        self._client = Client(key, secret)
        self._accountSnapshot = self.getAccountSnapshot()
        self._allOrders = self._getAllOrders()
        self._allTrades = self._getAllTrades()
        self._tickers = self._client.get_all_tickers()

    def getAccountSnapshot(self) -> dict:
        res = self._client.get_account_snapshot(type='SPOT')
        if res.get('code') != 200:
            print('Failed to query account snapshot')
            return None
        return res

    def getCoinsBalance(self) -> dict:
        """ return list of coins mapped to current quantity

        """
        # default 5 snapshot returned, select first
        snapshot = self._accountSnapshot.get('snapshotVos')[::-1][0]
        snapshotData = snapshot.get('data')

        coinBalanceMap = dict()
        for coinBalance in snapshotData.get('balances'):
            coinBalanceMap[coinBalance.get('asset')] = float(coinBalance.get('free')) + float(coinBalance.get('locked'))

        return coinBalanceMap

    def getCoinsList(self) -> list:
        """ return list of coins with quantity greater than zero

        """
        return [coin for coin, qty in self.getCoinsBalance().items() if qty > 0]

    def _getAllOrders(self):
        """ return all filled orders grouped by coin

        """
        coinOrders = dict()
        for coin in self.getCoinsList():
            if coin == 'USDT':
                continue
            coinOrders[coin] = self._getOrdersFor(coin)

        return coinOrders

    def getAllOrders(self):
        """ return all filled orders grouped by coin

        """

        return self._allOrders

    def _getOrdersFor(self, targetCoin: str, stableCoin: str='USDT'):
        symbol = targetCoin + stableCoin
        return [dict(orderId=order['orderId'],
                     quantity=float(order['executedQty']),
                     price=float(order['price']),
                     isBuy=order['side'] == 'BUY')
                for order in self._client.get_all_orders(symbol=symbol) if order['status'] == 'FILLED']

    def getOrdersFor(self, targetCoin: str):
        return self._allOrders.get(targetCoin)

    def _getTradesFor(self, targetCoin: str, stableCoin: str='USDT'):
        symbol = targetCoin + stableCoin
        return [dict(time=time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(int(trade['time'])/1000)),
                     qty=trade['qty'],
                     quoteQty=trade['quoteQty'],
                     price=trade['price'],
                     fees=trade['commission'],
                     feesAsset=trade['commissionAsset'],
                     isBuy=trade['isBuyer'])
                for trade in self._client.get_my_trades(symbol=symbol)]

    def getTradesFor(self, targetCoin: str):
        return self._allTrades.get(targetCoin)

    def _getAllTrades(self):
        """ return all trades grouped by coin

        """
        coinTrades = dict()
        for coin in self.getCoinsList():
            if coin == 'USDT':
                continue
            coinTrades[coin] = self._getTradesFor(coin)

        return coinTrades

    def getAllTrades(self):
        """ return all trades grouped by coin

        """

        return self._allTrades

    def getCurrentCoinPrice(self, coin, stableCoin = 'USDT'):
        priceList = self._tickers
        symbol = coin + stableCoin
        for coinPrice in priceList:
            if coinPrice['symbol'] == symbol:
                return float(coinPrice['price'])
        return None



if __name__ == '__main__':
    model = BinanceModel(key='DH1NjBKc1Nw3fy9dXM0ZHbAwHVZCAtkha6TW2G8zEECK7qfUarLpt0KGm2gdUlQf',
                 secret='FmH3JPxOS4LUffl1wGLG4pEYngkyoNDBXgKF3T9yTqnjQxOBbXVSvVEqhgJEiIes')

    print(model.getAccountSnapshot())
    print(model.getCoinsBalance())
    print(model.getCoinsList())
    # for coin in model._allOrders.keys():
    #     print(model.getOrdersFor(coin))
    for coin in model.getCoinsList():
        if coin == 'USDT':
            continue
        print(model._getTradesFor(coin))
