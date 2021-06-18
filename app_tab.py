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
        order = self._model.getOrdersFor(coin)
        col_count = len(order[0].keys())
        table_new.setColumnCount(col_count)

        for col_idx, key in enumerate(order[0].keys()):
            table_new.setHorizontalHeaderItem(col_idx, QTableWidgetItem(key))
        for row_idx, order in enumerate(self._model.getOrdersFor(coin)):
            table_new.insertRow(row_idx)
            for col_idx, param in enumerate(order.keys()):
                table_new.setItem(row_idx, col_idx, QTableWidgetItem(str(order.get(param))))

        # label_new = QtWidgets.QLabel(self.tab_overview)
        # label_new.setGeometry(QtCore.QRect(10, 30, 91, 21))
        # label_new.setObjectName("label")
        self._view.tabWidget.addTab(tab_new, "")

        _translate = QtCore.QCoreApplication.translate
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
