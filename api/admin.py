from django.contrib import admin
from .models import Parent, Child, Household, Invitation

admin.site.register(Parent)
admin.site.register(Child)    
admin.site.register(Household)
admin.site.register(Invitation) 
