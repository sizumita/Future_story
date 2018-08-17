from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AuthUser)
admin.site.register(Profile)
admin.site.register(Entry)
admin.site.register(Story)
admin.site.register(Write_Entry)
admin.site.register(Evaluation)
admin.site.register(Comment)
