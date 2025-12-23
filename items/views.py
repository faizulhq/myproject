from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm

# --- Halaman Utama ---
def index(request):
    return render(request, 'items/index.html')

# --- CRUD Views (Django Template Biasa) ---

# 1. READ (List View)
def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})

# 2. CREATE
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'title': 'Tambah Item Baru'})

# 3. UPDATE
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form, 'title': 'Edit Item'})

# 4. DELETE
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})

# --- API ViewSets (Yang lama) ---
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
