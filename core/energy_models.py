from django.db import models

from .models import Energy


class Energy_TFI(Energy):
    h = models.DecimalField( max_digits=8, decimal_places=3, verbose_name='h' )
    J = models.DecimalField( max_digits=8, decimal_places=3, verbose_name='J' )
    n_par = None

    def save(self, *args, **kwargs):
        self.n_par = len(self.__dict__)-len(super().__dict__)
        self.n_par = 1
        super().save(*args, **kwargs)

# Always add newly added energy models to the following list in order to have it registered in admin.py
_AUTO_REGISTER = [
    Energy_TFI,
    ]
