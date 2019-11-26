import re

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
    
