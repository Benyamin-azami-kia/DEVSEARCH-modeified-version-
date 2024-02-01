from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, UserEditForm, MessageForm
from .models import Profile, Skill, Message
from .utils import search_profile, custom_range_paginator


def profiles(request):
    query_search=''
    if request.GET.get('query_search'):
        query_search=request.GET.get('query_search')
        profiles=search_profile(query_search)
    else:
        profiles=Profile.objects.select_related('user').prefetch_related('skill_set').all()
    custom_range, profiles=custom_range_paginator(request, profiles,3)
    context={'profiles':profiles,'query_search':query_search,'custom_range':custom_range}
    return render(request,'users/index.html', context)

def profile(request, pk):
    try:
        profile=Profile.objects.select_related('user').prefetch_related('skill_set').get(pk=pk)
    except Profile.DoesNotExist:
        raise Http404()
    if profile.user_id == request.user.id:
        return redirect('user_account')
    projects=profile.project_set.prefetch_related('tags').all()
    context={'profile':profile,'projects':list(projects)}
    return render(request, 'users/user_profile.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request, username=username, password=password)

        if user != None:
            if user.is_active:
                login(request, user)
                messages.success(request,'You have logged in!')
                return redirect('profiles')
        else:
            messages.error(request,'Username or Password is incorrect!')
    context={'page':'login'}
    return render(request, 'users/login-register.html', context)

def user_register(request):
    form=CustomUserCreationForm()
    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            messages.success(request,'Account has been created!')
            return redirect('user_account')
    context={'page':'register','form':form}
    return render(request, 'users/login-register.html',context)

@login_required(login_url='login_page')
def logout_user(request):
    logout(request)
    messages.info(request,'You have logged out!')
    return redirect('profiles')

@login_required(login_url='login_page')
def user_account(request):
    try:
        profile=Profile.objects.select_related('user').prefetch_related('skill_set').get(user_id=request.user.id)
    except Profile.DoesNotExist:
        raise Http404()
    context={'profile':profile}
    return render(request,'users/account.html', context)

@login_required(login_url='login_page')
def edit_account(request):
    profile_form=ProfileForm(instance=request.user.profile)
    user_form=UserEditForm(instance=request.user)
    if request.method == 'POST':
        profile_form=ProfileForm(request.POST, request.FILES ,instance=request.user.profile)
        user_form=UserEditForm(request.POST ,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save(request)
            return redirect('user_account')
    context={'profile_form':profile_form, 'user_form':user_form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login_page')
def add_skill(request):
    form=SkillForm()
    if request.method == 'POST':
        form=SkillForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('user_account')
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login_page')
def update_skill(request,pk):
    profile=request.user.profile
    skill=get_object_or_404(profile.skill_set, pk=pk)
    form=SkillForm(instance=skill)
    if request.method == 'POST':
        form=SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save(request)
            messages.info(request, 'Skill was updated successfully!')
            return redirect('user_account')
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login_page')
def delete_skill(request, pk):
    profile=request.user.profile
    skill=get_object_or_404(profile.skill_set, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.error(request, 'Skill was deleted successfully!')
        return redirect('user_account')
    context={'object':skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login_page')
def inbox(request):
    profile=request.user.profile
    msgs=Message.objects.filter(recipient=profile).select_related('sender__user')
    context={'msgs':msgs}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login_page')
def show_message(request, pk):
    profile=request.user.profile
    message=get_object_or_404(Message.objects.select_related('sender__user'), pk=pk, recipient=profile)
    message.is_read = True
    message.save()
    context={'msg':message}
    return render(request, 'users/message.html', context)

@login_required
def send_message(request, pk):
    form=MessageForm()
    profile=get_object_or_404(Profile, pk=pk)
    if request.method == 'POST' :
        form=MessageForm(request.POST)
        if form.is_valid():
            msg=form.save(commit=False)
            msg.sender=request.user.profile
            msg.recipient=profile
            if msg.recipient == request.user.profile:
                messages.error(request, 'you wanna message to yourself? are you crazy?')
                return redirect('profile', pk=pk)
            msg.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('profile', pk)
    context={'form':form, 'profile':profile}
    return render(request, 'users/message_form.html', context)


