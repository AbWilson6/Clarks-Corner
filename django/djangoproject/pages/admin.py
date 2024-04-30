from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Shopping_User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("username", "password",     
                       "clark_email"),
        },
    ),
)

admin.site.register(Shopping_User, CustomUserAdmin)

# from .models import Shopping_User

# admin.site.register(Shopping_User)

from .models import Review

admin.site.register(Review)

from .models import Product

admin.site.register(Product)

from .models import has_in_cart

admin.site.register(has_in_cart)

from .models import Receipt

admin.site.register(Receipt)