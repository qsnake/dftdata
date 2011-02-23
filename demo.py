#! /usr/bin/env python

from json import load

f = open("dftdata.json")
element_data = load(f)

Hartree2eV = 27.21138
eV2kJpmol = 0.01036427
t = []
for Z in range(2, 93):
    approx = "LSD"
    Z = str(Z)
    E = float(element_data[Z]["DFT data"]["cation"][approx]["Etot"]) - \
            float(element_data[Z]["DFT data"]["neutral"][approx]["Etot"])
    t.append((Z, E))
t.sort(key=lambda x: x[1])
t.reverse()
print "Ionization energies in eV"
for n, (Z, E) in enumerate(t):
    symbol = element_data[Z]["symbol"]
    print "%2d %2s %9.6f" % (n+1, symbol, E * Hartree2eV)
