from django.contrib import admin
from .models import AccessKey, CustomUser, Payment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AccessKey)
admin.site.register(Payment)


#The following environment is selected: ~\Desktop\micro-focus\.venv\Scripts\python.exe
