from django.contrib import admin
from .models import Todo, Profile

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date_time',)

# Register your models here.
admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile)
