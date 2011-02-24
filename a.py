import datetime
from json import load
from google.appengine.ext import db
from google.appengine.api import users

class Energy(db.Model):
    Z = db.IntegerProperty()
    E = db.StringProperty()
    data_type = db.StringProperty()
    atom_type = db.StringProperty(choices=set(["cation", "neutral"]))
    calc_type = db.StringProperty(choices=set(["LSD", "LDA", "RLDA", "ScRLDA"]))
    energy_type = db.StringProperty(choices=set(["Etot", "Ekin", "Exc"]))

def fill():
    element_data = load(open("dftdata.json"))
    ion_energies = load(open("ion_energy/ion_energies.json"))
    for Z in range(2, 93):
        for atom_type in ["cation", "neutral"]:
            for calc_type in ["LDA", "RLDA", "LSD", "ScRLDA"]:
                for energy_type in ["Etot", "Ekin", "Exc"]:
                    data_type="DFT data"
                    E = element_data[str(Z)][data_type][atom_type][calc_type][energy_type]
                    e = Energy(Z=Z,
                            E=E,
                            data_type=data_type,
                            atom_type=atom_type,
                            calc_type=calc_type,
                            energy_type=energy_type)
                    e.put()

def show():
    q = Energy.all()
    q.filter("atom_type", "neutral")
    q.filter("energy_type", "Etot")
    q.filter("calc_type", "LSD")

    results = q.fetch(200)
    print len(results)
    for p in results:
        print p.Z, p.E, p.data_type, p.atom_type, p.calc_type, p.energy_type

if __name__ == "__main__":
    print "Start"
    fill()
    show()
    print "Stop"
