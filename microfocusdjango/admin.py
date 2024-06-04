from django.contrib import admin
from .models import AccessKey, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AccessKey)
