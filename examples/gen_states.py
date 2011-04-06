#! /usr/bin/env python

from jinja2 import Environment, FileSystemLoader

from json import load

states = []
element_data = load(open("../dftdata.json"))
for Z in range(1, 93):
    Z = str(Z)
    conf = element_data[Z]["configuration"]
    ks_energies = element_data[Z]["DFT data"]["neutral"]["LDA"]["ks_energies"]
    len_n = len(conf["n"])
    assert len(ks_energies) == len_n
    states.append({
        "Z" : Z,
        "len_n" : len_n,
        "n" : conf["n"],
        "l" : conf["l"],
        "f" : conf["f"],
        "ks_energies": ks_energies
        })

print "Generating the Fortran file..."
template = "states_tpl.f90"
env = Environment(loader=FileSystemLoader('.'))
t = env.get_template(template)
open("states.f90", "w").write(t.render({
    "states": states
    }))
