from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import Event, Participation, Sponsorship, Profile

User = get_user_model()


# ================= BADGE SYSTEM =================
def update_badge(profile):
    if profile.points >= 1000:
        profile.badge = "Champion 🏆"
    elif profile.points >= 500:
        profile.badge = "Contributor 🟡"
    elif profile.points >= 50:
        profile.badge = "Active 🔵"
    else:
        profile.badge = "Beginner 🟢"
    profile.save()


# ================= AUTO DELETE EVENTS =================
def delete_expired_events():
    today = timezone.now().date()
    Event.objects.filter(end_date__lt=today).delete()


# ================= HOME =================
def home(request):
    delete_expired_events()

    query = request.GET.get('location')

    if query:
        events = Event.objects.filter(
            normalized_location__icontains=query.lower().strip()
        )
    else:
        events = Event.objects.filter(end_date__gte=timezone.now().date())

    return render(request, 'index.html', {'events': events})


# ================= CREATE EVENT =================
@login_required
def create_event(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            created_by=request.user
        )
        return redirect('dashboard')

    return render(request, 'create_event.html')


# ================= JOIN EVENT (PENDING) =================
def join_event(request, event_id):
    if request.user.is_authenticated:
        Participation.objects.get_or_create(
            user=request.user,
            event_id=event_id,
            defaults={'status': 'pending'}
        )

    return redirect('home')


# ================= SPONSOR EVENT (PENDING) =================
@login_required
def sponsor_event(request, event_id):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        Sponsorship.objects.create(
            sponsor=request.user,
            event_id=event_id,
            amount=amount,
            status='pending'
        )

        return redirect('home')

    return render(request, 'sponsor.html')


# ================= LOGIN =================
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


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('home')


# ================= SIGNUP =================
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


# ================= CREATOR DASHBOARD =================
@login_required
def creator_dashboard(request):
    if request.user.role != 'creator':
        return redirect('home')

    events = Event.objects.filter(created_by=request.user)

    participations = Participation.objects.filter(
        event__in=events, status='pending'
    )

    sponsorships = Sponsorship.objects.filter(
        event__in=events, status='pending'
    )

    return render(request, 'dashboard.html', {
        'events': events,
        'participations': participations,
        'sponsorships': sponsorships
    })


# ================= APPROVE VOLUNTEER =================
@login_required
def approve_participation(request, id):
    obj = Participation.objects.get(id=id)
    obj.status = 'approved'
    obj.save()

    profile, _ = Profile.objects.get_or_create(user=obj.user)
    profile.points += 10
    update_badge(profile)

    return redirect('dashboard')


# ================= REJECT VOLUNTEER =================
@login_required
def reject_participation(request, id):
    obj = Participation.objects.get(id=id)
    obj.status = 'rejected'
    obj.save()
    return redirect('dashboard')


# ================= APPROVE SPONSOR =================
@login_required
def approve_sponsorship(request, id):
    obj = Sponsorship.objects.get(id=id)
    obj.status = 'approved'
    obj.save()

    profile, _ = Profile.objects.get_or_create(user=obj.sponsor)
    profile.points += obj.amount // 10
    update_badge(profile)

    return redirect('dashboard')


# ================= REJECT SPONSOR =================
@login_required
def reject_sponsorship(request, id):
    obj = Sponsorship.objects.get(id=id)
    obj.status = 'rejected'
    obj.save()
    return redirect('dashboard')


# ================= LEADERBOARD =================
def leaderboard(request):
    profiles = Profile.objects.all().order_by('-points')
    return render(request, 'leaderboard.html', {'profiles': profiles})


# ================= MY DASHBOARD =================
@login_required
def my_dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    rank = Profile.objects.filter(points__gt=profile.points).count() + 1

    return render(request, 'my_dashboard.html', {
        'profile': profile,
        'rank': rank
    })


# ================= CERTIFICATE =================
@login_required
def generate_certificate(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    html = render_to_string('certificate.html', {
        'user': request.user,
        'profile': profile,
        'today': timezone.now().date()
    })

    return HttpResponse(html)