from django.contrib import admin
from .models import User

# Register your models here.
try:
    admin.site.register(User)
except Exception:
    pass