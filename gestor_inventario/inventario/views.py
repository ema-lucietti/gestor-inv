# inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Ubicacion, Pallet, Producto, RemitoSalida, DetalleSalida
from .forms import (ProductoForm, UbicacionForm, PalletForm, 
                   RemitoSalidaForm, DetalleSalidaFormSet)


def cargar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado correctamente')
            return redirect('cargar_producto')
    else:
        form = ProductoForm()

    return render(request, 'inventario/cargar_producto.html', {'form': form})

def escanear_producto(request):
    form = ProductoForm()
    return render(request, 'inventario/escanear_producto.html', {'form': form})


def imprimir_etiqueta(request, pallet_id):
    pallet = get_object_or_404(Pallet, id=pallet_id)
    productos = Producto.objects.filter(pallet=pallet)
    return render(request, 'inventario/etiqueta.html', {'pallet': pallet, 'productos': productos})


def lista_pallets(request):
    ubicaciones = Ubicacion.objects.all()
    ubicacion_id = request.GET.get('ubicacion')
    
    if ubicacion_id:
        pallets = Pallet.objects.filter(ubicacion_id=ubicacion_id).select_related('ubicacion')
    else:
        pallets = Pallet.objects.all().select_related('ubicacion')

    return render(request, 'inventario/lista_pallets.html', {
        'pallets': pallets,
        'ubicaciones': ubicaciones,
        'ubicacion_seleccionada': int(ubicacion_id) if ubicacion_id else None,
    })

def crear_ubicacion(request):
    form = UbicacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Ubicación creada correctamente')
        return redirect('crear_ubicacion')
    return render(request, 'inventario/crear_ubicacion.html', {'form': form})

def crear_pallet(request):
    form = PalletForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Pallet creado correctamente')
        return redirect('lista_pallets')
    return render(request, 'inventario/crear_pallet.html', {'form': form})


def detalle_ubicacion(request, ubicacion_id):
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
    pallets = Pallet.objects.filter(ubicacion=ubicacion)
    return render(request, 'inventario/detalle_ubicacion.html', {
        'ubicacion': ubicacion,
        'pallets': pallets,
    })

def lista_ubicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'inventario/lista_ubicaciones.html', {
        'ubicaciones': ubicaciones
    })


def dashboard(request):
    productos = Producto.objects.all()
    ubicaciones = Ubicacion.objects.all()
    pallets = Pallet.objects.all().order_by('-id')  
    remitos_recientes = RemitoSalida.objects.all()[:5]

    # Estadísticas
    total_productos = productos.count()
    total_stock = sum(p.cantidad for p in productos)
    productos_sin_stock = productos.filter(cantidad=0).count()

    context = {
        'productos': productos,
        'ubicaciones': ubicaciones,
        'entradas': pallets[:5],
        'salidas': remitos_recientes,
        'total_productos': total_productos,
        'total_stock': total_stock,
        'productos_sin_stock': productos_sin_stock,
    }
    return render(request, 'inventario/dashboard.html', context)


# ========== FUNCIONALIDAD DE REMITOS DE SALIDA ==========

def lista_remitos(request):
    """Lista todos los remitos de salida"""
    remitos = RemitoSalida.objects.all().prefetch_related('detalles__producto')
    return render(request, 'inventario/lista_remitos.html', {'remitos': remitos})


def crear_remito(request):
    """Crear un nuevo remito de salida con sus detalles"""
    if request.method == 'POST':
        form = RemitoSalidaForm(request.POST)
        formset = DetalleSalidaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Crear el remito
                    remito = form.save()
                    
                    # Crear los detalles
                    formset.instance = remito
                    formset.save()
                    
                    messages.success(request, f'Remito {remito.id} creado correctamente')
                    return redirect('detalle_remito', remito_id=remito.id)
            except Exception as e:
                messages.error(request, f'Error al crear el remito: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
    else:
        form = RemitoSalidaForm()
        formset = DetalleSalidaFormSet()

    return render(request, 'inventario/crear_remito.html', {
        'form': form,
        'formset': formset
    })


def detalle_remito(request, remito_id):
    """Ver detalles de un remito específico"""
    remito = get_object_or_404(RemitoSalida, id=remito_id)
    detalles = remito.detalles.all().select_related('producto')
    
    return render(request, 'inventario/detalle_remito.html', {
        'remito': remito,
        'detalles': detalles
    })


def editar_remito(request, remito_id):
    """Editar un remito existente - solo si no se ha procesado"""
    remito = get_object_or_404(RemitoSalida, id=remito_id)
    
    if request.method == 'POST':
        form = RemitoSalidaForm(request.POST, instance=remito)
        formset = DetalleSalidaFormSet(request.POST, instance=remito)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    
                    # Manejar cambios en el formset
                    instances = formset.save(commit=False)
                    
                    # Eliminar detalles marcados para borrar
                    for obj in formset.deleted_objects:
                        obj.delete()
                    
                    # Guardar nuevos detalles
                    for instance in instances:
                        instance.save()
                    
                    messages.success(request, 'Remito actualizado correctamente')
                    return redirect('detalle_remito', remito_id=remito.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar el remito: {str(e)}')
    else:
        form = RemitoSalidaForm(instance=remito)
        formset = DetalleSalidaFormSet(instance=remito)
    
    return render(request, 'inventario/editar_remito.html', {
        'form': form,
        'formset': formset,
        'remito': remito
    })


def eliminar_remito(request, remito_id):
    """Eliminar un remito y devolver stock"""
    remito = get_object_or_404(RemitoSalida, id=remito_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Devolver el stock antes de eliminar
                for detalle in remito.detalles.all():
                    detalle.producto.cantidad += detalle.cantidad
                    detalle.producto.save()
                
                remito.delete()
                messages.success(request, 'Remito eliminado y stock restaurado')
                return redirect('lista_remitos')
        except Exception as e:
            messages.error(request, f'Error al eliminar el remito: {str(e)}')
    
    return render(request, 'inventario/confirmar_eliminar_remito.html', {
        'remito': remito
    })


def buscar_producto_ajax(request):
    """Búsqueda AJAX para productos (útil para seleccionar en remitos)"""
    from django.http import JsonResponse
    
    query = request.GET.get('q', '')
    if query:
        productos = Producto.objects.filter(
            nombre__icontains=query,
            cantidad__gt=0
        )[:10]
        
        results = [{
            'id': p.id,
            'text': f"{p.nombre} (Stock: {p.cantidad})",
            'stock': p.cantidad
        } for p in productos]
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})