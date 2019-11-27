import re
import urllib.request as req
from bs4 import BeautifulSoup
import requests

def link_to_name(reflink):
    # arxiv: strip number
    if 'arxiv' in reflink:
        name = re.search(r'(?<=arxiv.org/[abspdf]{3}/)\d+\.*\d+', reflink).group(0)
    elif 'github.com' in reflink:
        name = 'GitHub/'+re.search(r'(?<=github.com/)\w+', reflink).group(0)
    else:
        name = reflink

    return name
    

def list_references(refs):
    if refs is None:
        return []
    else:
        return [(ref, link_to_name(ref),) for ref in refs.split('\n')]


def external_link(link):
    if link[:7]=='http://':
        return link
    elif link[:8]=='https://':
        return link
    else:
        return 'http://' + link

    
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
        bibtex = requests.get(f'http://dx.doi.org/{soup.doi.string}', headers=headers).content.lstrip()
    else:
        authors = [auth.string for auth in soup.find_all('name') if auth.parent.name=='author']
        title = [title.string for title in soup.find_all('title') if title.parent.name=='entry'][0]
        year = ('20' if int(arx_id[:2])<25 else '19')+arx_id[:2]
        month = arx_id[2:4]
        cl = soup.primary_category['term']
        author = ' and '.join([f'{{{auth.split(" ")[-1]}}}'+', '+' '.join(auth.split(' ')[:-1]) for auth in authors])
        flag = '_'.join([auth.split(' ')[-1] for auth in authors[:2]]+[year])
        bibtex = f'''@article{{{flag},
    author = {{{author}}},
    title = {{{title}}},
    year = {{{year}}},
    month = {{{month}}},
    prefix = {{arXiv}},
    preprint = {{{arx_id}}},
    class = {{{cl}}}
}}'''
    return bibtex



