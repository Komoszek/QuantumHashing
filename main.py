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
        self.controlQubitNumberLabel.setText("Liczba kubitów:")
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

        self.showStateVectorButton = QPushButton(self)
        self.showStateVectorButton.setText("Wyświetl wektor stanów")
        self.showStateVectorButton.clicked.connect(self.showStateVectorButtonClicked)
        layout.addWidget(self.showStateVectorButton, 1, 1, 1, 1)

        self.showQuantumCircuitButton = QPushButton(self)
        self.showQuantumCircuitButton.setText("Wyświetl schemat układu kwantowego")
        self.showQuantumCircuitButton.clicked.connect(self.showQuantumCircuitButtonClicked)
        layout.addWidget(self.showQuantumCircuitButton, 2, 1, 1, 1)

        self.inputSwapTestWordLabel = QLabel(self)
        self.inputSwapTestWordLabel.setText("Binarne słowo wejściowe do porównania \nw Swap test:")
        layout.addWidget(self.inputSwapTestWordLabel, 3, 1, 1, 1)

        self.inputSwapTestWordLine = QLineEdit(self)
        self.inputSwapTestWordLine.setValidator(binaryValidator)
        layout.addWidget(self.inputSwapTestWordLine, 4, 1, 1, 1)

        self.swapTestButton = QPushButton(self)
        self.swapTestButton.setText("Wykonaj Swap test")
        self.swapTestButton.clicked.connect(self.swapTestButtonClicked)
        layout.addWidget(self.swapTestButton, 5, 1, 1, 1)

        self.authorsLabel = QLabel(self)
        self.authorsLabel.setText("Autorzy: Komoszyński Łukasz, Ulaski Wojciech, Zadrożny Bartosz")
        layout.addWidget(self.authorsLabel, 8, 0, 1, 2)

    def processTable(self):
        k = []
        for row in range(self.paramTable.rowCount()):
            item = self.paramTable.item(row, 0)
            text = item.text()
            k.append(int(text))

        return k

    def setupQuantumHasher(self):
        self.quantumHasher.msg = [int(d) for d in self.inputWordLine.text()]
        self.quantumHasher.control_qubits_num = self.inputControlQubitNumber.value()
        self.quantumHasher.k = self.processTable()

    def swapTestButtonClicked(self):
        print("swap test button clicked")
        first_message = [int(d) for d in self.inputWordLine.text()]
        second_message = [int(d) for d in self.inputSwapTestWordLine.text()]
        if(len(first_message) != len(second_message)):
            QMessageBox.about(self, "Error", "Długości wiadomości muszą być równe!")
            return

        control_qubits_count = self.inputControlQubitNumber.value()
        k = self.processTable()
        swapTester = SwapTester(first_message, second_message, control_qubits_count, k)
        swapTester.run_test(self)

    def showQuantumCircuitButtonClicked(self):
        self.setupQuantumHasher()
        self.quantumHasher.show_circuit()

    def showHistogramButtonClicked(self):
        self.setupQuantumHasher()
        self.quantumHasher.show_histogram()

    def showStateVectorButtonClicked(self):
        print("show state vector button clicked")

    def adjustTableRowCount(self, qubitNumber):
        self.paramTable.setRowCount(2 ** qubitNumber)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Kwantowo inspirowana funkcja skrótu")

    mainWin = MainWindow()
    mainWin.show()

    app.exec()
