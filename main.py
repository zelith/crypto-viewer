from binanceHelper import BinanceHelper
import time


if __name__ == '__main__':
    try:
        f = open('apiCredentials.txt', 'r')
        key = f.readline().strip()
        secret = f.readline().strip()
    except:
        key = input("Enter api key: ").strip()
        secret = input("Enter api secret: ").strip()
        f = open('apiCredentials.txt', 'w')
        f.writelines((key +'\n'+ secret))

    helper = BinanceHelper(key, secret)
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
        time.sleep(1)

