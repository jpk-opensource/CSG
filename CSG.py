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
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QVBoxLayout, QDialog, QDialogButtonBox,
                             QPushButton, QLabel, QLineEdit)

from csg_core import *

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.show()

    def init_UI(self):
        self.setWindowTitle("CSG: Chemical Structure Generator")
        self.grid = QGridLayout()

        self.grid.addWidget(QLabel("Chemical Formula:"), 0, 0)
        self.formula_field = QLineEdit()
        self.grid.addWidget(self.formula_field, 0, 1, 1, 3)

        self.go_btn = QPushButton("Go!")
        self.grid.addWidget(self.go_btn, 1, 1, 1, 2)

        self.go_btn.clicked.connect(self.on_go_btn_click)

        self.grid.setSpacing(10)
        self.setLayout(self.grid)

    def on_go_btn_click(self):
        element_dict = get_elements(self.formula_field.text())
        valid = validate(element_dict)

        if not valid:
            invalid_dlg = QDialog(self)
            invalid_dlg.setWindowTitle("Invalid Compound")

            dlg_btns = QDialogButtonBox.Ok
            dlg_btn_box = QDialogButtonBox(dlg_btns)
            dlg_btn_box.accepted.connect(invalid_dlg.accept)

            dlg_layout = QVBoxLayout()
            dlg_layout.addWidget(dlg_btn_box)

            invalid_dlg.setLayout(dlg_layout)
            invalid_dlg.exec_()

if __name__ == "__main__":
    app = QApplication(argv)
    w = Home()
    w.show()
    app.exec_()
