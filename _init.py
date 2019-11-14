import os, sys
import subprocess as sub

db_name = 'db.sqlite3'

if os.path.isfile(db_name):
    os.remove(db_name)
    print(f'DB {db_name} deleted successfully')
else:
    print(f'Where is you DB with name {db_name}?')

sub_makemi = sub.run(['python3', 'manage.py', 'makemigrations'])
if sub_makemi.returncode != 0:
    print(f'Problem detected during execution of makemigrations')

sub_migrate = sub.run(['python3', 'manage.py', 'migrate'])
if sub_migrate.returncode != 0:
    print(f'Problem detected during execution of migrate')


from core.models import *
from core.energy_models import *
from django.contrib.auth.models import User


admins = {'david':'123', 'thorben':'123'}
for name, pw in admins.items():
    user = User.objects.create_user(name,password=pw)
    user.is_superuser=True
    user.is_staff=True
    user.save()

graph = Graph(geometry='Hypercube', dim=1, pbc=1)
graph.save()

s1 = System(name='Transverse Field Ising Model', description='standard Ising model on a chain with PBC and transverse field h', H='J\sum^N_{i=1} Z_i Z_{i+1}+h\sum^N_{i=1} X_i', n_par=2, wikilink='en.wikipedia.org/wiki/Ising_model', contributors='system', graph=graph)
s1.save()
s2 = System(name='Isotropic Heisenberg model (XXX)', description='Heisenberg model with isotropic coupling (XXX model) on a chain, without transverse field.', H='J\sum^N_{i=1} X_i X_{i+1}+Y_i Y_{i+1}+Z_i Z_{i+1}', n_par=2, wikilink='en.wikipedia.org/wiki/classical_heisenberg_model', contributors='system', graph=graph)
s2.save()

e1_1 = Energy_TFI(value=0.07, system=s1, abs_error=0.01, h=1., J=0., references='www.github.com/dwierichs/groundstates/\nwww.google.com')
e1_2 = Energy_TFI(value=0.14, system=s1, rel_error=0.02, h=0., J=1., codelink='www.github.com/dwierichs/groundstates/')
e2_1 = Energy_XXX(value=0.05, system=s2, abs_error=0.01, J=0.)
e2_2 = Energy_XXX(value=0.10, system=s2, abs_error=0.02, J=1.)

e1_1.save()
e1_2.save()
e2_1.save()
e2_2.save()
