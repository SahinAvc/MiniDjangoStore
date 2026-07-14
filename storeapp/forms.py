from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-posta")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Kullanıcı Adı",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Şifre"
        self.fields["password2"].label = "Şifre (Tekrar)"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "description", "price", "city", "stock", "image_url", "is_active"]
        labels = {
            "category": "Kategori",
            "name": "İlan Başlığı",
            "description": "Açıklama",
            "price": "Fiyat (₺)",
            "city": "Şehir",
            "stock": "Stok Adedi",
            "image_url": "Resim URL",
            "is_active": "İlanı yayınla",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Örn: iPhone 14 Pro Max 256GB"}),
            "description": forms.Textarea(attrs={"rows": 6, "placeholder": "Ürününüzü detaylı anlatın..."}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "stock": forms.NumberInput(attrs={"min": "1"}),
            "image_url": forms.URLInput(attrs={"placeholder": "Örn: https://images.unsplash.com/... (Boş bırakılırsa varsayılan resim kullanılır)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_active":
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-check-input"
