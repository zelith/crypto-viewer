import functools

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidgetItem
import sys

from binanceHelper import BinanceHelper
from untitled import Ui_MainWindow
from functools import partial

class AppController:
    def __init__(self, model, view: QMainWindow):
        self._view = view
        self._model = model

        self.initialize_view()
        self.connect_signals()

    def initialize_view(self):
        self._view.comboBox_targetCoin.addItems(self._model.getCoinsList())

    def display_info(self, coin):
        print('selected ' + coin)
        price = self._model.getCurrentCoinPrice(coin)
        self._view.label.setText("price:" + str(price))

    def display_table(self, coin):
        self._view.tableWidget.setRowCount(0)
        for i, order in enumerate(self._model.getFilledOrders(coin)):
            self._view.tableWidget.insertRow(i)
            self._view.tableWidget.setItem(i, 0, QTableWidgetItem(order['side']))
            self._view.tableWidget.setItem(i, 1, QTableWidgetItem(str(order['price'])))
            self._view.tableWidget.setItem(i, 2, QTableWidgetItem(str(order['quantity'])))

    def connect_signals(self):
        self._view.comboBox_targetCoin.currentIndexChanged['QString'].connect(functools.partial(self.display_info))
        self._view.comboBox_targetCoin.currentIndexChanged['QString'].connect(functools.partial(self.display_table))



# def main(helper):
#
#     app = QApplication(sys.argv)
#     win = QWidget()
#     win.setGeometry(200, 200, 300, 300)
#     win.setWindowTitle("Position Viewer")
#
#     gridLayout = QtWidgets.QGridLayout()
#     targetCoinComboBox = QtWidgets.QComboBox()
#     targetCoinComboBox.addItems(helper.getCoinsList())
#
#     gridLayout.addWidget(targetCoinComboBox, 0, 0)
#
#     okButton = QtWidgets.QPushButton()
#     okButton.setText('OK')
#     gridLayout.addWidget(okButton, 0, 1)
#
#     # gridLayout.addWidget(QtWidgets.QLabel('SIDE'), 1, 0)
#     # gridLayout.addWidget(QtWidgets.QLabel('PRICE'), 1, 1)
#     # gridLayout.addWidget(QtWidgets.QLabel('AMOUNT'), 1, 2)
#
#     # for i, order in enumerate(orders, start=2):
#     #     print(i, order['executedQty'])
#     #     gridLayout.addWidget(QtWidgets.QLabel(order['side']), i, 0)
#     #     gridLayout.addWidget(QtWidgets.QLabel(order['price']), i, 1)
#     #     gridLayout.addWidget(QtWidgets.QLabel(order['executedQty']), i, 2)
#     #
#     label = QtWidgets.QLabel(win)
#     label.resize(250, 250)
#     label.setText('Select Coin')
#
#     # # label.move(5, 85)
#     win.setLayout(gridLayout)
#     win.show()
#     sys.exit(app.exec_())


if __name__ == "__main__":
    # Create the application object
    app = QtWidgets.QApplication(sys.argv)

    # Create the form object
    main_window = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    # Show form
    main_window.show()
    model = BinanceHelper(key='insert key', secret='insert secret')
    AppController(model=model, view=ui)

    # Run the program
    sys.exit(app.exec())
