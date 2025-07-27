Funcionalidades principales:
📦 Gestión de Inventario

Ubicaciones: Lugares físicos donde se almacenan los pallets
Pallets: Contenedores que agrupan productos
Productos: Items individuales con código de barras, nombre y cantidad

📋 Remitos de Salida

Crear remitos para registrar salidas de mercadería
Detalles de salida que descuentan automáticamente del stock
Control de stock insuficiente
Historial de movimientos

🖥️ Interfaz de Usuario

Dashboard con estadísticas
Carga y escaneo de productos
Listas y filtros por ubicación
Impresión de etiquetas
Búsqueda AJAX

Estructura del Sistema:
Ubicación → Pallet → Productos
                ↓
         Remitos de Salida → Detalles de Salida
Características destacadas:
✅ Control de Stock: Los remitos automáticamente descuentan del inventario
✅ Validaciones: Evita salidas con stock insuficiente
✅ Transacciones: Uso de transaction.atomic() para consistencia
✅ Admin Panel: Configurado para gestión administrativa
✅ Formularios Dinámicos: FormSets para múltiples productos por remito
 
 ¿Cómo usarlo?

Escaneás productos desde http://localhost:8000/escanear/

Se guardan en un pallet.

Vas a http://localhost:8000/pallet/1/etiqueta/ (reemplazá el 1 con el ID de tu pallet) y generás la etiqueta con botón de impresión.

----

Cuando vayas a http://localhost:8000/pallets/ vas a ver una lista de todos los pallets, con un botón para imprimir la etiqueta directamente (abre en nueva pestaña para poder imprimir sin salir de la lista).

---
