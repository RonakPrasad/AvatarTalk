from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectProperties)
admin.site.register(Avatars)
admin.site.register(Voices)
admin.site.register(ProjectVideo)