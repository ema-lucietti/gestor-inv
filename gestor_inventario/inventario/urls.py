from django.urls import path
from .views import (
    # Vistas existentes
    cargar_producto, escanear_producto, imprimir_etiqueta, lista_pallets,
    crear_ubicacion, crear_pallet, detalle_ubicacion, lista_ubicaciones,
    dashboard,
    # Nuevas vistas de remitos
    lista_remitos, crear_remito, detalle_remito, editar_remito, 
    eliminar_remito, buscar_producto_ajax
)

urlpatterns = [
    # Rutas principales
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'), 
    
    # Productos
    path('cargar-producto/', cargar_producto, name='cargar_producto'),
    path('escanear/', escanear_producto, name='escanear_producto'),
    
    # Pallets y ubicaciones
    path('pallet/<int:pallet_id>/etiqueta/', imprimir_etiqueta, name='imprimir_etiqueta'),
    path('pallets/', lista_pallets, name='lista_pallets'),
    path('crear-ubicacion/', crear_ubicacion, name='crear_ubicacion'),
    path('crear-pallet/', crear_pallet, name='crear_pallet'),
    path('ubicacion/<int:ubicacion_id>/', detalle_ubicacion, name='detalle_ubicacion'),
    path('ubicaciones/', lista_ubicaciones, name='lista_ubicaciones'),
    
    # Remitos de salida
    path('remitos/', lista_remitos, name='lista_remitos'),
    path('remitos/crear/', crear_remito, name='crear_remito'),
    path('remitos/<int:remito_id>/', detalle_remito, name='detalle_remito'),
    path('remitos/<int:remito_id>/editar/', editar_remito, name='editar_remito'),
    path('remitos/<int:remito_id>/eliminar/', eliminar_remito, name='eliminar_remito'),
    
    # AJAX
    path('api/buscar-producto/', buscar_producto_ajax, name='buscar_producto_ajax'),
]