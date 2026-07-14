import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from storeapp.models import Category, Product

class Command(BaseCommand):
    help = "Seeds categories and products into the database"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # 1. Ensure we have at least one user
        user, created = User.objects.get_or_create(username="demo")
        if created:
            user.set_password("demo1234")
            user.email = "demo@example.com"
            user.save()
            self.stdout.write(f"Created demo user: demo / demo1234")
        else:
            self.stdout.write("Using existing demo user")

        # Create an admin user too for convenience
        admin_user, admin_created = User.objects.get_or_create(username="admin", is_staff=True, is_superuser=True)
        if admin_created:
            admin_user.set_password("admin1234")
            admin_user.save()
            self.stdout.write("Created admin user: admin / admin1234")

        # 2. Categories data
        categories_data = [
            {"name": "Elektronik", "slug": "elektronik", "icon": "💻"},
            {"name": "Moda & Giyim", "slug": "moda-giyim", "icon": "👕"},
            {"name": "Ev & Yaşam", "slug": "ev-yasam", "icon": "🛋️"},
            {"name": "Spor & Outdoor", "slug": "spor-outdoor", "icon": "🏕️"},
            {"name": "Kitap & Hobi", "slug": "kitap-hobi", "icon": "📚"},
        ]

        categories = {}
        for cat_info in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_info["slug"],
                defaults={"name": cat_info["name"], "icon": cat_info["icon"]}
            )
            categories[cat_info["slug"]] = cat
            if created:
                self.stdout.write(f"Created category: {cat.name}")

        # 3. Products data
        products_data = [
            # Elektronik
            {
                "category_slug": "elektronik",
                "name": "iPhone 14 Pro Max 256 GB - Derin Mor",
                "description": "Kutusu, faturası ve orijinal şarj kablosuyla birlikte verilecektir. Pil sağlığı %89'dur. Ekranda ve kasada herhangi bir çizik ya da darbe yoktur. Garantisi yeni bitti. Kılıfları hediyedir.",
                "price": 42500.00,
                "city": "istanbul",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&auto=format&fit=crop&q=80",
            },
            {
                "category_slug": "elektronik",
                "name": "Sony WH-1000XM4 Kablosuz Kulak Üstü ANC Kulaklık",
                "description": "Aktif gürültü engelleme özelliği mükemmel çalışıyor. Çok az kullanıldı, sıfırdan farksızdır. Orijinal taşıma kutusu, AUX kablosu ve şarj kablosu mevcuttur. Pazarlık cüzidir.",
                "price": 8200.00,
                "city": "ankara",
                "stock": 3,
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
            },
            {
                "category_slug": "elektronik",
                "name": "MacBook Air M2 8GB 256GB SSD - Uzay Grisi",
                "description": "13.6 inç Liquid Retina ekran. Pil döngüsü sadece 45. Çiziksiz, temiz, ofis işleri için kullanıldı. Orijinal kutusu ve 30W adaptörü ile teslim edilecektir.",
                "price": 34000.00,
                "city": "izmir",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=600&auto=format&fit=crop&q=80",
            },
            # Moda
            {
                "category_slug": "moda-giyim",
                "name": "Nike Air Force 1 '07 - Beyaz Erkek Spor Ayakkabı",
                "description": "42 numara. Hiç giyilmedi, orijinal kutusunda duruyor. Yurt dışından hediye geldi ancak numarası küçük olduğu için satıyorum. Orijinallik kodu sorgulanabilir.",
                "price": 3100.00,
                "city": "bursa",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&auto=format&fit=crop&q=80",
            },
            {
                "category_slug": "moda-giyim",
                "name": "Vintage Oversize Deri Ceket - Siyah",
                "description": "Gerçek deridir. L beden uyumlu, dökümlü vintage kesim. Herhangi bir yırtığı, söküğü yoktur. Kuru temizlemesi yeni yapıldı. Çok tarz bir parça.",
                "price": 2400.00,
                "city": "istanbul",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&auto=format&fit=crop&q=80",
            },
            # Ev & Yasam
            {
                "category_slug": "ev-yasam",
                "name": "Minimalist Tasarım Ahşap Sehpa",
                "description": "Masif meşe ağacından el yapımı üretilmiştir. Salonunuza modern ve sıcak bir hava katacak. Ölçüleri: 80x50 cm, Yükseklik 42 cm. Hiçbir hasarı yoktur.",
                "price": 1850.00,
                "city": "antalya",
                "stock": 5,
                "image_url": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=600&auto=format&fit=crop&q=80",
            },
            {
                "category_slug": "ev-yasam",
                "name": "İskandinav Tarzı Keten L Koltuk - Gri",
                "description": "Temiz kullanılmış, lekesiz, yıkanabilir keten kılıflı L koltuk. Oturumu oldukça rahat ve geniştir. Taşınma sebebiyle satıyoruz. Demonte edilebilir.",
                "price": 14500.00,
                "city": "istanbul",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=600&auto=format&fit=crop&q=80",
            },
            # Spor & Outdoor
            {
                "category_slug": "spor-outdoor",
                "name": "Decathlon Quechua 3 Kişilik Kamp Çadırı",
                "description": "MH100 modeli. Sadece 2 kamp döneminde kullanıldı. Yırtık, sökük, su sızdırma gibi hiçbir problemi yoktur. Tüm kurulum aparatları, polleri ve kazıkları eksiksizdir.",
                "price": 1950.00,
                "city": "adana",
                "stock": 2,
                "image_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=600&auto=format&fit=crop&q=80",
            },
            {
                "category_slug": "spor-outdoor",
                "name": "Carraro Sportive 220 Şehir Bisikleti",
                "description": "24 vites, kilitlenebilir maşa, alüminyum kadro. 28 jant. Çok az kullanıldı, kapalı garajda muhafaza edildi. Bakımları yeni yapıldı, kullanıma hazır. Yanında kilit ve zil hediye.",
                "price": 9500.00,
                "city": "izmir",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=600&auto=format&fit=crop&q=80",
            },
            # Kitap & Hobi
            {
                "category_slug": "kitap-hobi",
                "name": "Catan Board Game - Türkçe Kutulu Kutu Oyunu",
                "description": "Dünyaca ünlü strateji oyunu Catan. Kutusu ve tüm içeriği eksiksiz, tertemiz durumdadır. Kartlarda ve pullarda yıpranma yoktur. Arkadaş grupları için harika bir eğlence.",
                "price": 1200.00,
                "city": "ankara",
                "stock": 2,
                "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=600&auto=format&fit=crop&q=80",
            },
            {
                "category_slug": "kitap-hobi",
                "name": "Kozmos Klasik Gitar - Başlangıç Seviyesi",
                "description": "Gitar öğrenmek isteyenler için ideal, yumuşak basımlı klasik gitar. Sap ayarı düzgündür. Yanında taşıma çantası ve penalar verilecektir. Telleri yeni değişti.",
                "price": 2100.00,
                "city": "konya",
                "stock": 1,
                "image_url": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=600&auto=format&fit=crop&q=80",
            }
        ]

        # Clean existing mock products if any to avoid duplication of this specific run
        Product.objects.filter(seller=user).delete()

        for prod_info in products_data:
            cat = categories.get(prod_info["category_slug"])
            product = Product.objects.create(
                seller=user,
                category=cat,
                name=prod_info["name"],
                description=prod_info["description"],
                price=prod_info["price"],
                city=prod_info["city"],
                stock=prod_info["stock"],
                image_url=prod_info["image_url"],
                is_active=True
            )
            self.stdout.write(f"Created product: {product.name} ({product.price} TL)")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
