
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item
from .forms import CategoryForm, ItemForm
from django.core.paginator import Paginator
from django.db import models
from datetime import datetime
import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def painel(request):
    categories = Category.objects.all()
    context = {
        "total_itens": Item.objects.count(),
        "total_categorias": categories.count(),
        "total_estoque": Item.objects.aggregate(total=models.Sum('quantity'))['total'] or 0,
        "total_alertas": Item.objects.filter(quantity__lt=5).count(),
        "nomes_categorias": [c.name for c in categories],
        "quantidades_categorias": [c.items.count() for c in categories],
        "ano_atual": datetime.now().year
    }
    return render(request, "painel/dashboard.html", context)

# Categories CRUD
def category_list(request):
    q = request.GET.get('q', '')
    qs = Category.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    return render(request, "painel/categories/list.html", {"categories": categories, "q": q})

def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, "painel/categories/form.html", {"form": form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, "painel/categories/form.html", {"form": form, "object": category})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('category-list')
    return render(request, "painel/categories/delete.html", {"object": category})

# Items CRUD
def item_list(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    low = request.GET.get('low', '')
    qs = Item.objects.select_related('category').all()
    if q:
        qs = qs.filter(name__icontains=q)
    if cat:
        qs = qs.filter(category_id=cat)
    if low == '1':
        qs = qs.filter(quantity__lt=5)
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    categories = Category.objects.all()
    return render(request, "painel/items/list.html", {"items": items, "categories": categories, "q": q, "cat": cat, "low": low})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "painel/items/detail.html", {"item": item})

def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item-list')
    else:
        form = ItemForm()
    return render(request, "painel/items/form.html", {"form": form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item-list')
    else:
        form = ItemForm(instance=item)
    return render(request, "painel/items/form.html", {"form": form, "object": item})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect('item-list')
    return render(request, "painel/items/delete.html", {"object": item})

# PDF
def items_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, height - 50, "Relatório de Itens - Sistema de Inventário")
    p.setFont("Helvetica", 10)
    y = height - 80
    items = Item.objects.select_related('category').all()
    for it in items:
        line = f"{it.id} - {it.name} | Categoria: {it.category.name if it.category else '---'} | Quantidade: {it.quantity}"
        p.drawString(40, y, line[:120])
        y -= 18
        if y < 80:
            p.showPage()
            y = height - 50
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
