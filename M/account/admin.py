from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User, OtpCode, Profile, Relation


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created')
    raw_id_fields = ('from_user','to_user')


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'phone_number', 'created')
    list_filter = ('created',)
    search_fields = ('code',)
    ordering = ('created',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'email', 'full_name', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
    (None, {'fields':('phone_number', 'email', 'full_name', 'password')}),
    ('Permissions', {'fields':('is_admin','is_active', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'full_name', 'password1', 'password2')}),
    )

    search_fields = ('email','full_name')
    ordering = ('email',)
    filter_horizontal = ()


class ProfileInline(admin.StackedInline):
    model = Profile

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.register(User, ExtendedUserAdmin)
admin.site.unregister(Group)





