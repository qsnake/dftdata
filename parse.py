#! /usr/bin/env python

from glob import glob

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


approximations = ["LDA", "LSD", "RLDA", "ScRLDA"]

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

for approx in approximations:
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


Hartree2eV = 27.21138
eV2kJpmol = 0.01036427
t = []
for Z in range(2, 93):
    E = float(element_data[Z]["DFT data"]["cation"]["LDA"]["Etot"]) - \
            float(element_data[Z]["DFT data"]["neutral"]["LDA"]["Etot"])
    t.append((Z, E))
t.sort(key=lambda x: x[1])
t.reverse()
for n, (Z, E) in enumerate(t):
    symbol = element_data[Z]["symbol"]
    print "%2d %2s %9.6f" % (n+1, symbol, E * Hartree2eV / eV2kJpmol)
