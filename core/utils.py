
def link_to_name(reflink):

    return reflink
    
def list_references(refs):
    if refs is None:
        return []
    else:
        return [(ref, link_to_name(ref),) for ref in refs.split('\n')]

def external_link(link):
    if link[:7]=='http://':
        return link
    else:
        return 'http://' + link
    
