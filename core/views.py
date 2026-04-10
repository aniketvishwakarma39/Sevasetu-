from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Event, Participation

User = get_user_model()

def home(request):
    query = request.GET.get('location')

    if query:
        events = Event.objects.filter(
            normalized_location__icontains=query.lower().strip()
        )
    else:
        events = Event.objects.all()

    return render(request, 'index.html', {'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            created_by=request.user
        )
        return redirect('home')

    return render(request, 'create_event.html')


def join_event(request, event_id):
    if request.user.is_authenticated:
        Participation.objects.get_or_create(
            user=request.user,
            event_id=event_id
        )
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)

        if user and user.role == role:
            login(request, user)

            if user.role == 'creator':
                return redirect('dashboard')

            return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
            role=request.POST['role']
        )
        return redirect('login')

    return render(request, 'signup.html')


@login_required
def creator_dashboard(request):
    if request.user.role != 'creator':
        return redirect('home')

    events = Event.objects.filter(created_by=request.user)
    participations = Participation.objects.filter(event__in=events)

    return render(request, 'dashboard.html', {
        'events': events,
        'participations': participations
    })

from .models import Sponsorship

@login_required
def sponsor_event(request, event_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        Sponsorship.objects.create(
            sponsor=request.user,
            event_id=event_id,
            amount=amount
        )

        return redirect('home')

    return render(request, 'sponsor.html')

from .models import Sponsorship

@login_required
def creator_dashboard(request):
    if request.user.role != 'creator':
        return redirect('home')

    events = Event.objects.filter(created_by=request.user)
    participations = Participation.objects.filter(event__in=events)
    sponsorships = Sponsorship.objects.filter(event__in=events)

    return render(request, 'dashboard.html', {
        'events': events,
        'participations': participations,
        'sponsorships': sponsorships
    })