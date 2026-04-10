from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SOS, SOSJoin


@login_required
def create_sos(request):
    if request.method == 'POST':
        SOS.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            created_by=request.user
        )
        return redirect('sos_list')

    return render(request, 'create_sos.html')


def sos_list(request):
    sos_list = SOS.objects.all()
    return render(request, 'sos_list.html', {'sos_list': sos_list})


@login_required
def join_sos(request, sos_id):
    sos = SOS.objects.get(id=sos_id)

    SOSJoin.objects.get_or_create(
        sos=sos,
        volunteer=request.user,
        defaults={'status': 'pending'}
    )

    # 🔥 EMAIL SEND
    send_mail(
        subject='🚨 SOS Alert!',
        message=f'''
{request.user.username} has joined your SOS request.

Location: {sos.location}

Please respond quickly.
''',
        from_email='your_email@gmail.com',
        recipient_list=[sos.created_by.email],
        fail_silently=False,
    )

    return redirect('sos_list')
@login_required
def approve_sos(request, id):
    obj = SOSJoin.objects.get(id=id)
    obj.status = 'approved'
    obj.save()
    return redirect('sos_list')


@login_required
def reject_sos(request, id):
    obj = SOSJoin.objects.get(id=id)
    obj.status = 'rejected'
    obj.save()
    return redirect('sos_list')

from django.core.mail import send_mail