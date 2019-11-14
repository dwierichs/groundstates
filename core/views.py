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
        system = self.get_object()
        system.references = list_references(system.references)

        energies = system.energy_set.order_by('value')
        params = [tup[0] for tup in energies[0].get_params()]

        for e in energies:
            e.references = list_references(e.references)
            e.pars = [tup[1] for tup in e.get_params()]

        context = super(DetailView, self).get_context_data(**kwargs)
        context['energies'] = energies
        context['params'] = params
        return context



