# chemistry.py: The Chemistry module for CSG

#
#   Copyright (C) 2020-2021 Jithin Renji, Kannan MD, Pranav Pujar
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

class PeriodicTable:
    """
    Contains elements elements which can form compounds according to the
    VSEPR theory.
    """
    def __init__(self):
        self.__groups = {
            1:  {
                'H':  1,  'Li': 3,  'Na': 11, 'K': 19,
                'Rb': 37, 'Cs': 55, 'Fr': 87
            },
            2:  {
                'Be': 4, 'Mg': 12, 'Ca': 20, 'Sr': 38, 'Ba': 56, 'Ra': 88
            },
            13: {
                'B':  5, 'Al': 13, 'Ga': 31, 'In': 49, 'Ti': 81
            },
            14: {
                'C':  6, 'Si': 14, 'Ge': 32, 'Sn': 50, 'Pb': 82
            },
            15: {
                'N':  7, 'P':  15, 'As': 33, 'Sb': 51, 'Bi': 83
            },
            16: {
                'O':  8, 'S':  16, 'Se': 34, 'Te': 52, 'Po': 84
            },
            17: {
                'F':  9, 'Cl': 17, 'Br': 35, 'I':  53, 'At': 85
            },
            18: {
                'He': 2, 'Ne': 10, 'Ar': 18, 'Kr': 36, 'Xe': 54, 'Rn': 86
            }
        }

        self.__group_valencies = {
            1:  1,
            2:  2,
            13: 3,
            14: 4,
            15: 3,
            16: 2,
            17: 1,
            18: 0
        }

        self.__group_valence_electrons = {
            1:  1,
            2:  2,
            13: 3,
            14: 4,
            15: 5,
            16: 6,
            17: 7,
            18: 8
        }

        self.__atomic_numbers = {
            'H':  1,
            'He': 2,
            'Li': 3,
            'Be': 4,
            'B':  5,
            'C':  6,
            'N':  7,
            'O':  8,
            'F':  9,
            'Ne': 10,
            'Na': 11,
            'Mg': 12,
            'Al': 13,
            'Si': 14,
            'P':  15,
            'S':  16,
            'Cl': 17,
            'Ar': 18,
            'K':  19,
            'Ca': 20,
            'Br': 35,
            'I':  53,
            'Xe': 54
        }

        self.__atomic_colors = [
            (135, 206, 235), (217, 255, 255), (204, 128, 255), (194, 255, 0),
            (255, 181, 181), (144, 144, 144), (48, 80, 248),   (255, 13, 13),
            (144, 224, 80),  (179, 227, 245), (171, 92, 242),  (138, 255, 0),
            (191, 166, 166), (240, 200, 160), (255, 128, 0),   (255, 255, 48),
            (31, 240, 31),   (128, 209, 227), (143, 64, 212),  (61, 225, 0),
            (230, 230, 230), (191, 194, 199), (166, 166, 171), (138, 153, 199),
            (156, 122, 199), (224, 102, 51),  (240, 144, 160), (80, 208, 80),
            (200, 128, 51),  (125, 128, 176), (194, 143, 143), (102, 143, 143),
            (189, 128, 227), (225, 161, 0),   (166, 41, 41),   (92, 184, 209),
            (112, 46, 176),  (0, 255, 0),     (148, 255, 255), (148, 224, 224),
            (115, 194, 201), (84, 181, 181),  (59, 158, 158),  (36, 143, 143),
            (10, 125, 140),  (0, 105, 133),   (192, 192, 192), (255, 217, 143),
            (166, 117, 115), (102, 128, 128), (158, 99, 181),  (212, 122, 0),
            (148, 0, 148),   (66, 158, 176),  (87, 23, 143),   (0, 201, 0),
            (112, 212, 255)
        ]

    def check(self, element):
        """
        Check if an element is present in the periodic table (as defined
        above).

        Args:
            element: the element which should be checked
        """
        for i in self.__groups:
            if element in self.__groups[i]:
                return True

        return False

    def get_valency(self, element):
        """
        Get an element's valency.

        Args:
            element: the element whose valency should be returned
        """
        for n_grp in self.__groups:
            if element in self.__groups[n_grp]:
                return self.__group_valencies[n_grp]

    def get_nvalence_electrons(self, element):
        """
        Get number of valence electrons in an element.

        Args:
            element: the element whose number of valence electrons should be
                     returned.
        """
        if element == 'He':
            return 2

        for n_grp in self.__groups:
            if element in self.__groups[n_grp]:
                return self.__group_valence_electrons[n_grp]

    def get_group_elements(self, num):
        """
        Get elements in a given group number.

        Args:
            num: group number
        """
        return list(self.__groups[num].keys())

    def get_markersize(self, element):
        """
        Get an element's marker size for rendering purposes.

        Args:
            element: the element whose marker size should be returned
        """
        return self.__atomic_numbers[element] + 4

    def get_markercolor(self, element):
        """
        Get an element's marker color for rendering purposes.

        Args:
            element: the element whose marker color should be returned.
        """
        atomic_number = self.__atomic_numbers[element]
        temp = list(self.__atomic_colors[atomic_number - 1])
        color_list = []
        for rgb in temp:
            color_list.append(rgb / 255)

        return color_list


class Stats:
    def __init__(self, ca_dict, nca_dict):
        """
        Constructor.

        Args:
            ca_dict: dictionary of the form {"central atom": subscript}.
                     Rationale: allows for expansion to compounds with more
                                than one central atom.

            nca_dict: dictionary of the form {"non central atom": subscript}
        """
        pt = PeriodicTable()

        self.c_atom_dict = ca_dict
        self.c_atom = list(ca_dict.keys())[0]
        self.c_atom_sub = list(ca_dict.values())[0]
        self.c_atom_val = 0
        self.c_atom_nval_e = 0
        for c_atom in ca_dict:
            self.c_atom_val = pt.get_valency(c_atom)
            self.c_atom_nval_e = pt.get_nvalence_electrons(c_atom)
            break

        self.nc_atom_dict = nca_dict
        self.nc_atom = list(nca_dict.keys())[0]
        self.nc_atom_sub = list(nca_dict.values())[0]
        self.nc_atom_val = 0
        self.nc_atom_nval_e = 0
        for nc_atom in nca_dict:
            self.nc_atom_val = pt.get_valency(nc_atom)
            self.nc_atom_nval_e = pt.get_nvalence_electrons(nc_atom)
            self.print_statsnc_atom_nval_e = pt.get_nvalence_electrons(nc_atom)
            break

    # This exists for debugging purposes
    def print_stats(self):
        """Print compound stats."""
        print("=== CENTRAL ATOM ===")
        print("\tAtom:\t\t\t\t", self.c_atom)
        print("\tValency:\t\t\t", self.c_atom_val)
        print("\tNo. of valence electrons:\t", self.c_atom_nval_e)

        print()

        print("=== NON-CENTRAL ATOM(S) ===")
        print("\tAtom\t\t\t\t", self.nc_atom)
        print("\tValency:\t\t\t", self.nc_atom_val)
        print("\tNo. of valence electrons:\t", self.nc_atom_nval_e)


pt = PeriodicTable()
