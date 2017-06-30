from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as AuthUser
from .models import *

class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'users'

class AuthUserAdmin(BaseUserAdmin):
    inlines = (UserInline, )

class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = True

class ChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline, )

admin.site.unregister(AuthUser)
admin.site.register(AuthUser, AuthUserAdmin)

admin.site.register(Project)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
