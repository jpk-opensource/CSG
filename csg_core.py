# csg_core.py: Core CSG functions

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

import sqlite3
from os         import path, mkdir
from chemistry  import PeriodicTable, Stats

oxidn_states = {'H': [-1, 1],
                'He': [0],
                'Li': [1],
                'Be': [2],
                'B': [3],
                'C': [-4, 2, 4],
                'N': [-3, -2, 4],  # There are more ig. have to look into this
                'O': [-2, -1, 1, 2],  # Must include -0.5, which causes errors
                'F': [-1, 1],
                'Ne': [0],
                'Na': [1],
                'Mg': [2],
                'Al': [3],
                'Si': [4],
                'P': [3, 5],
                'S': [-2, 4, 6],
                'Cl': [-1],  # Check this. I doubt other halogens other than F
                             # have only one oxidation state
                'Ar': [0],
                'K': [1],
                'Ca': [2],
                'Xe': [2, 4, 6, 8]}

tick = '\u2713'

def main():
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
        cur.execute("INSERT INTO history VALUES(NULL, ?, ?);", (chem_form, cmd_type))
        conn.commit()

        if chem_form.strip()[0] == '/':
            run_builtin_cmd(chem_form.split())
            continue

        element_dict = get_elements(chem_form)
        valid = validate(element_dict)

        if valid:
            lp = get_lp(element_dict)
            print(f"Lone Pairs: {lp}")

    conn.close()

def init_csg_db():
    """
    init_csg_db():
        Initialize the CSG database, if it does not exist. At the moment,
        all it does is to create the history table if it doesn't exist.
    """
    if not path.isdir(".db"):
        print("[!] .db/ does not exist. Creating now...")
        mkdir(".db")
        print(f"[{tick}] Done!")

    conn = sqlite3.connect(".db/csg_db.db")
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM history;")

    except Exception:
        print("[!] History table does not exist. Creating now...")
        table_str = "history("                                      \
                    "    number INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "    command VARCHAR(32),"                      \
                    "    type VARCHAR(32)"                          \
                    ")"

        cur.execute(f"CREATE TABLE {table_str};")
        print(f"[{tick}] Done!")

    conn.close()

def run_builtin_cmd(cmd_argv):
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

def history(args):
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
            print (f"[{tick}] Done!")

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
            aligned = "{:>6}  {:<30}  {:<12}".format(str(record[0]), record[1], record[2])
            print(aligned)

    conn.close()

def csg_help(args):
    if len(args) == 0:
        print("Valid commands:")
        print("\t{:<20} : {:<20}".format("/history, /hist", "Print command history"))
        print("\t{:<20} : {:<20}".format("/exit, /quit", "Exit CSG"))
        print("\t{:<20} : {:<20}".format("/help", "Display this help message"))

    for arg in args:
        if arg == "/help":
            print("Usage: /help [name]\n" +
                  "       Display command help, or (optionally) show usage info for\n" +
                  "       a specific builtin command.\n")

            print("Examples\n" +
                  "\t/help\n" +
                  "\t/help /history")

        elif arg in ("/hist", "/history"):
            print("Usage: /history [subcommand]\n" +
                  "       Show command history. If 'sub-command' is specified, execute it.\n")

            print("Subcommands:\n" +
                  "       clear                 : Clear history\n" +
                  "       select [command type] : Display history of specified command type only\n")

            print("Examples\n" +
                  "\t/history\n" +
                  "\t/history clear\n"+
                  "\t/history select builtin")

        elif arg in ("/exit", "/quit"):
            print("Usage: /exit\n" +
                  "       Exit CSG.")

        else:
            print(f"Invalid builtin command: '{arg}'")
            print("Try '/help' for more information")
            return

def get_elements(chem_form):
    """
    get_elements():
        Returns a dictionary of elements, with the corresponding number
        of the same element present in the formula.

    Example:
        get_elements("H2O") returns {"H": 2, "O": 1}
    """

    chem_form = chem_form.strip()

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


