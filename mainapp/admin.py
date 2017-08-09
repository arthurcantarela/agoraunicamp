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

class ProposalInline(admin.TabularInline):
    model = Proposal
    can_delete = True

class ProposalQuestionAdmin(admin.ModelAdmin):
    inlines = (ProposalInline, )

class CommentInline(admin.TabularInline):
    model = Comment
    can_delete = True

class DebateAdmin(admin.ModelAdmin):
    inlines = (CommentInline, )

class ReplyInline(admin.TabularInline):
    model = Reply
    can_delete = True

class CommentAdmin(admin.ModelAdmin):
    inlines = (ReplyInline, )

admin.site.unregister(AuthUser)
admin.site.register(AuthUser, AuthUserAdmin)

admin.site.register(Project)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(ProposalQuestion, ProposalQuestionAdmin)
admin.site.register(Question)
admin.site.register(Debate, DebateAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentHistory)
admin.site.register(Article)
