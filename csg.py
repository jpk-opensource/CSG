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
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *

from csg_core import *

DEFAULT_TITLE = "CSG: Chemical Structure Generator"

DARK_STYLESHEET = """
    QWidget {
        background-color: rgb(23, 23, 23);
        color: white;
    }

    QLineEdit, QListWidget {
        background-color: rgb(30, 30, 30);
        color: white;
    }

    QMenuBar {
        background-color: rgb(0, 0, 0);
    }
"""

LIGHT_STYLESHEET = """
    QWidget {
        background-color: rgb(230, 230, 230);
        color: black;
    }

    QLineEdit, QListWidget {
        background-color: rgb(255, 255, 255);
        color: black;
    }
"""

STYLESHEET = ""

class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.init_UI()
        self.show()

    def init_UI(self):
        self.setWindowTitle(DEFAULT_TITLE)
        self.setStyleSheet(DARK_STYLESHEET)

        self.layout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.form_layout = QFormLayout()


        self.recents_label = QLabel("Recents:")
        self.csg_label = QLabel("<b>CSG</b>")
        self.csg_label.setFont(QFont("Arial", 25))
        self.csg_label.setAlignment(Qt.AlignCenter)

        self.chem_form_label = QLabel("Chemical Formula:")
        self.formula_field = QLineEdit()
        self.go_btn = QPushButton("Go!")

        self.recents_list = QListWidget()

        init_csg_db()
        conn = sqlite3.connect(".db/csg_db.db")
        cur = conn.cursor()
        cur.execute("SELECT command FROM history WHERE type='formula';")

        i = 0
        for rec in cur.fetchall():
            self.recents_list.insertItem(i, rec[0])
            i += 1
        conn.close()

        self.main_layout.addWidget(self.recents_label)
        self.main_layout.addWidget(self.recents_list)

        self.form_layout.addRow(self.csg_label)
        self.form_layout.addRow(self.chem_form_label, self.formula_field)
        self.form_layout.addRow(self.go_btn)

        self.main_layout.addLayout(self.form_layout, 1, 1)

        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)

if __name__ == "__main__":
    if "--cli" in argv:
        main()
        exit()

    conn = sqlite3.connect(".db/csg_db.db")
    cur  = conn.cursor()
    
    app = QApplication(argv)

    try:
        cur.execute("SELECT * FROM user_preferences;")

    except Exception:
        print("[!] User preferences table does not exist! Creating...")
        user_preferences_table = """
            user_preferences (
                theme TEXT NOT NULL
            )
        """
        cur.execute(f"CREATE TABLE {user_preferences_table};")
        cur.execute("INSERT INTO user_preferences VALUES('dark');")
        print(f"[{tick}] Done!")

    w = Home()

    conn.close()        
    w.show()
    app.exec_()
