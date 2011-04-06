#! /usr/bin/env python

"""

NIST DFT Data obtained from:

http://physics.nist.gov/PhysRefData/DFTdata/
"""

from glob import glob
from json import dump

def convert_conf(c):
    states = []
    l_names = ["s", "p", "d", "f"]
    for state in c:
        n = int(state[0])
        l = l_names.index(state[1])
        assert state[2] == "^"
        f = int(state[3:])
        states.append((n, l, f))
    states.sort(key=lambda x: x[0])
    n = [x[0] for x in states]
    l = [x[1] for x in states]
    f = [x[2] for x in states]
    return n, l, f

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
            "configuration": "",
            "DFT data": {
                "cation": {},
                "neutral": {},
                }
        }

conf = open("configurations").readlines()[13:]

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
            ks_energies = []
            while True:
                state = f.readline().split()
                if len(state) == 0:
                    break
                assert len(state) == 2
                E = state[1]
                ks_energies.append(E)
            item = {
                    "Etot": Etot,
                    "Ekin": Ekin,
                    "Ecoul": Ecoul,
                    "Eenuc": Eenuc,
                    "Exc": Exc,
                    "ks_energies": ks_energies
                }
            element_data[Z]["DFT data"][ion][approx] = item

            if ion == "neutral" and approx == "LDA":
                configuration = conf[Z-1]
                configuration = configuration.split("  ")[6].strip().split()
                if configuration[0].startswith("["):
                    base = configuration[0]
                    base = base[1:-1]
                    base_Z = _symbols.index(base) + 1
                    base_configuration = element_data[base_Z]["configuration"]
                    configuration = base_configuration + configuration[1:]
                element_data[Z]["configuration"] = configuration

for Z in range(1, 93):
    n, l, f = convert_conf(element_data[Z]["configuration"])
    element_data[Z]["configuration"] = dict(n=n, l=l, f=f)

f = open("dftdata.json", "w")
dump(element_data, f)
