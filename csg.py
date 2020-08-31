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

VERSION = "v0.1-alpha"


def start_csg():
    if "--cli" in argv:
        from core import main
        main()

    elif "--help" in argv or "-h" in argv:
        usage()
        exit()

    elif "--version" in argv or "-V" in argv:
        version()
        exit()

    try:
        from ui import ui_main

        if len(argv) > 1:
            print("[!] Ignoring extra argument(s): ", ", ".join(argv[1:]))

        ui_main()

    except ModuleNotFoundError:
        print("[!] PyQt5 needs to be installed to run the graphical front-end.")
        print(f"""[!] Try running '{argv[0]} --cli' to run CSG from the command-line
    or install PyQt5 by running 'pip install pyqt5'""")

        exit()


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
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
""")


if __name__ == "__main__":
    start_csg()
