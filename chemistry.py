# chemistry.py: The Chemistry module for CSG

#
#   Copyright (C) 2020 Jithin Renji, Kannan MD, Pranav Pujar
#
#   This file is part of CSG
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
    def __init__(self):
        self.groups = {
            1:  {'H': 1, 'Li': 3, 'Na': 11, 'K': 19, 'Rb': 37, 'Cs': 55, 'Fr': 87},
            2:  {'Be': 4, 'Mg': 12, 'Ca': 20, 'Sr': 38, 'Ba': 56, 'Ra': 88},
            13: {'B': 5,  'Al': 13, 'Ga': 31, 'In': 49, 'Ti': 81},
            14: {'C': 6,  'Si': 14, 'Ge': 32, 'Sn': 50, 'Pb': 82},
            15: {'N': 7,  'P': 15,  'As': 33, 'Sb': 51, 'Bi': 83},
            16: {'O': 8,  'S': 16,  'Se': 34, 'Te': 52, 'Po': 84},
            17: {'F': 9,  'Cl': 17, 'Br': 35, 'I': 53,  'At': 85},
            18: {'He': 2, 'Ne': 10, 'Ar': 18, 'Kr': 36, 'Xe': 54, 'Rn': 86}
        }
        
        self.group_valencies = {
            1:  1,
            2:  2,
            13: 3,
            14: 4,
            15: 3,
            16: 2,
            17: 1,
            18: 0
        }
        
        self.group_valence_electrons = {
            1: 1,
            2: 2,
            13: 3,
            14: 4,
            15: 5,
            16: 6,
            17: 7,
            18: 8
        }
        
    def get_valency(self, element):
        for n_grp in self.groups:
            if element in self.groups[n_grp]:
                return self.group_valencies[n_grp]
                
    def get_nvalence_electrons(self, element):
        if element == 'He':
            return 2

        for n_grp in self.groups:
            if element in self.groups[n_grp]:
                return self.group_valence_electrons[n_grp]
    
    def get_group_elements(self, num):
        return list(self.groups[num].keys())

class Stats:
    def __init__(self, ca, nca_dict):
        pt = PeriodicTable()
        self.c_atom = ca
        self.c_atom_val = pt.get_valency(ca)
        self.c_atom_nval_e = pt.get_nvalence_electrons(ca)
        
        self.nc_atom_dict = nca_dict
        self.nc_atom_val_list = []
        self.nc_atom_nval_e_list = []
        
        for el in nca_dict:
            self.nc_atom_val_list.append(pt.get_valency(el))
            self.nc_atom_nval_e_list.append(pt.get_nvalence_electrons(el))        
    
    # This exists for debugging purposes
    def print_stats(self):
        print("=== CENTRAL ATOM ===")
        print("\tAtom:\t\t\t\t", self.c_atom)
        print("\tValency:\t\t\t", self.c_atom_val)
        print("\tNo. of valence electrons:\t", self.c_atom_nval_e)
    
        print()
        
        print("=== NON-CENTRAL ATOM(S) ===")
        print("\tAtom\t\t\t\t", self.nc_atom_dict)
        print("\tValency:\t\t\t", self.nc_atom_val_list)
        print("\tNo. of valence electrons:\t", self.nc_atom_nval_e_list)
