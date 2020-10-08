# ui.py: CSG UI

#
#   Copyright (C) 2020 Jithin Renji, Kannan MD, Pranav Pujar
#
#   This file is part of CSG.
#
#   CSG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   CSG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with CSG.  If not, see <https://www.gnu.org/licenses/>.
#

from sys import argv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *

from core import *

DEFAULT_TITLE = "CSG: Chemical Structure Generator"

DARK_STYLESHEET = ""
LIGHT_STYLESHEET = ""
STYLESHEET = ""


class StackHolder(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 300)
        self.setWindowTitle(DEFAULT_TITLE)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout()
        back_btn_layout = QHBoxLayout()
        self.stackw = QStackedWidget()
        self.stackw.addWidget(Home())
        self.stackw.addWidget(PreferencesPage(self, self.stackw))

        # Populate the menubar
        menubar = QMenuBar()
        emenu_actions = menubar.addMenu("Edit")
        pref_action = emenu_actions.addAction("Preferences")
        pref_action.triggered.connect(self.set_preferences)

        self.back_btn = QPushButton("< Back")
        self.back_btn.setFixedSize(70, 30)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.hide()

        layout.addWidget(menubar)

        back_btn_layout.addWidget(self.back_btn)
        back_btn_layout.addStretch(1)

        layout.addLayout(back_btn_layout)
        layout.addWidget(self.stackw)
        self.setLayout(layout)

        self.show()

    def set_preferences(self):
        self.back_btn.show()
        self.setWindowTitle("CSG: Preferences")
        i = self.stackw.currentIndex()
        if i == 0:
            self.stackw.setCurrentIndex(1)

    def go_back(self):
        self.stackw.setCurrentIndex(0)
        self.setWindowTitle(DEFAULT_TITLE)
        self.back_btn.hide()


class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.init_UI()
        self.show()

    def init_UI(self):
        self.layout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.form_layout = QFormLayout()

        # Headings for the recents list and the program
        self.recents_label = QLabel("Recents:")
        self.csg_label = QLabel("<b>CSG</b>")
        self.csg_label.setFont(QFont("Arial", 25))
        self.csg_label.setAlignment(Qt.AlignCenter)

        # The main CSG form
        self.chem_form_label = QLabel("Chemical Formula:")
        self.formula_field = QLineEdit()
        self.formula_field.setFixedHeight(25)
        self.formula_field.textChanged.connect(self.formula_field_text_changed)

        self.go_btn = QPushButton("Go!")
        self.go_btn.setObjectName("go_btn")
        self.go_btn.setFixedHeight(25)
        self.go_btn.clicked.connect(self.go_btn_clicked)
        self.go_btn.setDisabled(True)

        self.formula_field.returnPressed.connect(self.go_btn_clicked)

        self.recents_list = QListWidget()
        self.recents_list.itemClicked.connect(self.recent_clicked)

        self.clear_recents_btn = QPushButton("Clear")
        self.clear_recents_btn.setFixedHeight(30)
        self.clear_recents_btn.clicked.connect(self.clear_recents_btn_clicked)
        self.clear_recents_btn.setCursor(Qt.PointingHandCursor)

        init_csg_db()
        conn = sqlite3.connect(".db/csg_db.db")
        cur = conn.cursor()
        cur.execute("SELECT command FROM history WHERE type='formula';")

        i = 0
        all_recs = cur.fetchall()
        items = []
        for rec in all_recs:
            items.append(rec[0])

        items = items[::-1]

        self.recents_list.addItems(items)
        conn.close()

        self.main_layout.addWidget(self.recents_label)
        self.main_layout.addWidget(self.recents_list)
        self.main_layout.addWidget(self.clear_recents_btn)

        self.form_layout.addRow(self.csg_label)
        self.form_layout.addRow(self.chem_form_label, self.formula_field)
        self.form_layout.addRow(self.go_btn)

        self.main_layout.addLayout(self.form_layout, 1, 1)

        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)

    def formula_field_text_changed(self):
        is_valid = validate(self.formula_field.text())
        if is_valid:
            self.formula_field.setStyleSheet("""
                border: 1px solid green;
                border-radius: 3px;
            """)
            self.go_btn.setEnabled(True)
            self.go_btn.setCursor(Qt.PointingHandCursor)

        else:
            self.formula_field.setStyleSheet("""
                border: 1px solid red;
                border-radius: 3px;
            """)
            self.go_btn.setDisabled(True)

    def do_render(self, chem_form):
        conn = sqlite3.connect(".db/csg_db.db")
        cur = conn.cursor()
        cur.execute("SELECT command FROM history WHERE type='formula';")
        all_rec = cur.fetchall()
        all_chem_forms = []
        for rec in all_rec:
            all_chem_forms.append(rec[0])

        if len(all_chem_forms) == 0 or chem_form not in all_chem_forms:
            cur.execute("INSERT INTO history VALUES(NULL, ?, ?);",
                        (chem_form, "formula"))
            conn.commit()
            self.recents_list.insertItem(0, chem_form)

        render(chem_form)
        conn.close()

    def go_btn_clicked(self):
        chem_form = self.formula_field.text()
        is_valid = validate(chem_form)
        if is_valid:
            self.do_render(chem_form)

    def clear_recents_btn_clicked(self):
        self.recents_list.clear()

        conn = sqlite3.connect(".db/csg_db.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM history WHERE type='formula';")
        conn.commit()
        conn.close()

    def recent_clicked(self, item):
        self.do_render(item.text())


