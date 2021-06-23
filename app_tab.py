import functools

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidgetItem
import sys

from binanceModel import BinanceModel
from tabView import Ui_MainWindow
from functools import partial

class AppController:
    def __init__(self, model: BinanceModel, view: QMainWindow):
        self._view = view
        self._model = model

        for coin in self._model.getCoinsList():
            if coin == 'USDT':
                continue
            self.createNewTabForCoin(coin)

    def createNewTabForCoin(self, coin: str = 'USDT'):
        tab_new = QtWidgets.QWidget()
        tab_new.setObjectName("tab_" + coin)

        table_new = QtWidgets.QTableWidget(tab_new)
        table_new.setGeometry(QtCore.QRect(10, 70, 761, 431))
        table_new.setObjectName("table_" + coin)
        # fill table
        trades = self._model.getTradesFor(coin)
        col_count = len(trades[0].keys())
        table_new.setColumnCount(col_count)

        for col_idx, key in enumerate(trades[0].keys()):
            table_new.setHorizontalHeaderItem(col_idx, QTableWidgetItem(key))
        for row_idx, trades in enumerate(self._model.getTradesFor(coin)):
            table_new.insertRow(row_idx)
            for col_idx, param in enumerate(trades.keys()):
                table_new.setItem(row_idx, col_idx, QTableWidgetItem(str(trades.get(param))))

        trades = self._model.getTradesFor(coin)
        total_buy_price = sum(
            [float(trade.get('qty')) * float(trade.get('price')) for trade in trades if trade.get('isBuy')])
        total_sell_price = sum(
            [float(trade.get('qty')) * float(trade.get('price')) for trade in trades if not trade.get('isBuy')])
        current_profit = total_sell_price - total_buy_price
        current_balance = model.getCoinsBalance().get(coin)
        current_price = model.getCurrentCoinPrice(coin)
        estimated_running_profit = current_profit + (current_price * current_balance)

        label_balance = QtWidgets.QLabel(tab_new)
        label_balance.setGeometry(QtCore.QRect(10, 10, 200, 21))
        label_balance.setObjectName("current_balance")

        label_current_price = QtWidgets.QLabel(tab_new)
        label_current_price.setGeometry(QtCore.QRect(250, 10, 200, 21))
        label_current_price.setObjectName("current_price")

        label_total_buy_price = QtWidgets.QLabel(tab_new)
        label_total_buy_price.setGeometry(QtCore.QRect(10, 30, 200, 21))
        label_total_buy_price.setObjectName("total_buy_price")

        label_total_sell_price = QtWidgets.QLabel(tab_new)
        label_total_sell_price.setGeometry(QtCore.QRect(250, 30, 200, 21))
        label_total_sell_price.setObjectName("total_sell_price")

        label_current_profit = QtWidgets.QLabel(tab_new)
        label_current_profit.setGeometry(QtCore.QRect(500, 10, 200, 21))
        label_current_profit.setObjectName("current_profit")

        label_estimated_running_profit = QtWidgets.QLabel(tab_new)
        label_estimated_running_profit.setGeometry(QtCore.QRect(500, 30, 200, 21))
        label_estimated_running_profit.setObjectName("estimated_running_profit")

        self._view.tabWidget.addTab(tab_new, "")

        _translate = QtCore.QCoreApplication.translate
        label_balance.setText(_translate("MainWindow", "current_balance: " + str(current_balance)))
        label_current_price.setText(_translate("MainWindow", "current_price: " + str(current_price)))
        label_total_buy_price.setText(_translate("MainWindow", "total_buy_price: " + str(total_buy_price)))
        label_total_sell_price.setText(_translate("MainWindow", "total_sell_price: " + str(total_sell_price)))
        label_current_profit.setText(_translate("MainWindow", "current_profit: " + str(current_profit)))
        label_estimated_running_profit.setText(_translate("MainWindow", "estimated_running_profit: " + str(estimated_running_profit)))
        self._view.tabWidget.setTabText(self._view.tabWidget.indexOf(tab_new), _translate("MainWindow", coin))




if __name__ == "__main__":
    try:
        f = open('apiCredentials.txt', 'r')
        key = f.readline().strip()
        secret = f.readline().strip()
    except:
        key = input("Enter api key: ").strip()
        secret = input("Enter api secret: ").strip()
        f = open('apiCredentials.txt', 'w')
        f.writelines((key +'\n'+ secret))

    # Create the application object
    app = QtWidgets.QApplication(sys.argv)

    # Create the form object
    main_window = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    # Show form
    main_window.show()
    model = BinanceModel(key=key,
                         secret=secret)
    AppController(model=model, view=ui)

    # Run the program
    sys.exit(app.exec())
