import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import SiteSettings, Plan, Trainer, ClassSession, Testimonial, TrialBooking

@admin.register(SiteSettings)
class SiteAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None): return False

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_popular", "order"); list_editable = ("price", "is_popular", "order")

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order"); list_editable = ("order",)

@admin.register(ClassSession)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "day", "start", "end", "trainer"); list_filter = ("day", "category")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "profession", "visible"); list_editable = ("visible",)

@admin.register(TrialBooking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "whatsapp", "plan", "preferred_date", "status", "created_at")
    list_editable = ("status",); list_filter = ("status", "plan"); search_fields = ("name", "phone", "email")
    date_hierarchy = "created_at"; actions = ["export_csv", "mark_contacted"]
    @admin.display(description="WhatsApp")
    def whatsapp(self, o): return format_html('<a href="https://wa.me/91{}" target="_blank" rel="noopener">Chat</a>', o.phone)
    @admin.action(description="Mark selected as contacted")
    def mark_contacted(self, request, qs): qs.update(status="contacted")
    @admin.action(description="Export selected to CSV")
    def export_csv(self, request, qs):
        r = HttpResponse(content_type="text/csv"); r["Content-Disposition"] = 'attachment; filename="bookings.csv"'
        w = csv.writer(r); w.writerow(["Name", "Phone", "Email", "Plan", "Date", "Status", "Created"])
        for b in qs: w.writerow([b.name, b.phone, b.email, b.plan or "", b.preferred_date, b.status, b.created_at.strftime("%Y-%m-%d %H:%M")])
        return r
