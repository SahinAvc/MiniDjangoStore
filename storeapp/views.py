from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, RegisterForm


def home(request):
    products = Product.objects.filter(is_active=True).select_related("category", "seller")
    categories = Category.objects.all()

    q = request.GET.get("q", "").strip()
    category_slug = request.GET.get("kategori", "").strip()
    city = request.GET.get("sehir", "").strip()
    min_price = request.GET.get("min_fiyat", "").strip()
    max_price = request.GET.get("max_fiyat", "").strip()

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if city:
        products = products.filter(city=city)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        "products": products,
        "categories": categories,
        "cities": Product.CITIES,
        "filters": {
            "q": q,
            "kategori": category_slug,
            "sehir": city,
            "min_fiyat": min_price,
            "max_fiyat": max_price,
        },
        "total_count": products.count(),
    }
    return render(request, "storeapp/public/home.html", context)


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("category", "seller"),
        pk=pk,
        is_active=True,
    )
    similar = Product.objects.filter(
        is_active=True,
        category=product.category,
    ).exclude(pk=pk)[:4]
    return render(
        request,
        "storeapp/public/product_detail.html",
        {"product": product, "similar": similar},
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("storeapp:panel_dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Hoş geldiniz! Hesabınız oluşturuldu.")
            return redirect("storeapp:panel_dashboard")
    else:
        form = RegisterForm()
    return render(request, "storeapp/auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("storeapp:panel_dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Tekrar hoş geldiniz, {user.username}!")
            next_url = request.GET.get("next", "storeapp:panel_dashboard")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"
    return render(request, "storeapp/auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız.")
    return redirect("storeapp:home")


@login_required(login_url="storeapp:login")
def panel_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    stats = {
        "total": products.count(),
        "active": products.filter(is_active=True).count(),
        "inactive": products.filter(is_active=False).count(),
    }
    return render(
        request,
        "storeapp/panel/dashboard.html",
        {"products": products, "stats": stats},
    )


@login_required(login_url="storeapp:login")
def panel_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "İlanınız başarıyla yayınlandı.")
            return redirect("storeapp:panel_dashboard")
    else:
        form = ProductForm()
    return render(
        request,
        "storeapp/panel/product_form.html",
        {"form": form, "title": "Yeni İlan Ver"},
    )


@login_required(login_url="storeapp:login")
def panel_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{product.name}" güncellendi.')
            return redirect("storeapp:panel_dashboard")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "storeapp/panel/product_form.html",
        {"form": form, "title": "İlanı Düzenle", "product": product},
    )


@login_required(login_url="storeapp:login")
def panel_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f'"{name}" silindi.')
        return redirect("storeapp:panel_dashboard")
    return render(
        request,
        "storeapp/panel/product_confirm_delete.html",
        {"product": product},
    )
