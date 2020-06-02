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
                'S': [4, 6],
                'Cl': [-1],  # Check this. I doubt other halogens other than F
                             # have only one oxidation state
                'Ar': [0],
                'K': [1],
                'Ca': [2],
                'Xe': [4, 6, 8]}

def main():
    print("CSG: Chemical Structure Generator\n")

    chem_form = input("Enter chemical structure: ")
    element_dict = get_elements(chem_form)
    valid = validate(element_dict)

    if valid:
        get_lp(element_dict)
    else:
        print()
    print(valid)


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

    first_element_charges, second_element_charges, element_list = [], [], []
    net_charge_zero = False
    element_list = []

    # Populating a list of input elements if they exist
    for el in element_dict:
        if el not in oxidn_states:
            print("Enter a valid chemical\n")
            return False
        else:
            element_list.append(el)

    # Check for deviation from strictly 2 elements
    if len(element_list) != 2:
        print("Only chemical compounds with 2 elements accepted\n")
        return False

    # Creating lists of total charge on individual elements in order to
    # be able to equate their sum to zero.
    for variable_oxidn_state in oxidn_states[element_list[0]]:
        first_element_charges.append(element_dict[element_list[0]] * variable_oxidn_state)

    for variable_oxidn_state in oxidn_states[element_list[1]]:
        second_element_charges.append(element_dict[element_list[1]] * variable_oxidn_state)

    # Summation to find the net charge. Validity of input auto-falsifies
    # if it fails to show zero net charge.
    for i in range(len(first_element_charges)):
        for j in range(len(second_element_charges)):
            net_charge = first_element_charges[i] + second_element_charges[j]
            if net_charge == 0:
                net_charge_zero = True
                break

    if not net_charge_zero:
        print("Enter a valid chemical\n")
        return False
    else:
        return True

def get_lp(element_dict):
    elm1,elm2=list(element_dict.keys())
    atm1,atm2=list(element_dict.values())

    if atm1>atm2:
        c_atom=elm2
        c_sub=atm2
        nc_atom=elm1
        nc_sub=atm1
    elif atm2>atm1:
        c_atom=elm1
        c_sub=atm1
        nc_atom=elm2
        nc_sub=atm2
    else:
        c_atom=0
    
    grp1={'H':1,
          'Li':3,
          'Na':11,
          'K':19,
          'Rb':37,
          'CS':55,
          'Fr':87}
    grp1_valency=1
    grp1_total_e=grp1.values()
    if elm1=="H":
        grp1_valnc_e=1
    else:
        grp1_valnc_e=2

    grp2={'Be':4,
          'Mg':12,
          'Ca':20,
          'Sr':38,
          'Ba':56,
          'Ra':88}
    grp2_valency=2
    gr2_total_e=grp2.values()
    grp2_valnc_e=2
    
    grp13={'B':5,
           'Al':13,
           'Ga':31,
           'In':49,
           'Ti':81}
    grp13_valency=3
    grp13_total_e=grp13.values()
    grp13_valnc_e=3

    grp14={'C':6,
           'Si':14,
           'Ge':32,
           'Sn':50,
           'Pb':82}
    grp14_valency=4
    grp14_total_e=grp14.values()
    grp14_valnc_e=4

    grp15={'N':7,
           'P':15,
           'As':33,
           'Sb':51,
           'Bi':83}
    grp15_valency=3
    grp15_total_e=grp15.values()
    grp15_valnc_e=5
    
    grp16={'O':8,
           'S':16,
           'Se':34,
           'Te':52,
           'Po':84}
    grp16_valency=2
    grp16_total_e=grp16.values()
    grp16_valnc_e=6

    grp17={'F':9,
           'Cl':17,
           'Br':35,
           'I':53,
           'At':85}
    grp17_valency=1
    grp17_total_e=grp17.values()
    grp17_valnc_e=7

    grp18={'He':2,
           'Ne':10,
           'Ar':18,
           'Kr':36,
           'Xe':54,
           'Rn':86}
    grp18_valency=0
    grp18_total_e=grp18.values()
    if elm1=="He":
        grp18_valnc_e=2
    else:
        grp18_valnc_e=8

    if c_atom!=0:
        if nc_atom in grp1 or nc_atom in grp17:
            elec1=grp1_valency*nc_sub
        elif nc_atom in grp2 or nc_atom in grp16:
            elec1=grp2_valency*nc_sub
        elif nc_atom in grp13 or nc_atom in grp15:
            elec1=grp3_valency*nc_sub
        elif nc_atm in grp4:
            elec1=grp4_valency*nc_sub
        
        if c_atom in grp1:
            elec2=grp1_valency*c_sub
            lp_e=(grp1_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp2:
            elec2=grp2_valency*c_sub
            lp_e=(grp2_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp13:
            elec2=grp13_valency*c_sub
            lp_e=(grp13_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp14:
            elec2=grp14_valency*c_sub
            lp_e=(grp14_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp15:
            elec2=grp15_valency*c_sub
            lp_e=(grp15_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp16:
            elec2=grp16_valency*c_sub
            lp_e=(grp16_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp17:
            elec2=grp17_valency*c_sub
            lp_e=(grp17_valnc_e)-elec2
            lp=lp_e/2
        elif c_atom in grp18:
            elec2=grp18_valency*c_sub
            lp_e=(grp18_valnc_e)-elec2
            lp=lp_e/2
    else:
        lp=0
        if elm1 in grp1 or elm1 in grp17:
            elec1=grp1_valency*atm1
        elif elm1 in grp2 or elm1 in grp16:
            elec1=grp2_valency*atm1
        elif elm1 in grp13 or elm1 in grp15:
            elec1=grp3_valency*atm1
        elif elm1 in grp4:
            elec1=grp4_valency*atm1
        
        if elm2 in grp1:
            elec2=grp1_valency*atm2
        elif elm2 in grp2:
            elec2=grp2_valency*atm2
        elif elm2 in grp13:
            elec2=grp13_valency*atm2
        elif elm2 in grp14:
            elec2=grp14_valency*atm2
        elif elm2 in grp15:
            elec2=grp15_valency*atm2
        elif elm2 in grp16:
            elec2=grp16_valency*atm2
        elif elm2 in grp17:
            elec2=grp17_valency*atm2
        elif elm2 in grp18:
            elec2=grp18_valency*atm2
    print("lone pair=",lp)
    


if __name__ == "__main__":
    main()
