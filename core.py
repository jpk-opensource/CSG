# core.py: Core CSG functions

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

import sqlite3
import re
from os import path, mkdir
from chemistry import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


oxidn_states = {
    'H':  [-1, 1],
    'He': [0],
    'Li': [1],
    'Be': [2],
    'B':  [3],
    'C':  [-4, 2, 4],
    'N':  [-2, 4, 3],
    'O':  [-2, 2],
    'F':  [-1, 1, 3],
    'Ne': [0],
    'Na': [1],
    'Mg': [2],
    'Al': [3],
    'Si': [4],
    'P':  [3, 5],
    'S':  [-2, 4, 6],
    'Cl': [-1, 3],
    'Ar': [0],
    'K':  [1],
    'Ca': [2],
    'Br': [-1, 1, 3, 5, 7],
    'I':  [-1, 1, 3, 5, 7],
    'Xe': [2, 4, 6, 8]
}

tick = '\u2713'


def main() -> None:
    print("CSG: Chemical Structure Generator v0.1")
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

    conn.close()


def init_csg_db() -> None:
    """
    init_csg_db():
        Initialize the CSG database, if it does not exist. At the moment,
        all it does is to create the history table if it doesn't exist.
    """
    if not path.isdir(".db"):
        print("[!] Creating database directory...")
        mkdir(".db")
        print(f"[{tick}] Done!")

    conn = sqlite3.connect(".db/csg_db.db")
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM history;")

    except sqlite3.OperationalError as ex:
        if "no such table" in str(ex):
            print("[!] Initializing History table...")
            table_str = "history("                                      \
                        "    number INTEGER PRIMARY KEY AUTOINCREMENT," \
                        "    command VARCHAR(32),"                      \
                        "    type VARCHAR(32)"                          \
                        ")"

            cur.execute(f"CREATE TABLE {table_str};")
            print(f"[{tick}] Done!")

        else:
            raise

    conn.close()


