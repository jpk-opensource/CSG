#!/usr/bin/python3

#
#   CSG: Chemical Structure Generator
#
#   Copyright (C) 2020 Jithin Renji, Kannan MD, Pranav Pujar
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from sys import argv
from PyQt5.QtWidgets import (QApplication, QDesktopWidget,
                             QWidget, QGridLayout, QVBoxLayout, 
                             QPushButton, QLabel, QMessageBox,
                             QLineEdit)

from csg_core import *

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.show()

    def init_UI(self):
        self.setWindowTitle("CSG: Chemical Structure Generator")
        self.resize(250, 150)
        self.center()
        self.grid = QGridLayout()

        self.grid.addWidget(QLabel("Chemical Formula:"), 0, 0)
        self.formula_field = QLineEdit()
        self.grid.addWidget(self.formula_field, 0, 1, 1, 3)

        self.go_btn = QPushButton("Go!")
        self.go_btn.setStyleSheet(":enabled {" +
                                        "color: white;" +
                                        "background-color: green;" +
                                  "}")
        self.go_btn.setDisabled(True)

        self.formula_field.textChanged.connect(self.enable_disable_btn)
        self.grid.addWidget(self.go_btn, 1, 1, 1, 2)

        self.go_btn.clicked.connect(self.on_go_btn_click)

        self.grid.setSpacing(10)
        self.setLayout(self.grid)

    def center(self):
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)

        self.move(rectangle.topLeft())

    def enable_disable_btn(self):
        if len(self.formula_field.text()) > 0:
            self.go_btn.setDisabled(False)

        else:
            self.go_btn.setDisabled(True)

    def on_go_btn_click(self): 
        element_dict = get_elements(self.formula_field.text())
        valid = validate(element_dict)

        if not valid:
            QMessageBox.warning(self, "Invalid Compound",
                                    "Enter a valid compound.",
                                    QMessageBox.Ok, QMessageBox.Ok)
            

if __name__ == "__main__":
    app = QApplication(argv)
    w = Home()
    w.show()
    app.exec_()
