from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
    )
from django.db.models import Q

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

        energies = system.energy_set.order_by('value')

        code_exists = False
        for e in energies:
            if e.codelink:
                e.codelink = list_references(e.codelink)
                code_exists = True
            e.pars = [tup[1:] for tup in e.get_params()]
            e.references = list_references(e.references)

        params = [tup[0] for tup in energies.first().get_params()]

        energy_refs = energies.first().references2.all()
        for e in energies[1:]:
            energy_refs = energy_refs.union(e.references2.all())

        context = super(DetailView, self).get_context_data(**kwargs)
        context['theres_code'] = code_exists
        context['energies'] = energies
        context['params'] = params
        context['energy_refs'] = energy_refs
        context['sys_refs'] = list_references(system.references)

        return context

