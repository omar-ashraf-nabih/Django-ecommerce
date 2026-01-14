from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="الاسم بالكامل", max_length=120)
    phone = forms.CharField(label="رقم الهاتف", max_length=30)
    address = forms.CharField(label="العنوان", widget=forms.Textarea(attrs={"rows": 3}))
    notes = forms.CharField(label="ملاحظات", required=False, widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " input").strip()
