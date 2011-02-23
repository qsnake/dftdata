#! /usr/bin/env python

"""

NIST DFT Data obtained from:

http://physics.nist.gov/PhysRefData/DFTdata/
"""

from glob import glob
from json import dump

_symbols = ["H",  "He", "Li", "Be", "B",  "C",  "N",  "O",  "F", "Ne",
        "Na", "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar", "K", "Ca",
        "Sc", "Ti", "V",  "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
        "Sb", "Te", "I",  "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
        "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
        "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
        "Pa", "U",  "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
        "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
        "Rg", "Uub", "Uut", "Uuq", "Uup", "Uuh", "Uus", "UUo"]

element_data = {
        }
for Z in range(1, 93):
    symbol = _symbols[Z-1]
    element_data[Z] = {
            "atomic number": Z,
            "symbol": symbol,
            "DFT data": {
                "cation": {},
                "neutral": {},
                }
        }

for approx in ["LDA", "LSD", "RLDA", "ScRLDA"]:
    for Z in range(1, 93):
        for ion in ["neutral", "cation"]:
            if Z == 1 and ion == "cation":
                continue
            g = approx + "/" + ion + "s/" + "%02d" % Z + "*"
            name, = glob(g)
            f = open(name)
            Etot = f.readline().split("=")[1].strip()
            Ekin = f.readline().split("=")[1].strip()
            Ecoul = f.readline().split("=")[1].strip()
            Eenuc = f.readline().split("=")[1].strip()
            Exc = f.readline().split("=")[1].strip()
            item = {
                    "Etot": Etot,
                    "Ekin": Ekin,
                    "Ecoul": Ecoul,
                    "Eenuc": Eenuc,
                    "Exc": Exc,
                }
            element_data[Z]["DFT data"][ion][approx] = item

f = open("dftdata.json", "w")
dump(element_data, f)
