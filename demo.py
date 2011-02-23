#! /usr/bin/env python

from json import load

element_data = load(open("dftdata.json"))
ion_energies = load(open("ion_energy/ion_energies.json"))

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
print "n symbol E_dft E_exp"
for n, (Z, E) in enumerate(t):
    symbol = element_data[Z]["symbol"]
    E_exp = ion_energies[str(Z)]
    print "%2d %2s %9.6f %s" % (n+1, symbol, E * Hartree2eV, E_exp)
