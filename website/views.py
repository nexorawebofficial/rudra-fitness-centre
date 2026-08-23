import os

from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from diets.models import DietCategory, DietPlan
from memberships.models import MembershipPlan
from notifications.services import notify_admins
from trainers.models import Trainer

from .forms import EnquiryForm
from .models import FAQ, Equipment, GalleryImage, Testimonial


def home(request):
    trainers = Trainer.objects.filter(is_active=True)[:3]
    plans = MembershipPlan.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_published=True)[:6]
    gallery = GalleryImage.objects.filter(is_visible=True)[:8]
    return render(request, 'website/home.html', {
        'trainers': trainers,
        'plans': plans,
        'testimonials': testimonials,
        'gallery': gallery,
    })


def about(request):
    return render(request, 'website/about.html')


def trainers(request):
    trainer_list = Trainer.objects.filter(is_active=True)
    return render(request, 'website/trainers.html', {'trainers': trainer_list})


def pricing(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    return render(request, 'website/pricing.html', {'plans': plans})


def equipment(request):
    equipment_list = Equipment.objects.filter(is_visible=True)
    return render(request, 'website/equipment.html', {'equipment_list': equipment_list})


def diet_nutrition(request):
    categories = DietCategory.objects.annotate(
        published_plan_count=Count('plans', filter=Q(plans__is_published=True)),
    )
    return render(request, 'website/diet_nutrition.html', {'categories': categories})


def diet_category_detail(request, slug):
    category = get_object_or_404(DietCategory, slug=slug)
    plans = category.plans.filter(is_published=True)
    return render(request, 'website/diet_category_detail.html', {'category': category, 'plans': plans})


def diet_plan_detail(request, pk):
    plan = get_object_or_404(DietPlan, pk=pk, is_published=True)
    return render(request, 'website/diet_plan_detail.html', {'plan': plan})


def gallery(request):
    images = GalleryImage.objects.filter(is_visible=True)
    return render(request, 'website/gallery.html', {'images': images})


def testimonials(request):
    testimonial_list = Testimonial.objects.filter(is_published=True)
    return render(request, 'website/testimonials.html', {'testimonials': testimonial_list})


def faq(request):
    faqs = FAQ.objects.filter(is_visible=True)
    return render(request, 'website/faq.html', {'faqs': faqs})


def contact(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            notify_admins(
                event_type='enquiry',
                title='New enquiry received',
                message=f"{enquiry.name} ({enquiry.phone or enquiry.email}): {enquiry.message[:200]}",
            )
            messages.success(request, "Thanks! We've received your message and will get back to you soon.")
            return redirect('contact')
    else:
        form = EnquiryForm()
    return render(request, 'website/contact.html', {'form': form})


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')


def terms_and_conditions(request):
    return render(request, 'website/terms_and_conditions.html')


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


def assetlinks(request):
    """Digital Asset Links file that proves this domain owns the Android (TWA) app,
    so Play Store's package opens full-screen with no browser address bar.

    Fill in TWA_PACKAGE_NAME and TWA_SHA256_FINGERPRINT (from PWABuilder / your
    Play signing key) once the Android package has been generated. Until then this
    intentionally returns an empty list.
    """
    TWA_PACKAGE_NAME = ''  # e.g. "com.rudrafitness.app"
    TWA_SHA256_FINGERPRINT = ''  # e.g. "14:6D:E9:83:C5:73..." from PWABuilder

    if not TWA_PACKAGE_NAME or not TWA_SHA256_FINGERPRINT:
        return JsonResponse([], safe=False)

    return JsonResponse([
        {
            'relation': ['delegate_permission/common.handle_all_urls'],
            'target': {
                'namespace': 'android_app',
                'package_name': TWA_PACKAGE_NAME,
                'sha256_cert_fingerprints': [TWA_SHA256_FINGERPRINT],
            },
        },
    ], safe=False)
