from django.contrib import admin
from .models import Project, Review, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields=['title__istartswith']
    autocomplete_fields=['owner']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields=['project','owner']
    list_display=['project','created']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass