from django.db import models
from django.templatetags.static import static
DAYS = [(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")]
CATS = [("cardio", "Cardio"), ("crossfit", "Crossfit"), ("powerlifting", "Powerlifting"), ("yoga", "Yoga"), ("hiit", "HIIT")]

class SiteSettings(models.Model):
    name = models.CharField(max_length=80, default="Gymnast Fitness")
    tagline = models.CharField(max_length=120, default="Train Hard. Feel Strong.")
    about_title = models.CharField(max_length=100, default="Train With Experts")
    about_text = models.TextField(default="Modern equipment, supportive trainers and classes for every level.")
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=15, blank=True, help_text="Digits with country code, e.g. 917668352855")
    email = models.EmailField(blank=True, help_text="Booking notifications are sent here")
    address = models.CharField(max_length=200, blank=True)
    hours_weekday = models.CharField(max_length=60, default="6.00 AM - 10.00 PM")
    hours_weekend = models.CharField(max_length=60, default="7.00 AM - 8.00 PM")
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    class Meta:
        verbose_name_plural = "Site settings"
    def __str__(self): return self.name
    def save(self, *a, **k):
        self.pk = 1; super().save(*a, **k)
    @classmethod
    def load(cls): return cls.objects.get_or_create(pk=1)[0]

class Plan(models.Model):
    name = models.CharField(max_length=60)
    price = models.PositiveIntegerField(help_text="Rupees per month")
    features = models.TextField(help_text="One feature per line")
    is_popular = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["order", "price"]
    def __str__(self): return f"{self.name} (Rs {self.price})"
    def feature_list(self): return [f.strip() for f in self.features.splitlines() if f.strip()]

class Trainer(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=80, default="Trainer")
    photo = models.FileField(upload_to="trainers/", blank=True, help_text="Optional. Square photo works best")
    order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["order", "name"]
    def __str__(self): return self.name
    @property
    def photo_url(self): return self.photo.url if self.photo else static(f"img/team-{(self.pk or 0) % 4 + 1}.jpg")

class ClassSession(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CATS)
    day = models.PositiveSmallIntegerField(choices=DAYS)
    start = models.TimeField(); end = models.TimeField()
    trainer = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.SET_NULL)
    class Meta: ordering = ["day", "start"]
    def __str__(self): return f"{self.name} - {self.get_day_display()}"

class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    profession = models.CharField(max_length=80, blank=True)
    text = models.TextField()
    photo = models.FileField(upload_to="testimonials/", blank=True)
    visible = models.BooleanField(default=True, help_text="Only add real member reviews")
    @property
    def photo_url(self): return self.photo.url if self.photo else static("img/user.jpg")
    def __str__(self): return self.name

class TrialBooking(models.Model):
    STATUS = [("new", "New"), ("contacted", "Contacted"), ("joined", "Joined"), ("closed", "Closed")]
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=10)
    email = models.EmailField(blank=True)
    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.SET_NULL)
    preferred_date = models.DateField()
    message = models.TextField(blank=True, max_length=500)
    status = models.CharField(max_length=12, choices=STATUS, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.name} ({self.phone})"
