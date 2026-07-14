from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField("Kategori", max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField("İkon", max_length=50, blank=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    CITIES = [
        ("istanbul", "İstanbul"),
        ("ankara", "Ankara"),
        ("izmir", "İzmir"),
        ("bursa", "Bursa"),
        ("antalya", "Antalya"),
        ("adana", "Adana"),
        ("konya", "Konya"),
        ("gaziantep", "Gaziantep"),
        ("diger", "Diğer"),
    ]

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Satıcı",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kategori",
    )
    name = models.CharField("İlan Başlığı", max_length=200)
    description = models.TextField("Açıklama", blank=True)
    price = models.DecimalField("Fiyat", max_digits=10, decimal_places=2)
    city = models.CharField("Şehir", max_length=50, choices=CITIES, default="istanbul")
    stock = models.PositiveIntegerField("Stok", default=1)
    image_url = models.URLField("Resim URL", max_length=500, blank=True, null=True)
    is_active = models.BooleanField("Yayında", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&auto=format&fit=crop&q=60"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "İlan"
        verbose_name_plural = "İlanlar"

    def __str__(self):
        return self.name

    def get_city_display_name(self):
        return dict(self.CITIES).get(self.city, self.city)
