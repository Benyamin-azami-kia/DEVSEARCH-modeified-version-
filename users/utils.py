from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage

def search_profile(query_search):
    profiles=Profile.objects.distinct().select_related('user')\
                            .prefetch_related('skill_set')\
                            .filter(Q(user__first_name__istartswith=query_search) | 
                                    Q(user__last_name__istartswith=query_search) |
                                    Q(skill__in=Skill.objects.filter(name__icontains=query_search)))
    return profiles

def custom_range_paginator(request, profiles, result):
    page=request.GET.get('page')
    paginator=Paginator(profiles, result)
    try:
        profiles=paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        profiles=paginator.page(page)

    left_index=(int(page) - 1)
    if left_index < 1:
        left_index = 1
    right_indext=(int(page) + 5)
    if right_indext > paginator.num_pages:
        right_indext = paginator.num_pages + 1
    custom_range=range(left_index,right_indext)
    return custom_range, profiles