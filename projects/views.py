from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project, Review
from .forms import ProjectForm, ReviewForm
from .utils import search_project, custom_range_paginator



def projects(request):
    query_search=''
    send_mail('test','hello this is test','devsearchmail.gmail.com',
                    ['benyamin.az@hotmail.com'], fail_silently=False)
    if request.GET.get('query_search') :
        query_search=request.GET.get('query_search')
        projects=search_project(query_search)
    else:
        projects=Project.objects.prefetch_related('tags')\
                            .select_related('owner__user')
    custom_range, projects=custom_range_paginator(request,projects,3)
    context={'projects':projects, 'query_search':query_search,'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request,pk):
    project=get_object_or_404(Project.objects.prefetch_related('tags')\
                                            .select_related('owner__user'),pk=pk)
    reviews=Review.objects.filter(project_id=project.id).select_related('owner__user')
    form=ReviewForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login_page')
        profile=request.user.profile
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.project=project
            review.owner=profile
            if review.owner == project.owner :
                messages.error(request, 'You can not vote your own work!')
                return redirect('project', project.id)
            review.save()
            project.getVoteCount
            messages.success(request,'Your Review was successfully submitted!')
            return redirect('project', pk=project.id)
    context={'project':project,'form':form,'reviews':reviews}
    return render(request, 'projects/single_project.html', context)


@login_required(login_url='login_page')
def create_project(request):
    form=ProjectForm()
    if request.method == 'POST':
        form=ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=request.user.profile
            project.save()
            return redirect('projects')
    context={'form':form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login_page')
def update_project(request, pk):
    user_profile=request.user.profile
    project=get_object_or_404(user_profile.project_set, pk=pk)
    form=ProjectForm(instance=project)
    if request.method == 'POST':
        form=ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context={'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login_page')
def delete_project(request, pk):
    user_profile=request.user.profile
    project=get_object_or_404(user_profile.project_set, pk=pk)
    if request.method == 'POST': 
        project.delete()
        return redirect('user_account')
    context={'object':project}
    return render(request, 'delete_template.html', context)
