from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Area)
admin.site.register(group)
admin.site.register(Host)
admin.site.register(servers_info)
admin.site.register(AWS_INSTANCES)
admin.site.register(project)
admin.site.register(project_host)