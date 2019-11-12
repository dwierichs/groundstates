from django.db import models

from groundstates.settings import (
    _graph_geometry_CHOICES,
    _graph_dim_MAX,
    )

class Graph(models.Model):
    geometry = models.CharField( max_length=40, verbose_name='type', choices=_graph_geometry_CHOICES )
    dim = models.IntegerField( verbose_name='dimension', choices=[(i,i) for i in range(_graph_dim_MAX+1)] )
    pbc = models.IntegerField( verbose_name='periodic boundary conditions', choices=[(i,i) for i in range(int(2**_graph_dim_MAX))] )


class System(models.Model):
    name = models.CharField( max_length=80, verbose_name='name' )
    description = models.TextField( default=None, verbose_name='description' )
    H = models.TextField(verbose_name='Hamiltonian')
    n_par = models.IntegerField( verbose_name='number of parameters' )
    wikilink = models.CharField( max_length=100, verbose_name='Wikipedia link' )
    #data = MEDIAFIELD?
    contributors = models.TextField( default=None, verbose_name='contributors' )

    graph = models.ForeignKey( Graph, on_delete=models.CASCADE, verbose_name='graph' ) # on_delete to be modified! #%#

    def save(self):
        super().save()


class Energy(models.Model):
    value = models.DecimalField( max_digits=14, decimal_places=10, verbose_name='energy' )
    abs_error = models.DecimalField( max_digits=14, decimal_places=10, default=None, blank=True, verbose_name='absolute deviation' )
    rel_error = models.DecimalField( max_digits=9, decimal_places=8, default=None, blank=True, verbose_name='relative deviation' )
    method = models.CharField( max_length=70, verbose_name='computational method' )
    codelink = models.CharField( max_length=140, verbose_name='code repository' )
    references = models.TextField( verbose_name='references' )

    system = models.ForeignKey( System, on_delete=models.CASCADE, verbose_name='system' )

    def save(self, *args, **kwargs):
        if self.rel_error is None:
            if self.abs_error is not None:
                self.rel_error = self.abs_error/abs(self.value)
            else: # is this the convention we want? What about entries with numerically exact solutions 
                  # (i.e. numerical evaluations of analytic solutions)#%#
                self.rel_error = 0.
                self.abs_error = 0.

        super().save(*args, **kwargs)


