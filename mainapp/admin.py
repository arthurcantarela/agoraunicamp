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

class AnswerInline(admin.TabularInline):
    model = Answer
    can_delete = True

class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline, )

admin.site.unregister(AuthUser)
admin.site.register(AuthUser, AuthUserAdmin)

admin.site.register(Project)
admin.site.register(Question, QuestionAdmin)
