#!/usr/bin/env python3

import sys

import quantumHashing
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from swapTester import SwapTester


class TableInputDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        w = QLineEdit(parent)
        w.setValidator(QRegularExpressionValidator(QRegularExpression("\d*")))
        return w


class MainWindow(QMainWindow):
    def __init__(self):
        self.quantumHasher = quantumHashing.QuantumHash()
        self.quantumHasher2 = quantumHashing.QuantumHash()
        QMainWindow.__init__(self)
        binaryValidator = QRegularExpressionValidator(QRegularExpression("[0-1]*"))

        self.setMinimumSize(600, 460)
        self.setMaximumSize(600, 460)
        self.setWindowTitle("Kwantowo inspirowana funkcja skrótu")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QGridLayout(centralWidget)

        self.inputWordLabel = QLabel(self)
        self.inputWordLabel.setText("Binarne słowo wejściowe:")
        layout.addWidget(self.inputWordLabel, 0, 0, 1, 1)

        self.inputWordLine = QLineEdit(self)
        self.inputWordLine.setValidator(binaryValidator)
        layout.addWidget(self.inputWordLine, 1, 0, 1, 1)

        self.controlQubitNumberLabel = QLabel(self)
        self.controlQubitNumberLabel.setText("Liczba kubitów kontrolnych:")
        self.controlQubitNumberLabel.adjustSize()
        layout.addWidget(self.controlQubitNumberLabel, 2, 0, 1, 1)

        self.inputControlQubitNumber = QSpinBox(self)
        self.inputControlQubitNumber.setMinimum(1)
        self.inputControlQubitNumber.setMaximum(4)
        self.inputControlQubitNumber.valueChanged.connect(self.adjustTableRowCount)
        layout.addWidget(self.inputControlQubitNumber, 3, 0, 1, 1)

        self.paramTable = QTableWidget(self)
        self.paramTable.setColumnCount(1)
        self.paramTable.setRowCount(2)
        self.paramTable.setHorizontalHeaderLabels(['Wartość współczynnika'])
        self.paramTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.paramTable.setItemDelegate(TableInputDelegate())
        layout.addWidget(self.paramTable, 5, 0, 3, 1)

        self.showHistogramButton = QPushButton(self)
        self.showHistogramButton.setText("Wyświetl histogram")
        self.showHistogramButton.clicked.connect(self.showHistogramButtonClicked)
        layout.addWidget(self.showHistogramButton, 0, 1, 1, 1)

        self.showQuantumCircuitButton = QPushButton(self)
        self.showQuantumCircuitButton.setText("Wyświetl schemat układu kwantowego")
        self.showQuantumCircuitButton.clicked.connect(self.showQuantumCircuitButtonClicked)
        layout.addWidget(self.showQuantumCircuitButton, 1, 1, 1, 1)

        self.inputSwapTestWordLabel = QLabel(self)
        self.inputSwapTestWordLabel.setText("Binarne słowo wejściowe do porównania \nw Swap test:")
        layout.addWidget(self.inputSwapTestWordLabel, 2, 1, 1, 1)

        self.inputSwapTestWordLine = QLineEdit(self)
        self.inputSwapTestWordLine.setValidator(binaryValidator)
        layout.addWidget(self.inputSwapTestWordLine, 3, 1, 1, 1)

        self.swapTestShowButton = QPushButton(self)
        self.swapTestShowButton.setText("Pokaż układ kwantowy Swap testu")
        self.swapTestShowButton.clicked.connect(self.swapTestShowButtonClicked)
        layout.addWidget(self.swapTestShowButton, 4, 1, 1, 1)

        self.swapTestButton = QPushButton(self)
        self.swapTestButton.setText("Wykonaj Swap test")
        self.swapTestButton.clicked.connect(self.swapTestButtonClicked)
        layout.addWidget(self.swapTestButton, 5, 1, 1, 1)

        self.authorsLabel = QLabel(self)
        self.authorsLabel.setText("Autorzy: Komoszyński Łukasz, Ulaski Wojciech, Zadrożny Bartosz")
        layout.addWidget(self.authorsLabel, 8, 0, 1, 2)

    def processTable(self):
        k = []
        maxVal = 2 ** len(self.inputWordLine.text()) - 1
        for row in range(self.paramTable.rowCount()):
            item = self.paramTable.item(row, 0)
            if item is None:
                QMessageBox.about(self, "Error", f"Brak współczynnika na {row+1} pozycji!")
                return None
            text = item.text()
            value = int(text)

            if value < 0 or value > maxVal:
                QMessageBox.about(self, "Error", f"Współczynnik na {row+1} pozycji spoza zakresu [0, {maxVal}]!")
                return None
            k.append(value)

        return k

    def setupQuantumHasher(self):
        table = self.processTable()
        if table is None:
            return False

        self.quantumHasher.msg = [int(d) for d in self.inputWordLine.text()]
        self.quantumHasher.control_qubits_num = self.inputControlQubitNumber.value()
        self.quantumHasher.k = table

        self.quantumHasher2.msg = [int(d) for d in self.inputSwapTestWordLine.text()]
        self.quantumHasher2.control_qubits_num = self.quantumHasher.control_qubits_num
        self.quantumHasher2.k = self.quantumHasher.k
        return True

    def setupSwapTester(self):
        if(len(self.inputWordLine.text()) != len(self.inputSwapTestWordLine.text())):
            QMessageBox.about(self, "Error", "Długości wiadomości muszą być równe!")
            return None

        if not self.setupQuantumHasher():
            return None

        return SwapTester(self.quantumHasher, self.quantumHasher2)

    def swapTestShowButtonClicked(self):
        swapTester = self.setupSwapTester()
        if swapTester is not None:
            swapTester.show_circuit()

    def swapTestButtonClicked(self):
        swapTester = self.setupSwapTester()
        if swapTester is not None:
            swapTester.run_test(self)

    def showQuantumCircuitButtonClicked(self):
        if not self.setupQuantumHasher():
            return
        self.quantumHasher.show_circuit()

    def showHistogramButtonClicked(self):
        if not self.setupQuantumHasher():
            return
        self.quantumHasher.show_histogram()

    def adjustTableRowCount(self, qubitNumber):
        self.paramTable.setRowCount(2 ** qubitNumber)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Kwantowo inspirowana funkcja skrótu")

    mainWin = MainWindow()
    mainWin.show()

    app.exec()
