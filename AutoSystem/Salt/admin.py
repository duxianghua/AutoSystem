from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Salt_info)
admin.site.register(Module)
admin.site.register(Command)