def init_geometry_db() -> None:
    conn = sqlite3.connect('.db/geometry.db')
    cur = conn.cursor()

    # compounds without lp
    cur.execute('''create table AB(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB values('nca1', '0', '0', '1')''')

    cur.execute('''create table AB2(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB2 values('nca1', '0', '-1', '0')''')
    cur.execute('''insert into AB2 values('nca2', '0', '1', '0')''')

    cur.execute('''create table AB3(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB3 values('nca1', '-0.67', '-0.5', '0')''')
    cur.execute('''insert into AB3 values('nca2', '0.67', '-0.5', '0')''')
    cur.execute('''insert into AB3 values('nca3', '0', '0.67', '0')''')

    cur.execute('''create table AB4(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB4 values('nca1', '-0.4', '-0.5', '-0.5')''')
    cur.execute('''insert into AB4 values('nca2', '0.4', '-0.5', '-0.5')''')
    cur.execute('''insert into AB4 values('nca3', '0', '0', '1')''')
    cur.execute('''insert into AB4 values('nca4', '0', '1', '-0.5')''')

    cur.execute('''create table AB5(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB5 values('nca1', '0', '3', '0')''')
    cur.execute('''insert into AB5 values('nca2', '0', '0', '-2')''')
    cur.execute('''insert into AB5 values('nca3', '2', '0', '1')''')
    cur.execute('''insert into AB5 values('nca4', '-2', '0', '1')''')
    cur.execute('''insert into AB5 values('nca5', '0', '-3', '0')''')

    cur.execute('''create table AB6(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB6 values('nca1', '0', '3', '0')''')
    cur.execute('''insert into AB6 values('nca2', '2', '0', '2')''')
    cur.execute('''insert into AB6 values('nca3', '-2', '0', '2')''')
    cur.execute('''insert into AB6 values('nca4', '2', '0', '-2')''')
    cur.execute('''insert into AB6 values('nca5', '-2', '0', '-2')''')
    cur.execute('''insert into AB6 values('nca6', '0', '-3', '0')''')

    # compounds with lp
    cur.execute('''create table AB2L(
                        atom text,
                        x text,
                        y text,
                        z text)
                        ''')
    cur.execute('''insert into AB2L values('nca1', '-0.8', '-0.1', '0')''')
    cur.execute('''insert into AB2L values('nca2', '0.8', '-0.1', '0')''')

    cur.execute('''create table AB3L(
                        atom text,
                        x text,
                        y text,
                        z text)
                        ''')
    cur.execute('''insert into AB3L values('nca1', '-0.4', '-0.5', '-0.5')''')
    cur.execute('''insert into AB3L values('nca2', '0.4', '-0.5', '-0.5')''')
    cur.execute('''insert into AB3L values('nca4', '0', '1', '-0.5')''')

    cur.execute('''create table AB4L(
                           atom text,
                           x text,
                           y text,
                           z text)
                           ''')
    cur.execute('''insert into AB4L values('nca1', '0', '3', '0')''')
    cur.execute('''insert into AB4L values('nca3', '2', '0', '-1')''')
    cur.execute('''insert into AB4L values('nca4', '-2', '0', '-1')''')
    cur.execute('''insert into AB4L values('nca5', '0', '-3', '0')''')

    cur.execute('''create table AB5L(
                               atom text,
                               x text,
                               y text,
                               z text)
                               ''')
    cur.execute('''insert into AB5L values('nca1', '0', '3', '0.5')''')
    cur.execute('''insert into AB5L values('nca2', '2', '0', '2.5')''')
    cur.execute('''insert into AB5L values('nca3', '-2', '0', '2')''')
    cur.execute('''insert into AB5L values('nca5', '-2', '0', '-2.5')''')
    cur.execute('''insert into AB5L values('nca6', '0', '-3', '0.5')''')

    cur.execute('''create table AB6L(
                                        atom text,
                                        x text,
                                        y text,
                                        z text)
                                        ''')
    cur.execute('''insert into AB6L values('nca1', '0', '3', '-1')''')
    cur.execute('''insert into AB6L values('nca2', '2', '0', '2')''')
    cur.execute('''insert into AB6L values('nca3', '-2', '-1', '2')''')
    cur.execute('''insert into AB6L values('nca4', '2', '0', '-2')''')
    cur.execute('''insert into AB6L values('nca5', '-2', '0', '-2')''')
    cur.execute('''insert into AB6L values('nca6', '0', '-3', '0')''')

    # compounds with 2 lp
    cur.execute('''create table AB2L2(
                                     atom text,
                                     x text,
                                     y text,
                                     z text)
                                     ''')
    cur.execute('''insert into AB2L2 values('nca1', '-5', '-3', '-4')''')
    cur.execute('''insert into AB2L2 values('nca2', '5', '-3', '-4')''')

    cur.execute('''create table AB3L2(
                                atom text,
                                x text,
                                y text,
                                z text)
                                ''')
    cur.execute('''insert into AB3L2 values('nca2', '0', '0', '-2')''')
    cur.execute('''insert into AB3L2 values('nca3', '2', '0', '1')''')
    cur.execute('''insert into AB3L2 values('nca4', '-2', '0', '1')''')

    cur.execute('''create table AB4L2(
                                    atom text,
                                    x text,
                                    y text,
                                    z text)
                                    ''')
    cur.execute('''insert into AB4L2 values('nca1', '0', '3', '0')''')
    cur.execute('''insert into AB4L2 values('nca2', '2', '0', '2')''')
    cur.execute('''insert into AB4L2 values('nca5', '-2', '0', '-2')''')
    cur.execute('''insert into AB4L2 values('nca6', '0', '-3', '0')''')

    conn.commit()
    conn.close()


def run_builtin_cmd(cmd_argv: list) -> None:
    """
    run_builtin_cmd():
        Pretty self-explanatory. Runs builtin commands, if it is recognized.
        Builtin commands start with '/'.
    """
    args = cmd_argv[1:]
    if cmd_argv[0] in ("/hist", "/history"):
        history(args)

    elif cmd_argv[0] == "/help":
        csg_help(args)

    elif cmd_argv[0] in ("/quit", "/exit"):
        print("Exiting...")
        exit()

    else:
        print(f"Invalid command: '{cmd_argv[0]}'")
        print("Try '/help' for more information.")


