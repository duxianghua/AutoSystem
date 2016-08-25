from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(area)
admin.site.register(app_category)
admin.site.register(hosts)
admin.site.register(projects)
admin.site.register(ec2_instances)
admin.site.register(project_hosts)
admin.site.register(app_cate_hosts)
