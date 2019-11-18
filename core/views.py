from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
    )

from .models import (
    Graph,
    System,
    #Energy,
    )
from .energy_models import *
from .energy_models import _AUTO_REGISTER
from users.models import (
    Message,
    )

from .utils import (
    list_references,
    link_to_name,
    )

class HomeView(ListView):
    model = System
    template_name = 'core/home.html'
    context_object_name = 'systems'
    order_by = 'name'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['msgs'] = Message.objects.order_by('-date_mod')
        return context


class SystemSearchView(ListView):
    model = System
    template_name = 'core/system_search_results.html'
    context_object_name = 'system_search_results' 
    query = ''
    
    def get_queryset(self):
        self.query = self.request.GET.get('q')
        object_list = System.objects.filter(search_flags__flag=self.query)
        return object_list    

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['query'] = self.query
        return context

class SystemDetailView(DetailView):
    template_name = 'core/system_detail.html'
    model = System

    def get_context_data(self, **kwargs):
        system = self.get_object()
        system.references = list_references(system.references)

        energies = system.energy_set.order_by('value')
        params = [tup[0] for tup in energies[0].get_params()]

        code_exists = False
        for e in energies:
            e.references = list_references(e.references)
            e.codelink = list_references(e.codelink)
            if e.codelink != []:
                code_exists = True
            e.pars = [tup[1:] for tup in e.get_params()]

        context = super(DetailView, self).get_context_data(**kwargs)
        context['theres_code'] = code_exists
        context['energies'] = energies
        context['params'] = params
        # New policy: collect all references attached to an energy and reference them in the table but 
        # actually put them below (or above) the table.
        all_energy_refs = []
        for e in energies:
            for ref, refname in e.references:
                if (ref, refname) not in all_energy_refs:
                    all_energy_refs.append( (ref,refname,len(all_energy_refs)) )
        for e in energies:
            e.references = [ref[2] for ref in all_energy_refs if (ref[0],ref[1]) in e.references]
        context['all_energy_refs'] = all_energy_refs
        return context



