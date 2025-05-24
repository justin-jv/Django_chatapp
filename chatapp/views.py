from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Message, Group, GroupMessage, CustomUser
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_home')
    else:
        form = RegisterForm
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('chat_home')
    else:
        form = LoginForm()
    return render(request,'login.html', {'form':form})    


def logout_view(request):
    logout(request)
    return redirect('login')


User = get_user_model()

@login_required
def chat_home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request,'chat_home.html',{'users':users})


@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            Message.objects.create(sender=request.user, receiver=other_user,message=msg)

    messages = Message.objects.filter(
        sender = request.user, receiver = other_user
    ) | Message.objects.filter(
        sender=other_user, receiver=request.user
    )
    messages = messages.order_by('timestamp')

    return render(request, 'chat_detail.html', {
        'other_user': other_user,
        'messages': messages
    })



@login_required
def group_list(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'group_list.html', {'groups': groups})


@login_required
def group_chat(request,group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user not in group.members.all():
        return HttpResponse("You are not a member of this group.")
    
    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            GroupMessage.objects.create(group=group, sender=request.user, message=msg)
    
    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')

    return render(request, 'group_chat.html', {
        'group': group,
        'messages': messages
    })

def private_chat_view(request, username):
    other_user = get_object_or_404(CustomUser, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_view(request, username):
    other_user = User.objects.filter(username=username).first()
    if not other_user:
        return render(request, 'chat_not_found.html')  # create a simple error page

    context = {
        'other_user': other_user,
    }
    return render(request, 'chat_detail.html', context)
