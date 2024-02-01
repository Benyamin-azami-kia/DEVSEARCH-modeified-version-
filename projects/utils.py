from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage


def search_project(query_search):
    projects=Project.objects.distinct().filter(Q(title__icontains=query_search) |
                                Q(description__icontains=query_search)|
                                Q(owner__user__first_name__icontains=query_search) |
                                Q(tags__in=Tag.objects.filter(name__icontains=query_search)))\
                                .select_related('owner__user').prefetch_related('tags')
    return projects

def custom_range_paginator(request, projects, result):
    page=request.GET.get('page')
    paginator=Paginator(projects, result)
    try:
        projects=paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        projects=paginator.page(page)

    left_index=(int(page) - 1)
    if left_index < 1:
        left_index = 1
    right_indext=(int(page) + 5)
    if right_indext > paginator.num_pages:
        right_indext = paginator.num_pages + 1
    custom_range=range(left_index,right_indext)
    return custom_range, projects