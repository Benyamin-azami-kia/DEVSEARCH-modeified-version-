from django.contrib import admin
from .models import Profile, Skill, Message


class SkillInline(admin.StackedInline):
    model=Skill
    autocomplete_fields=['owner']
    extra=0
    min_num=1


@admin.register(Message)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields=['sender','recipient']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields=['user']
    search_fields=['user__first_name__istartswith','user__last_name__istartswith']
    inlines=[SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    autocomplete_fields=['owner']
    search_fields=['name']