from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Event, Participation, Sponsorship, Profile

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
        return redirect('dashboard')

    return render(request, 'create_event.html')


def join_event(request, event_id):
    if request.user.is_authenticated:
        obj, created = Participation.objects.get_or_create(
            user=request.user,
            event_id=event_id
        )

        # 🔥 POINTS ADD
        if created:
            request.user.profile.points += 10
            request.user.profile.save()

    return redirect('home')


@login_required
def sponsor_event(request, event_id):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        Sponsorship.objects.create(
            sponsor=request.user,
            event_id=event_id,
            amount=amount
        )

        # 🔥 POINTS ADD
        request.user.profile.points += amount // 10
        request.user.profile.save()

        return redirect('home')

    return render(request, 'sponsor.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user and user.role == request.POST['role']:
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
        User.objects.create_user(
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
    sponsorships = Sponsorship.objects.filter(event__in=events)

    return render(request, 'dashboard.html', {
        'events': events,
        'participations': participations,
        'sponsorships': sponsorships
    })


def leaderboard(request):
    profiles = Profile.objects.all().order_by('-points')
    return render(request, 'leaderboard.html', {'profiles': profiles})


@login_required
def my_dashboard(request):
    profile = request.user.profile

    rank = Profile.objects.filter(points__gt=profile.points).count() + 1

    return render(request, 'my_dashboard.html', {
        'profile': profile,
        'rank': rank
    })