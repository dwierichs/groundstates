from django.db import models

from .models import Energy


class Energy_TFI(Energy):
    
    h = models.DecimalField( max_digits=14, decimal_places=10 )
    J = models.DecimalField( default=0., max_digits=14, decimal_places=10 )

    def get_params(self):
        return super().get_params() + [
                                    ('h', self.h,),
                                    ('J', self.J,),
                                    ]

class Energy_XXX(Energy):
    
    J = models.DecimalField( max_digits=14, decimal_places=10 )

    def get_params(self):
        return super().get_params() + [
                                    ('J', self.J,),
                                    ]



# Always add newly added energy models to the following list in order to have it registered in admin.py
_AUTO_REGISTER = [
    Energy_TFI,
    Energy_XXX,
    ]