class PreferencesPage(QWidget):
    def __init__(self, stackh: StackHolder, stackw: QStackedWidget):
        super().__init__()
        layout = QVBoxLayout()
        self.stackh = stackh
        self.stackw = stackw

        theme_label = QLabel("Theme")

        self.dark_radio_btn = QRadioButton("Dark theme")
        self.dark_radio_btn.clicked.connect(self.change_to_dark_theme)

        self.light_radio_btn = QRadioButton("Light Theme")
        self.light_radio_btn.clicked.connect(self.change_to_light_theme)

        if STYLESHEET == DARK_STYLESHEET:
            self.dark_radio_btn.setChecked(True)

        else:
            self.light_radio_btn.setChecked(True)

        layout.addWidget(theme_label)
        layout.addWidget(self.dark_radio_btn)
        layout.addWidget(self.light_radio_btn)
        layout.addStretch()

        self.setLayout(layout)
        self.show()

    def change_to_dark_theme(self):
        global STYLESHEET
        global DARK_STYLESHEET
        conn = sqlite3.connect(".db/csg_db.db")
        cur = conn.cursor()
        cur.execute("UPDATE user_preferences SET theme='dark';")
        conn.commit()
        conn.close()

        STYLESHEET = DARK_STYLESHEET
        self.stackh.setStyleSheet(STYLESHEET)

    def change_to_light_theme(self):
        global STYLESHEET
        global LIGHT_STYLESHEET
        conn = sqlite3.connect(".db/csg_db.db")
        cur = conn.cursor()
        cur.execute("UPDATE user_preferences SET theme='light';")
        conn.commit()
        conn.close()

        STYLESHEET = LIGHT_STYLESHEET
        self.stackh.setStyleSheet(STYLESHEET)


def ui_main():
    global STYLESHEET
    global LIGHT_STYLESHEET
    global DARK_STYLESHEET

    init_csg_db()

    with open("styles/light_theme.css") as light_theme:
        LIGHT_STYLESHEET = light_theme.read()

    with open("styles/dark_theme.css") as dark_theme:
        DARK_STYLESHEET = dark_theme.read()

    conn = sqlite3.connect(".db/csg_db.db")
    cur = conn.cursor()

    app = QApplication(argv)

    try:
        cur.execute("SELECT * FROM user_preferences;")

    except sqlite3.OperationalError as ex:
        if "no such table" in str(ex):
            print("[!] Initializing User Preferences table...")
            user_preferences_table = """
                user_preferences (
                    theme TEXT NOT NULL
                )
            """
            cur.execute(f"CREATE TABLE {user_preferences_table};")
            cur.execute("INSERT INTO user_preferences VALUES('dark');")
            conn.commit()
            print(f"[{tick}] Done!")

        else:
            raise

    cur.execute("SELECT theme FROM user_preferences;")
    theme_result = cur.fetchall()
    if theme_result[0][0] == "dark":
        STYLESHEET = DARK_STYLESHEET

    else:
        STYLESHEET = LIGHT_STYLESHEET

    w = StackHolder()

    conn.close()
    w.show()
    app.exec_()


if __name__ == "__main__":
    ui_main()
