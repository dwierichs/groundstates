from django.db import models
from polymorphic.models import PolymorphicModel as Poly
import re

from groundstates.settings import (
    _graph_geometry_CHOICES,
    _graph_dim_MAX,
    )

from .utils import list_references, external_link

class Graph(models.Model):
    geometry = models.CharField( max_length=40, verbose_name='type', choices=_graph_geometry_CHOICES )
    dim = models.IntegerField( verbose_name='dimension', choices=[(i,i) for i in range(_graph_dim_MAX+1)] )
    pbc = models.IntegerField( verbose_name='periodic boundary conditions', choices=[(i,i) for i in range(int(2**_graph_dim_MAX))] )
    def __str__(self):
        return f'{self.dim}D - {self.geometry}'


class SearchFlag(models.Model):
    flag = models.CharField( max_length=100, null=True, blank=True, verbose_name='search flag' )
    def __str__(self):
        return f'{self.flag}'


class System(models.Model):
    name = models.CharField( max_length=80, verbose_name='name' )
    description = models.TextField( default=None, verbose_name='description' )
    H = models.TextField( verbose_name='Hamiltonian' )
    n_par = models.IntegerField( verbose_name='number of parameters' )
    wikilink = models.CharField( max_length=100, null=True, blank=True, verbose_name='Wikipedia link' )
    #data = MEDIAFIELD?
    contributors = models.TextField( default=None, null=True, blank=True, verbose_name='contributors' )
    references = models.TextField( null=True, blank=True, verbose_name='references' )

    graph = models.ForeignKey( Graph, on_delete=models.CASCADE, verbose_name='graph' ) # on_delete to be modified! #%#
    search_flags = models.ManyToManyField( SearchFlag, verbose_name='search flags' )

    def save(self, *args, **kwargs):
        # Purify latex of Hamiltonian
        pure_H_0 = re.search(r'(?<=^\$).*(?=\$$)', self.H) # look for $'s in H
        pure_H_1 = re.search(r'(?<=^\\\[).*(?=\\\]$)', self.H) # look for \['s in H
        if pure_H_0 is not None:
            self.H = pure_H_0.group(0)
        elif pure_H_1 is not None:
            self.H = pure_H_1.group(0)

        # Purify links:
        self.wikilink = external_link(self.wikilink)
        super().save(*args, **kwargs)


class Literature(models.Model):
    title = models.CharField( max_length=250, verbose_name='title' )
    authors = models.TextField( null=True, blank=True, verbose_name='authors' )
    link = models.CharField( max_length=150, verbose_name='link' )

    year = models.IntegerField( null=True, blank=True, verbose_name='year' )
    journal = models.CharField( max_length=100, null=True, blank=True, verbose_name='journal' )
    comment = models.TextField( null=True, blank=True, verbose_name='comment' )
    bibtex = models.TextField( null=True, blank=True, verbose_name='BibTex entry' )


class Energy(Poly):
    value = models.DecimalField( max_digits=14, decimal_places=10, verbose_name='energy' )
    system = models.ForeignKey( System, on_delete=models.CASCADE, verbose_name='system' )
    abs_error = models.DecimalField( max_digits=14, decimal_places=10, null=True, blank=True, verbose_name='absolute error' )
    rel_error = models.DecimalField( max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='relative error' )
    codelink = models.CharField( max_length=140, null=True, blank=True, verbose_name='code repository' )
    references = models.TextField( null=True, blank=True, verbose_name='references' )
    references2 = models.ManyToManyField( Literature, verbose_name='references' )

    def get_params(self):
        return [
            ('Energy', self.value, 4),
            ('Abs. Error', self.abs_error, 4),
            ]

    def save(self, *args, **kwargs):
        if self.rel_error in [None, 0.]:
            if self.abs_error not in [None, 0.]:
                self.rel_error = self.abs_error/abs(self.value)
        elif self.abs_error in [None, 0.]:
            self.abs_error = self.rel_error*abs(self.value)
        if self.references:
            self.references = '\n'.join([external_link(reflink) for reflink in self.references.split('\n')])
        super().save(*args, **kwargs)

