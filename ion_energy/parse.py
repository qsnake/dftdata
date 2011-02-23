from json import dump

def trim(s, v):
    i = s.find(v)
    s = s[i+len(v):]
    return s

s = open("orig.html").read()
s = s.replace("&nbsp;", "")
energies = {}
for Z in range(1, 105):
    s = trim(s, '<TR VALIGN="baseline">')
    s = trim(s, '<TD ALIGN="RIGHT">')
    _Z = int(s[:s.find("<")])
    assert _Z == Z
    if Z == 85:
        E = ""
    else:
        s = trim(s, '<TD ALIGN="right">')
        E = (s[:s.find("<")]).strip()
        E = E.replace("?", "")
    energies[Z] = E

f = open("ion_energies.json", "w")
dump(energies, f)