def validate(element_dict):
    """
    Checks if
        (a) Input chemical has only 2 elements
        (b) They exist, i.e, the constitute a key in the
            `oxidn_states` dict (which, btw, still requires a hell
            lotta additions)
        (c) Their net charge is zero (this condition checking is
            achieved by taking into account the oxidn states of each
           element)

    :parameter element_dict is a dictionary (see element_dict from main())
    :returns boolean
    @kannan the exceptions are taken care of by the various oxidation states
    listed in `oxidn_states` (only for compounds with 2 elements)
    """
    pt = PeriodicTable()
    first_element_charges, second_element_charges, third_element_charges, element_list = [], [], [], []
    net_charge_zero = False
    element_list = []

    # Populating a list of input elements if they exist
    # Transition metals wont properly be validated cos oxidn states is incomplete
    for el in element_dict:
        if not pt.check(el):
            print("Enter a valid chemical")
            return False
        else:
            element_list.append(el)

    # Check for deviation from strictly 2 elements
    if len(element_list) not in [2, 3]:
        print("Enter a valid chemical")
        return False

    # Creating lists of total charge on individual elements in order to
    # be able to equate their sum to zero.
    for variable_oxidn_state in oxidn_states[element_list[0]]:
        first_element_charges.append(element_dict[element_list[0]] * variable_oxidn_state)

    for variable_oxidn_state in oxidn_states[element_list[1]]:
        second_element_charges.append(element_dict[element_list[1]] * variable_oxidn_state)

    if len(element_list) == 3:
        for variable_oxidn_state in oxidn_states[element_list[2]]:
            third_element_charges.append(element_dict[element_list[2]] * variable_oxidn_state)


    # Summation to find the net charge. Validity of input auto-falsifies
    # if it fails to show zero net charge.
    for i in range(len(first_element_charges)):
        for j in range(len(second_element_charges)):
            if len(element_list) == 3:
                for k in range(len(third_element_charges)):
                    net_charge = first_element_charges[i] + second_element_charges[j] + third_element_charges[k]
                    if net_charge == 0:
                        net_charge_zero = True
                        break
            else:
                net_charge = first_element_charges[i] + second_element_charges[j]
                if net_charge == 0:
                    net_charge_zero = True
                    break

    if not net_charge_zero:
        print("Enter a valid chemical")
        return False

    else:
        return True


def get_compound_stats(element_dict):
    pt = PeriodicTable()
    elements = list(element_dict.keys())
    subscripts = list(element_dict.values())

    central_atom = ""

    min_sub = min(subscripts)
    if subscripts.count(min_sub) == 1:
        central_atom = elements[subscripts.index(min_sub)]

    elif len(elements) == 3:
        max_valence_electrons = 0
        for el in elements:
            nv_e = pt.get_nvalence_electrons(el)

            if element_dict[el] == 1:
                if nv_e > max_valence_electrons:
                    max_valence_electrons = nv_e
                    central_atom = el

    if central_atom == "":
        central_atom = elements[0]

    # List of non central atoms
    nca_dict = {}

    for el in elements:
        if el != central_atom:
            nca_dict[el] = element_dict[el]

    stats = Stats(central_atom, nca_dict)

    return stats

def get_lp(element_dict):
    """
    get_lp():
        Return the number of lone pairs in a given compound.
    """
    pt = PeriodicTable()
    stats = get_compound_stats(element_dict)

    # Dictionary of non-central atoms
    nc_atoms = stats.nc_atom_dict

    # 'Lone pairs' is initialized to the number of valence electrons
    # of the central atom.
    #
    # We are utilizing this formula:
    #       lp = (c_atom valence electrons - number of bond pair e's) / 2
    lp = stats.c_atom_nval_e
    bp = 0

    for el in nc_atoms:
        bp += pt.get_valency(el) * nc_atoms[el]

    lp = (lp - bp) / 2

    return lp

def classify_geometry(element_dict, lp):
    """
    classify_geometry():
        Classifies the geometry of a given compound, given
        `element_dict` (see get_elements()) and number of
        lone pairs `lp` (see get_lp()).

        This function returns a dictionary.

    Example:
        classify_geometry({'H': 2, 'O': 1}, 1) returns
        {'A': 1, 'B': 2, 'L': 1}
    """

    # This dictionary holds the final classification.
    geometry = {'A': 1, 'B': 1, 'L': 0}

    for el in element_dict:
        if element_dict[el] > 1:
            geometry['B'] = element_dict[el]
            break

    geometry['L'] = int(lp)
    return geometry


def gdict_to_str(geometry_dict):
    """
    gdict_to_str():
        Coverts a geometry dictionary to string.

    Example:
        gdict_to_str({'A': 1, 'B': 2, 'L': 0}) returns
        "AB2"
    """

    # This stores the final geometry string
    geometry_str = ""

    for el in geometry_dict:
        # Subscript value
        sub = geometry_dict[el]

        if sub > 1:
            geometry_str += el + str(sub)

        elif sub == 1:
            geometry_str += el

    return geometry_str


if __name__ == "__main__":
    main()
