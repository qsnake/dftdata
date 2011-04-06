#! /usr/bin/env python

from jinja2 import Environment, FileSystemLoader

from json import load

states = []
element_data = load(open("../dftdata.json"))
for Z in range(1, 93):
    Z = str(Z)
    conf = element_data[Z]["configuration"]
    ks_energies = element_data[Z]["DFT data"]["neutral"]["RLDA"]["ks_energies"]
    no = []
    lo = []
    so = []
    fo = []
    for n, l, f in zip(conf["n"], conf["l"], conf["f"]):
        if l == 0:
            spins = [1]
        else:
            spins = [0, 1]
        for s in spins:
            if s == 1:
                j = l + 0.5
            else:
                j = l - 0.5
            fn = 2*j+1
            fn_total = 2*(2*l+1)
            no.append(n)
            lo.append(l)
            so.append(s)
            fo.append(f*fn/fn_total)
    len_n = len(no)
    assert len(ks_energies) == len_n
    states.append({
        "Z" : Z,
        "len_n" : len_n,
        "n" : no,
        "l" : lo,
        "s" : so,
        "f" : fo,
        "ks_energies": ks_energies
        })

print "Generating the Fortran file..."
template = "states_rel_tpl.f90"
env = Environment(loader=FileSystemLoader('.'))
t = env.get_template(template)
open("states_rel.f90", "w").write(t.render({
    "states": states
    }))
