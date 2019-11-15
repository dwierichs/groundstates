from django.contrib import admin
from .models import (
    Graph,
    SearchFlag,
    System,
    )

from .energy_models import *
from .energy_models import _AUTO_REGISTER

admin.site.register(System)
admin.site.register(Graph)
admin.site.register(SearchFlag)

for energy_model in _AUTO_REGISTER:
    admin.site.register(energy_model)



