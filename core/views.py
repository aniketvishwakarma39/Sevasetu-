from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
import os
from datetime import date
from .models import Event, Participation, Sponsorship, Profile

User = get_user_model()


# 🔥 BADGE SYSTEM
def update_badge(profile):
    points = profile.points

    if points >= 1000:
        profile.badge = "Champion 🏆"
    elif points >= 500:
        profile.badge = "Contributor 🟡"
    elif points >= 50:
        profile.badge = "Active 🔵"
    else:
        profile.badge = "Beginner 🟢"

    profile.save()


# 🏠 HOME
def home(request):
    query = request.GET.get('location')

    if query:
        events = Event.objects.filter(
            normalized_location__icontains=query.lower().strip()
        )
    else:
        events = Event.objects.all()

    return render(request, 'index.html', {'events': events})


# ➕ CREATE EVENT
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


# 🙋 JOIN EVENT + POINTS
def join_event(request, event_id):
    if request.user.is_authenticated:
        obj, created = Participation.objects.get_or_create(
            user=request.user,
            event_id=event_id
        )

        if created:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.points += 10
            update_badge(profile)

    return redirect('home')


# 💰 SPONSOR EVENT + POINTS
@login_required
def sponsor_event(request, event_id):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        Sponsorship.objects.create(
            sponsor=request.user,
            event_id=event_id,
            amount=amount
        )

        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.points += amount // 10
        update_badge(profile)

        return redirect('home')

    return render(request, 'sponsor.html')


# 🔐 LOGIN
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


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')


# 🆕 SIGNUP
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


# 📊 CREATOR DASHBOARD
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


# 🏆 LEADERBOARD
def leaderboard(request):
    profiles = Profile.objects.all().order_by('-points')
    return render(request, 'leaderboard.html', {'profiles': profiles})


# 👤 MY DASHBOARD
@login_required
def my_dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    rank = Profile.objects.filter(points__gt=profile.points).count() + 1

    return render(request, 'my_dashboard.html', {
        'profile': profile,
        'rank': rank
    })


# 🎓 CERTIFICATE DOWNLOAD (PDF)
from django.conf import settings
import os

@login_required
def generate_certificate(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # ✅ correct HTML render
    html = render_to_string('certificate.html', {
        'user': request.user,
        'profile': profile,
        'today': date.today().strftime("%d %B %Y")
    })

    # ✅ wkhtmltopdf config
    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    )

    # ✅ important fix (image + CSS support)
    pdf = pdfkit.from_string(
        html,
        False,
        configuration=config,
        options={"enable-local-file-access": ""}
    )

    # ✅ response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    return response