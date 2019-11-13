from django.contrib import admin
from .models import (
    Graph,
    System,
    )

from .energy_models import *
from .energy_models import _AUTO_REGISTER

admin.site.register(Graph)
admin.site.register(System)
for energy_model in _AUTO_REGISTER:
    admin.site.register(energy_model)

