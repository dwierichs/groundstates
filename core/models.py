from django.db import models
from polymorphic.models import PolymorphicModel as Poly

from groundstates.settings import (
    _graph_geometry_CHOICES,
    _graph_dim_MAX,
    )

class Graph(models.Model):
    geometry = models.CharField( max_length=40, verbose_name='type', choices=_graph_geometry_CHOICES )
    dim = models.IntegerField( verbose_name='dimension', choices=[(i,i) for i in range(_graph_dim_MAX+1)] )
    pbc = models.IntegerField( verbose_name='periodic boundary conditions', choices=[(i,i) for i in range(int(2**_graph_dim_MAX))] )
    def __str__(self):
        return f'{self.dim}D - {self.geometry}'


class System(models.Model):
    name = models.CharField( max_length=80, verbose_name='name' )
    description = models.TextField( default=None, verbose_name='description' )
    H = models.TextField(verbose_name='Hamiltonian')
    n_par = models.IntegerField( verbose_name='number of parameters' )
    wikilink = models.CharField( max_length=100, null=True, blank=True, verbose_name='Wikipedia link' )
    #data = MEDIAFIELD?
    contributors = models.TextField( default=None, null=True, blank=True, verbose_name='contributors' )

    graph = models.ForeignKey( Graph, on_delete=models.CASCADE, verbose_name='graph' ) # on_delete to be modified! #%#

    def save(self):
        super().save()


class Energy(Poly):

    value = models.DecimalField( max_digits=14, decimal_places=10 )
    system = models.ForeignKey( System, on_delete=models.CASCADE )
    abs_error = models.DecimalField( default=0., max_digits=14, decimal_places=10 )
    rel_error = models.DecimalField( default=0., max_digits=10, decimal_places=7 )

    def get_params(self):
        return [
            ('Energy', self.value,),
            ('Abs. Error', self.abs_error,),
            ]
