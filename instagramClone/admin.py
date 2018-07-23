from django.contrib import admin

# Register your models here.
from .models import Profile,Image,Comments


# Register your models here.
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Comments)