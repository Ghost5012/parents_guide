from django.contrib import admin

from .models import Parent, Driver, Bus

# Register your models here.
admin.site.register([Bus, Driver, Parent])
# admin.site.register(Driver)
