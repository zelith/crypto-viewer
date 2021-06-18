from binance.client import Client


class BinanceModel:
    def __init__(self, key: str, secret: str):
        self._client = Client(key, secret)
        self._accountSnapshot = self.getAccountSnapshot()
        self._allOrders = self._getAllOrders()

    def getAccountSnapshot(self) -> dict:
        res = self._client.get_account_snapshot(type='SPOT')
        if res.get('code') != 200:
            print('Failed to query account snapshot')
            return None
        return res

    def getCoinsBalance(self) -> list:
        """ return list of coins mapped to current quantity

        """
        # default 5 snapshot returned, select first
        snapshot = self._accountSnapshot.get('snapshotVos')[0]
        snapshotData = snapshot.get('data')

        coinBalanceList = list()
        for coinBalance in snapshotData.get('balances'):
            cb = dict(name=coinBalance.get('asset'),
                      quantity=float(coinBalance.get('free')) + float(coinBalance.get('locked'))
                      )
            coinBalanceList.append(cb)

        return coinBalanceList

    def getCoinsList(self) -> list:
        """ return list of coins with quantity greater than zero

        """
        return [coin.get('name') for coin in self.getCoinsBalance() if coin.get('quantity') > 0]

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



if __name__ == '__main__':
    model = BinanceModel(key='insert key here',
                 secret='insert secret here')

    print(model.getCoinsBalance())
    print(model.getCoinsList())
    for coin in model._allOrders.keys():
        print(model.getOrdersFor(coin))
