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
def exp_key(x):
    e = ion_energies[str(x[0])]
    if e == "":
        return 0
    else:
        return float(e)

t.sort(key=exp_key)
t.reverse()
print "Ionization energies in eV"
print "n symbol E_dft E_exp error"
for n, (Z, E) in enumerate(t):
    symbol = element_data[Z]["symbol"]
    E_dft = E * Hartree2eV
    E_exp = ion_energies[str(Z)]
    if E_exp == "":
        error = 0
    else:
        error = abs(E_dft - float(E_exp))
    print "%2d %2s %9.6f %-7s %6.2e" % (n+1, symbol, E_dft, E_exp, error)
