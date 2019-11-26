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

from core.utils import link_to_name

admins = {'david':'123', 'thorben':'123'}
for name, pw in admins.items():
    user = User.objects.create_user(name,password=pw)
    user.is_superuser=True
    user.is_staff=True
    user.save()

graph = Graph(geometry='Hypercube', dim=1, pbc=1)
graph.save()

sf1 = SearchFlag(flag='tfi')
sf1.save()
sf2 = SearchFlag(flag='xxx')
sf2.save()

s1 = System(name='Transverse Field Ising Model', description='standard Ising model on a chain with PBC and transverse field h', H='J\sum^N_{i=1} Z_i Z_{i+1}+h\sum^N_{i=1} X_i', n_par=2, wikilink='en.wikipedia.org/wiki/Ising_model', contributors='system', graph=graph)
s1.save()
s1.search_flags.add(sf1)
s2 = System(name='Isotropic Heisenberg model (XXX)', description='Heisenberg model with isotropic coupling (XXX model) on a chain, without transverse field.', H='J\sum^N_{i=1} X_i X_{i+1}+Y_i Y_{i+1}+Z_i Z_{i+1}', n_par=2, wikilink='en.wikipedia.org/wiki/classical_heisenberg_model', contributors='system', graph=graph)
s2.save()
s2.search_flags.add(sf2)

l4_bibtex='@ARTICLE{2019PhRvL.123g0503C,\nauthor = {{Campbell}, Earl},\ntitle = "{Random Compiler for Fast Hamiltonian Simulation}",\nurnal = {\prl},\nwords = {Quantum Physics},\n year = "2019",\nmonth = "Aug",\nolume = {123},\number = {7},\n  eid = {070503},\npages = {070503},\n  doi = {10.1103/PhysRevLett.123.070503},\nrefix = {arXiv},\nprint = {1811.08017},\nClass = {quant-ph},\ndsurl = {https://ui.adsabs.harvard.edu/abs/2019PhRvL.123g0503C},\nsnote = {Provided by the SAO/NASA Astrophysics Data System}}'

l1 = Literature(title='Test titles are the first titles ever', authors='Wurst, Hans\nPiet', link='www.google.com')
l1.save()
l2 = Literature(title='There shall be a website with groundstates!', authors='Auch Immer, Wer\nWurst, Hans', link='www.arxiv.org/pdf/1405.05431.pdf')
l2.save()
l3 = Literature(title='Code should not be a reference but a codelink', authors='David', link='www.github.com/dwierichs/groundstates/\nwww.google.com')
l3.save()
l4 = Literature(title=link_to_name('https://arxiv.org/pdf/1811.08017.pdf'), authors='Someone', link='https://arxiv.org/pdf/1811.08017.pdf', bibtex=l4_bibtex)
l4.save()
l5 = Literature(title='Some stuff', authors='A person', link='https://arxiv.org/abs/1706.02998')
l5.save()

e1_1 = Energy_TFI(value=0.07, system=s1, abs_error=0.01, h=1., J=0.)
e1_2 = Energy_TFI(value=0.14, system=s1, rel_error=0.02, h=0., J=1., codelink='www.github.com/dwierichs/groundstates/')
e2_1 = Energy_XXX(value=0.05, system=s2, abs_error=0.01, J=0.)
e2_2 = Energy_XXX(value=0.10, system=s2, abs_error=0.02, J=1.)

e1_1.save()
e1_2.save()
e2_1.save()
e2_2.save()

e1_1.references.add(l1)
e1_2.references.add(l1,l2,l4)
e2_1.references.add(l1,l4)
e2_2.references.add(l2,l3)
s1.references.add(l5)

print(f'Initialization of new DB successful.')
