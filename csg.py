#!/usr/bin/env python3

#
#   CSG: Chemical Structure Generator
#
#   Copyright (C) 2020-2021 Jithin Renji, Kannan MD, Pranav Pujar
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

import sqlite3

from core import (init_csg_db, validate, run_builtin_cmd, get_elements, get_lp,
                 classify_geometry, render)
from ui import ui_init


VERSION = "v0.1-alpha.3"


def main():
    if "--cli" in argv:
        repl()

    elif "--help" in argv or "-h" in argv:
        usage()
        exit()

    elif "--version" in argv or "-V" in argv:
        version()
        exit()

    try:
        if len(argv) > 1:
            print("[!] Ignoring extra argument(s): ", ", ".join(argv[1:]))

        ui_init()

    except ModuleNotFoundError:
        print("[!] PyQt5 needs to be installed to run the graphical front-end.")
        print(f"""[!] Try running '{argv[0]} --cli' to run CSG from the command-line
    or install PyQt5 by running 'pip install pyqt5'""")

        exit()


def repl() -> None:
    print(f"CSG: Chemical Structure Generator {VERSION}")
    print("Type '/help' for help on command usage.\n")

    init_csg_db()
    conn = sqlite3.connect(".db/csg_db.db")
    cur = conn.cursor()

    while True:
        try:
            chem_form = input(">> ")

        # Exit on Ctrl-D
        except EOFError:
            print("Exiting...")
            conn.close()
            exit()

        # Ignore Ctrl-C
        except KeyboardInterrupt:
            print()
            continue

        if chem_form == '':
            continue

        cmd_type = "builtin" if chem_form[0] == '/' else "formula"

        if chem_form.strip()[0] == '/':
            run_builtin_cmd(chem_form.split())
            cur.execute("INSERT INTO history VALUES(NULL, ?, ?);",
                        (chem_form, cmd_type))
            conn.commit()
            continue

        valid = validate(chem_form)

        if valid:
            element_dict = get_elements(chem_form)
            lp = get_lp(element_dict)
            geometry = classify_geometry(element_dict, lp)

            print("{:<10} : {:<6}".format("Lone Pairs", lp))
            print("{:<10} : {:<6}".format("Geometry", geometry))

            render(chem_form)

        else:
            print("Enter a valid compound with exactly 2 elements.")


def usage():
    print(f"Usage: {argv[0]} [OPTION]")
    print("\tGenerate simple chemical structures.\n")

    print("Options:")
    print("\t{:<21}{:<20}".format("--cli", "Run in the terminal"))
    print("\t{:<15}{:<6}{:<20}".format("--help,", "-h", "Show this help message and exit"))
    print("\t{:<15}{:<6}{:<20}".format("--version,", "-V", "Show version information and exit"))


def version():
    print(f"""\
CSG {VERSION}
Copyright (C) 2020-2021 Jithin Renji, Kannan MD, and Pranav Pujar
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Jithin Renji, Kannan MD, and Pranav Pujar.\
""")


if __name__ == "__main__":
    main()
