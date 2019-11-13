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

    
class HomeView(ListView):
    model = System
    template_name = 'core/home.html'
    context_object_name = 'systems'
    order_by = 'name'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['msgs'] = Message.objects.order_by('-date_mod')
        return context


class SystemDetailView(DetailView):
    template_name = 'core/system_detail.html'
    model = System

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        energies_tmp = self.get_object().energy_set.all()
        energies = [[tup[1] for tup in e.get_params()] for e in energies_tmp]
        params = [tup[0] for tup in energies_tmp[0].get_params()]
        #e_type = [cls for cls in _AUTO_REGISTER if isinstance(energies[0], cls)]
        #refs = [r for e in energies for r in e.references.split('\n')]
        #refnames = refs # Here we can automatically generate a better name (e.g. the arxiv handle or such things) #%#
        #context['refs'] = [(refs[i],refnames[i],) for i in range(len(refs))]
        context['energies'] = energies
        context['params'] = params
        return context



