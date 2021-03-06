from django.db import models
from polymorphic.models import PolymorphicModel as Poly
import re

from groundstates.settings import (
    _graph_geometry_CHOICES,
    _graph_dim_MAX,
    )

from .utils import (
    list_references, 
    external_link, 
    link_to_name,
    arxiv_to_bibtex,
    automatic_search_flags,
    )


class Graph(models.Model):
    geometry = models.CharField( max_length=40, verbose_name='type', choices=_graph_geometry_CHOICES )
    dim = models.IntegerField( verbose_name='dimension', choices=[(i,i) for i in range(_graph_dim_MAX+1)] )
    pbc = models.IntegerField( verbose_name='periodic boundary conditions', choices=[(i,i) for i in range(int(2**_graph_dim_MAX))] )
    def __str__(self):
        return f'{self.dim}D - {self.geometry}'


class SearchFlag(models.Model):
    flag = models.CharField( max_length=100, verbose_name='search flag' )

    def __str__(self):
        return f'{self.flag}'

    def save(self, *args, **kwargs):
        self.flag = self.flag.lower()
        super().save(*args, **kwargs)


class Literature(models.Model):
    link = models.CharField( max_length=150, verbose_name='link' )
    title = models.CharField( max_length=250, null=True, blank=True, verbose_name='title' )
    authors = models.TextField( null=True, blank=True, verbose_name='authors' )

    year = models.IntegerField( null=True, blank=True, verbose_name='year' )
    journal = models.CharField( max_length=100, null=True, blank=True, verbose_name='journal' )
    comment = models.TextField( null=True, blank=True, verbose_name='comment' )
    bibtex = models.TextField( null=True, blank=True, verbose_name='BibTex entry' )
    disp_name = models.CharField( max_length=150, null=True, blank=True, verbose_name='displayed name' )

    def save(self, *args, **kwargs):

        # Cover the case of only id being provided in link
        arx_id = re.search(r'^\d+\.*\d+$', self.link)
        if 'arxiv.org' in self.link or arx_id:
            if arx_id: # There is only an id given
                bibtex_scr, title_scr, authors_scr = arxiv_to_bibtex(arx_id.group(0))
            else: # There is an arxiv.org link given
                bibtex_scr, title_scr, authors_scr = arxiv_to_bibtex(self.link)
            if not self.title:
                self.title = title_scr
            if not self.authors:
                self.authors = authors_scr.replace(' and ', '; ').replace('{', '').replace('}', '')
            if not self.bibtex:
                self.bibtex = bibtex_scr
        else:
            assert self.title is not None, f'Title is required if the link does not point to arxiv.\nProvided link: {self.link}'

        self.link = external_link(self.link)
        if not self.disp_name:
            self.disp_name = link_to_name(self.link)
        super().save(*args, **kwargs)


class System(models.Model):
    name = models.CharField( max_length=80, verbose_name='name' )
    description = models.TextField( default=None, verbose_name='description' )
    H = models.TextField( verbose_name='Hamiltonian' )
    n_par = models.IntegerField( verbose_name='number of parameters' )
    wikilink = models.CharField( max_length=100, null=True, blank=True, verbose_name='Wikipedia link' )
    #data = MEDIAFIELD?
    contributors = models.TextField( default=None, null=True, blank=True, verbose_name='contributors' )
    references = models.ManyToManyField( Literature, verbose_name='references' )

    graph = models.ForeignKey( Graph, on_delete=models.CASCADE, verbose_name='graph' ) # on_delete to be modified! #%#
    search_flags = models.ManyToManyField( SearchFlag, verbose_name='search flags' )

    def save(self, *args, **kwargs):
        # Purify latex of Hamiltonian - This should be done a bit nicer at some point
        pure_H_0 = re.search(r'(?<=^\$).*(?=\$$)', self.H) # look for $'s in H
        pure_H_1 = re.search(r'(?<=^\\\[).*(?=\\\]$)', self.H) # look for \['s in H
        if pure_H_0 is not None:
            self.H = pure_H_0.group(0)
        elif pure_H_1 is not None:
            self.H = pure_H_1.group(0)

        # Purify links:
        if self.wikilink:
            self.wikilink = external_link(self.wikilink)
        super().save(*args, **kwargs)
        for flag in automatic_search_flags(self):
            SF = SearchFlag(flag=flag)
            SF.save()
            self.search_flags.add(SF)


class Energy(Poly):
    value = models.DecimalField( max_digits=14, decimal_places=10, verbose_name='energy' )
    system = models.ForeignKey( System, on_delete=models.CASCADE, verbose_name='system' )
    abs_error = models.DecimalField( max_digits=14, decimal_places=10, null=True, blank=True, verbose_name='absolute error' )
    rel_error = models.DecimalField( max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='relative error' )
    codelink = models.CharField( max_length=140, null=True, blank=True, verbose_name='code repository' )
    references = models.ManyToManyField( Literature, verbose_name='references' )

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
        if self.codelink:
            self.codelink = external_link(self.codelink)
        super().save(*args, **kwargs)

