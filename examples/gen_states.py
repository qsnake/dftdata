#! /usr/bin/env python

from jinja2 import Environment, FileSystemLoader

states = [{
    "Z" : 1,
    "len_n" : 3,
    "n" : [1, 2, 3],
    "l" : [1.5, 2, 3],
    "f" : [1.0, 2, 3],
    }, {
    "Z" : 2,
    "len_n" : 3,
    "n" : [1, 2, 3],
    "l" : [1.5, 2, 3],
    "f" : [1.0, 2, 3],
    }, {
    "Z" : 3,
    "len_n" : 3,
    "n" : [1, 2, 3],
    "l" : [1.5, 2, 3],
    "f" : [1.0, 2, 3],
    }]

print "Generating the Fortran file..."
template = "states_tpl.f90"
env = Environment(loader=FileSystemLoader('.'))
t = env.get_template(template)
open("states.f90", "w").write(t.render({
    "states": states
    }))
