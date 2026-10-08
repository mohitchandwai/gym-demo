from urllib.parse import quote
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import CATS, ClassSession, Plan, Testimonial, Trainer, TrialBooking, SiteSettings

def home(request):
    sessions = list(ClassSession.objects.select_related("trainer"))
    tabs = [("all", "All Classes", sessions)] + [(k, l, [s for s in sessions if s.category == k]) for k, l in CATS]
    tabs = [t for t in tabs if t[2]]
    return render(request, "home.html", {"plans": Plan.objects.all(), "trainers": Trainer.objects.all(),
        "testimonials": Testimonial.objects.filter(visible=True), "tabs": tabs})

def book(request):
    form = BookingForm(request.POST or None, initial={"plan": request.GET.get("plan")})
    if request.method == "POST" and form.is_valid():
        key = "book:" + request.META.get("REMOTE_ADDR", "x"); n = cache.get(key, 0)
        if n >= 5:
            form.add_error(None, "Too many requests. Please try again in an hour or WhatsApp us.")
        else:
            cache.set(key, n + 1, 3600)
            b = form.save()
            request.session["last_booking"] = b.pk
            site = SiteSettings.load()
            if site.email:
                send_mail(f"New free trial booking: {b.name}", f"Name: {b.name}\nPhone: {b.phone}\nPlan: {b.plan}\nDate: {b.preferred_date}\nMessage: {b.message}",
                          None, [site.email], fail_silently=True)
            return redirect("book_thanks")
    return render(request, "book.html", {"form": form})

def book_thanks(request):
    b = TrialBooking.objects.filter(pk=request.session.get("last_booking")).first()
    if not b: return redirect("book")
    site = SiteSettings.load()
    wa = ""
    if site.whatsapp:
        wa = f"https://wa.me/{site.whatsapp}?text=" + quote(f"Hi, I'm {b.name}. I booked a free trial for {b.preferred_date:%d %b %Y}. My number: {b.phone}.")
    return render(request, "thanks.html", {"booking": b, "wa_link": wa})
