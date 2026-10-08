import re, datetime
from django import forms
from .models import TrialBooking

class BookingForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))  # honeypot
    phone = forms.CharField(max_length=20)  # cleaned to 10 digits below
    class Meta:
        model = TrialBooking
        fields = ["name", "phone", "email", "plan", "preferred_date", "message"]
        widgets = {"preferred_date": forms.DateInput(attrs={"type": "date"}), "message": forms.Textarea(attrs={"rows": 3})}
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        for n, f in self.fields.items():
            if n != "website": f.widget.attrs["class"] = "form-control"
        self.fields["plan"].empty_label = "Not sure yet"
        self.fields["phone"].widget.attrs.update({"placeholder": "10-digit mobile number", "inputmode": "numeric"})
    def clean_phone(self):
        d = re.sub(r"\D", "", self.cleaned_data["phone"])
        if len(d) == 12 and d.startswith("91"): d = d[2:]
        if not re.fullmatch(r"[6-9]\d{9}", d): raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return d
    def clean_preferred_date(self):
        d = self.cleaned_data["preferred_date"]
        if d < datetime.date.today(): raise forms.ValidationError("Please pick today or a future date.")
        return d
    def clean_website(self):
        if self.cleaned_data.get("website"): raise forms.ValidationError("Spam detected.")
        return ""