def history(args: list) -> None:
    conn = sqlite3.connect(".db/csg_db.db")
    cur = conn.cursor()

    hist_query = "SELECT * FROM history"
    show_hist = True

    if len(args) > 0:
        if args[0] == "clear":
            show_hist = False
            print("[-] Clearing history...")
            cur.execute("DELETE FROM history;")
            cur.execute("DELETE FROM sqlite_sequence WHERE name='history';")
            conn.commit()
            print(f"[{tick}] Done!")

        elif args[0] == "select":
            if len(args) != 2:
                print("Please specify a command type to select.")
                return

            elif args[1] not in ("formula", "builtin"):
                print(f"Invalid command type: '{args[1]}'")
                return

            else:
                hist_query += f" WHERE type='{args[1]}';"

        else:
            print(f"Invalid subcommand for '/history': {args[0]}")

    if show_hist:
        cur.execute(hist_query)

        print("{:>6}  {:<30}  {:<12}".format("No.", "Command", "Type"))
        for record in cur.fetchall():
            aligned = "{:>6}  {:<30}  {:<12}".format(str(record[0]), record[1],
                                                     record[2])
            print(aligned)

    conn.close()


def csg_help(args: list) -> None:
    if len(args) == 0:
        print("Valid commands:")
        print("\t{:<20}{:<20}".format("/history, /hist", "Print command history"))
        print("\t{:<20}{:<20}".format("/exit, /quit", "Exit CSG"))
        print("\t{:<20}{:<20}".format("/help", "Display this help message"))

    for arg in args:
        if arg == "/help":
            print("Usage: /help [name]\n"
                  "       Display command help, or (optionally) show usage info for\n"
                  "       a specific builtin command.\n")

            print("Examples\n"
                  "\t/help\n"
                  "\t/help /history")

        elif arg in ("/hist", "/history"):
            print("Usage: /history [subcommand]\n"
                  "       Show command history. If 'sub-command' is specified, execute it.\n")

            print("Subcommands:\n"
                  "       clear                 : Clear history\n"
                  "       select [command type] : Display history of specified command type only\n")

            print("Examples\n"
                  "\t/history\n"
                  "\t/history clear\n"
                  "\t/history select builtin")

        elif arg in ("/exit", "/quit"):
            print("Usage: /exit\n"
                  "       Exit CSG.")

        else:
            print(f"Invalid builtin command: '{arg}'")
            print("Try '/help' for more information")
            return


def get_elements(chem_form: str) -> dict:
    """
    get_elements():
        Returns a dictionary of elements, with the corresponding number
        of the same element present in the formula.

    Example:
        get_elements("H2O") returns {"H": 2, "O": 1}
    """

    if chem_form is None:
        return

    chem_form = chem_form.strip()

    # Formula should be of the form:
    #     <Element 1>[Subscript]<Element2>[Subscript]
    re_match = re.match("^([A-Z][a-z]?\d*){2}", chem_form)
    if re_match is None or re_match.group() != chem_form:
        return

    # This stores the final elements dictionary.
    element_dict = {}

    # The `current` element
    cur_el = ""

    # The string to hold number of atoms of the `current` element.
    # This value is a string, because we need to be able to concatenate
    # each digit to the end of this variable.
    cur_el_num_str = "1"

    # This flag is set when a digit is found in the formula.
    found_digit = False

    for ch in chem_form:
        if ch.isupper():
            # If `cur_el` is not empty, it means that
            # before *this* element, there was another element
            # in the formula. If `found_digit` is also not set,
            # it implies that the previous element did not have
            # any number to go along with it.
            if cur_el != "" and not found_digit:
                element_dict[cur_el] = 1

            cur_el = ch

            # Unset `found_digit` when uppercase letter is found
            found_digit = False

        elif ch.islower():
            cur_el += ch

            # Unset `found_digit` when lowercase letter is found
            found_digit = False

        elif ch.isdigit():
            if not found_digit:
                found_digit = True
                cur_el_num_str = ch
                element_dict[cur_el] = int(cur_el_num_str)

            else:
                cur_el_num_str += ch
                element_dict[cur_el] = int(cur_el_num_str)

    # If `found_digit` is False after the loop, it means that there was
    # no number specified for the last element. For example, this
    # would be true in the case of H2O
    if not found_digit:
        element_dict[cur_el] = 1

    return element_dict


