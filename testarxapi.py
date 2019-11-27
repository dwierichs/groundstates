import urllib.request as req
from pprint import pprint
from bs4 import BeautifulSoup
import re
import requests

def arxiv_to_bibtex(string):
    '''
    Takes either a full link or the id alone
    '''
    id1 = re.search(r'(?<=arxiv.org/[abspdf]{3}/)\d+\.*\d+', string)
    id2 = re.search(r'^\d+\.*\d+$', string)
    if id1:
        arx_id = id1.group(0)
    elif id2:
        arx_id = id2.group(0)
    else:
        raise ValueError('The given string does not lead to an arxiv paper')

    url = f'http://export.arxiv.org/api/query?id_list={arx_id}'
    data = req.urlopen(url).read()
    soup = BeautifulSoup(data, 'lxml-xml')
    if soup.journal_ref:
        headers = {
            'Accept': 'text/bibliography; style=bibtex',
        }
        bibtex = requests.get(f'http://dx.doi.org/{soup.doi.string}', headers=headers)
        print(bibtex.content.lstrip())
        #bibtex = soup.journal_ref.string
    else:
        authors = [auth.string for auth in soup.find_all('name') if auth.parent.name=='author']
        title = [title.string for title in soup.find_all('title') if title.parent.name=='entry'][0]
        year = ('20' if int(arx_id[:2])<25 else '19')+arx_id[:2]
        month = arx_id[2:4]
        cl = soup.primary_category['term']
        bibtex = f'''@article{{{authors[0]}_{authors[1]}_{year},
    author = {{{authors}}},
    title = {{{title}}},
    year = {{{year}}},
    month = {{{month}}},
    prefix = {{arXiv}},
    preprint = {{{arx_id}}},
    class = {{{cl}}}
}}'''
    return bibtex


for arx_id in ['1706.02998', '1911.11140']:
    #print(soup.prettify)
    #print(soup.journal_ref)
    print(arxiv_to_bibtex(arx_id))



