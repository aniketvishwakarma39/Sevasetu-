from django.shortcuts import render
from .models import Event

def home(request):
    query = request.GET.get('location')

    if query:
        events = Event.objects.filter(
            normalized_location__icontains=query.lower().strip()
        )
    else:
        events = Event.objects.all()

    return render(request, 'index.html', {'events': events})

from django.shortcuts import render, redirect
from .models import Event

def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')

        Event.objects.create(
            title=title,
            description=description,
            location=location,
            created_by=request.user 
        )

        return redirect('home')

    return render(request, 'create_event.html')