from datetime import time
from django.core.management.base import BaseCommand
from core.models import SiteSettings, Plan, Trainer, ClassSession

class Command(BaseCommand):
    help = "Load SAMPLE content (edit or delete everything in /admin before going live)"
    def handle(self, *a, **k):
        if Plan.objects.exists(): return self.stdout.write("Data already exists, skipping.")
        s = SiteSettings.load(); s.name = "Gymnast Fitness"; s.whatsapp = "919999999999"; s.phone = "+91 99999 99999"
        s.address = "Your gym address here"; s.save()
        for i, (n, p, f, pop) in enumerate([("Starter", 1499, "Gym floor access\nCardio zone\nLocker facility", False),
            ("Pro", 2499, "Everything in Starter\nAll group classes\nPersonal trainer sessions", True),
            ("Elite", 3999, "Everything in Pro\nUnlimited PT sessions\nCustom diet plan", False)]):
            Plan.objects.create(name=n, price=p, features=f, is_popular=pop, order=i)
        tr = [Trainer.objects.create(name=n, role=r, order=i) for i, (n, r) in enumerate(
            [("Trainer One", "Strength Coach"), ("Trainer Two", "Cardio & HIIT"), ("Trainer Three", "Yoga"), ("Trainer Four", "Crossfit")])]
        rows = [("Morning Cardio", "cardio", 0, 6, 0, 0), ("Crossfit", "crossfit", 1, 7, 0, 3), ("Power Lifting", "powerlifting", 2, 18, 0, 0),
                ("Yoga Flow", "yoga", 3, 6, 30, 2), ("HIIT Burn", "hiit", 4, 18, 30, 1), ("Bootcamp", "crossfit", 5, 8, 0, 3), ("Stretch & Recover", "yoga", 6, 9, 0, 2)]
        for n, c, d, h, m, t in rows:
            ClassSession.objects.create(name=n, category=c, day=d, start=time(h, m), end=time(h + 1, m), trainer=tr[t])
        self.stdout.write("Sample data loaded. Replace it in /admin.")
