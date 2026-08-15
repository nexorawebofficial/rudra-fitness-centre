import os

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm
from .models import MembershipPlan, Trainer


def home(request):
    trainers = Trainer.objects.all()[:3]
    plans = MembershipPlan.objects.all()[:3]
    return render(request, 'website/home.html', {'trainers': trainers, 'plans': plans})


def about(request):
    return render(request, 'website/about.html')


def trainers(request):
    trainer_list = Trainer.objects.all()
    return render(request, 'website/trainers.html', {'trainers': trainer_list})


def pricing(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'website/pricing.html', {'plans': plans})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! We've received your message and will get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})


def offline(request):
    return render(request, 'website/offline.html')


def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'sw.js')
    with open(sw_path, 'r', encoding='utf-8') as f:
        content = f.read()
    response = HttpResponse(content, content_type='application/javascript')
    # Root scope so the service worker can control every page, not just /static/js/
    response['Service-Worker-Allowed'] = '/'
    return response
