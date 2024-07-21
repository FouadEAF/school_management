# # users/admin.py
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User
# # from .forms import UserCreationForm, UserChangeForm


# class CustomUserAdmin(UserAdmin):
#     # add_form = UserCreationForm
#     # form = UserChangeForm
#     model = User
#     list_display = ['username', 'cnie', 'first_name',
#                     'last_name', 'email', 'is_staff', 'is_active']
#     list_filter = ['is_staff', 'is_active']
#     fieldsets = (
#         (None, {'fields': ('username', 'cnie', 'departement', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_staff',
#          'is_active', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'cnie', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
#          ),
#     )
#     search_fields = ('username', 'cnie',)
#     ordering = ('username',)


# admin.site.register(User, CustomUserAdmin)

# =========================================================================================
# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('cnie', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'cnie', 'password1', 'password2', 'role'),
        }),
    )
    list_display = ('username', 'cnie', 'is_staff')
    search_fields = ('username', 'cnie')
    ordering = ('username',)


admin.site.register(User, UserAdmin)
