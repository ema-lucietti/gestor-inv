# En admin.py
from django.contrib import admin
from .models import Ubicacion, Pallet, Producto

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Pallet) 
class PalletAdmin(admin.ModelAdmin):
    list_display = ['numero_pallet', 'ubicacion']
    list_filter = ['ubicacion']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_barras', 'cantidad', 'pallet']
    list_filter = ['pallet__ubicacion']
    search_fields = ['nombre', 'codigo_barras']