# NO IS A BUG
def validate(chem_form: str) -> bool:
    """
    Checks if
        (a) Input chemical has only 2 elements
        (b) They exist, i.e, the constitute a key in the
            `oxidn_states` dict (which, btw, still requires a hell
            lotta additions)
        (c) Their net charge is zero (this condition checking is
            achieved by taking into account the oxidn states of each
           element)

    :parameter chem_form is a string
    :returns boolean
    """

    element_dict = get_elements(chem_form)
    if element_dict is None or len(element_dict) != 2:
        return False

    first_element_charges, second_element_charges, element_list = [], [], []
    net_charge_zero = False

    # Populating a list of input elements if they exist
    # No validation of transition elements
    for el in element_dict:
        if not pt.check(el):
            return False
        else:
            element_list.append(el)

    # Creating lists of total charge on individual elements in order to
    # be able to equate their sum to zero.
    for variable_oxidn_state in oxidn_states[element_list[0]]:
        first_element_charges.append(element_dict[element_list[0]]
                                     * variable_oxidn_state)

    for variable_oxidn_state in oxidn_states[element_list[1]]:
        second_element_charges.append(element_dict[element_list[1]]
                                      * variable_oxidn_state)

    # Summation to find the net charge. Validity of input auto-falsifies
    # if it fails to show zero net charge.
    for i in range(len(first_element_charges)):
        for j in range(len(second_element_charges)):
            net_charge = first_element_charges[i] + second_element_charges[j]
            if net_charge == 0:
                net_charge_zero = True
                break

    return net_charge_zero


def get_compound_stats(element_dict: dict) -> Stats:
    elements = list(element_dict.keys())
    subscripts = list(element_dict.values())

    # Central atom
    ca = ""

    # Central atom subscript
    ca_sub = 1

    # The least subscript among all
    min_sub = min(subscripts)

    if subscripts.count(min_sub) == 1:
        i = subscripts.index(min_sub)
        ca = elements[i]
        ca_sub = subscripts[i]

    # If there is no obvious central atom, pick the first one.
    if ca == "":
        ca = elements[0]
        ca_sub = subscripts[0]

    ca_dict = {ca: ca_sub}

    nca_dict = {}
    nca_sub = 1

    nca = ""
    for elem in elements:
        if elem != ca:
            nca = elem
            nca_sub = subscripts[elements.index(nca)]

    nca_dict = {nca: nca_sub}

    stats = Stats(ca_dict, nca_dict)

    return stats


def get_lp(element_dict: dict) -> float:
    """
    get_lp():
        Return the number of lone pairs in a given compound.
    """

    stats = get_compound_stats(element_dict)

    # 'Lone pairs' is initialized to the number of valence electrons
    # of the central atom.
    #
    # Using this formula:
    #       lp = (c_atom valence electrons - number of bond pair e's) / 2
    lp = stats.c_atom_nval_e * stats.c_atom_sub
    bp = pt.get_valency(stats.nc_atom) * stats.nc_atom_sub

    lp = (lp - bp) / 2

    return lp


def classify_geometry(element_dict: dict, lp: float) -> str:
    """
    classify_geometry():
        Classifies the geometry of a given compound, given
        `element_dict` (see get_elements()) and number of
        lone pairs `lp` (see get_lp()).
    """

    # There will be at least 2 atoms and no lone pairs by default
    geometry_dict = {'A': 1, 'B': 1, 'L': 0}

    for el in element_dict:
        if element_dict[el] > 1:
            geometry_dict['B'] = element_dict[el]
            break

    geometry_dict['L'] = int(lp)

    # Final classification
    geometry_str = ""

    for el in geometry_dict:
        # Subscript value
        sub = geometry_dict[el]

        if sub > 1:
            geometry_str += el + str(sub)

        elif sub == 1:
            geometry_str += el

    return geometry_str


def fetch_coordinates(geometry: str) -> tuple:
    """
        Initializing the geometry database if does not exist.
        To be used for fetching coordinates and rendering.
    """
    x, y, z = [], [], []

    conn = sqlite3.connect('.db/geometry.db')
    cur = conn.cursor()
    try:
        cur.execute(f'''select * from {geometry}''')

    except sqlite3.OperationalError as ex:
        if "no such table" in str(ex):
            init_geometry_db()
            cur.execute(f'''select * from {geometry}''')
        else:
            raise

    for record in cur.fetchall():
        x.append(float(record[1]))
        y.append(float(record[2]))
        z.append(float(record[3]))

    return x, y, z


def render(chem_form: str) -> None:
    """
        Fetches the information from the `geometry` database using the
        input_geometry parameter. Renders the input compound in 3-dimensional
        space using matplotlib, taking into account the user preferred theme
        and bond order.
    """
    element_dict = get_elements(chem_form)
    geometry = classify_geometry(element_dict, get_lp(element_dict))

    x, y, z = fetch_coordinates(geometry)

    ca, nca = '', ''
    element_list = []
    for ele in element_dict:
        element_list.append(ele)

    for ele in element_dict:
        if element_dict[ele] == 1:
            ca = ele
            element_list.remove(ca)
            break

    nca = element_list[0]

    # Get rid of the default toolbar
    mpl.rcParams['toolbar'] = 'None'

    fig = plt.figure(f'{chem_form} ({geometry} type)')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()

    ax.plot(x, y, z, 'o', c=pt.get_markercolor(nca),
            markersize=pt.get_markersize(nca))
    ax.plot(0, 0, 0, 'o', c=pt.get_markercolor(ca),
            markersize=pt.get_markersize(ca))

    conn = sqlite3.connect('.db/csg_db.db')
    cur = conn.cursor()
    cur.execute('select theme from user_preferences')
    theme = cur.fetchone()[0]
    conn.close()

    # Storing the hexadecimal color values as per user preference.
    # To be used for background color while rendering in matplotlib
    if theme == 'dark':
        facecolor = '#171717'
    else:
        facecolor = '#E9E9E9'

    ax.set_facecolor(facecolor)
    fig.patch.set_facecolor(facecolor)

    # Determining Bond Order and populating bond_params
    # for use in plotting bonds and placing legends
    if pt.get_nvalence_electrons(nca) == 1:
        bond_order = 1
    else:
        bond_order = 8 - pt.get_nvalence_electrons(nca)

    if bond_order == 1:
        bond_params = {
            'dark': 'royalblue', 'light': 'g', 'lw': 1, 'bo': 'single'
        }
    elif bond_order == 2:
        bond_params = {
            'dark': 'g', 'light': 'navy', 'lw': 2.5, 'bo': 'double'
        }
    else:
        bond_params = {
            'dark': 'b', 'light': 'red', 'lw': 3.5, 'bo': 'triple'
        }

    # Plotting Bonds
    for i in range(len(x)):
        ax.plot([0, x[i]], [0, y[i]], [0, z[i]], '-',
                linewidth=bond_params['lw'], c=bond_params[theme], alpha=0.75)

    # Placing Legends
    element_handles = [
        Line2D([0], [0], marker='o', color='w', label=nca,
               markerfacecolor=pt.get_markercolor(nca), markersize=15),

        Line2D([0], [0], marker='o', color='w', label=ca,
               markerfacecolor=pt.get_markercolor(ca), markersize=15)
    ]

    bond_handles = [
        Line2D([0], [0], color=bond_params[theme], lw=bond_params['lw'],
               label=bond_params['bo'], markerfacecolor=bond_params[theme],
               markersize=15)
    ]

    element_legend = plt.legend(handles=element_handles, loc=1,
                                bbox_to_anchor=(1.3, 1.15))

    # Adding `legend` artist to facilitate multiple legends on the same axes
    plt.gca().add_artist(element_legend)

    plt.legend(handles=bond_handles, title='Bond Order', loc=4,
               bbox_to_anchor=(1.12, 0.987))

    plt.show()

    conn = sqlite3.connect(".db/csg_db.db")
    cur = conn.cursor()
    cur.execute("SELECT command FROM history WHERE type='formula';")
    all_recs = cur.fetchall()

    if len(all_recs) == 0:
        print("NEW")
        cur.execute("INSERT INTO history VALUES(NULL, ?, ?);",
                    (chem_form, "formula"))
        conn.commit()

    else:
        chem_forms = []
        for rec in all_recs:
            chem_forms.append(rec[0])


        if chem_form not in chem_forms:
            print("NEW")
            cur.execute("INSERT INTO history VALUES(NULL, ?, ?);",
                        (chem_form, "formula"))
            conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
