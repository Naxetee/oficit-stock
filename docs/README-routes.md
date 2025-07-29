# 🚀 Documentación de Endpoints - Sistema de Inventario Oficit

Esta documentación describe todos los endpoints disponibles en el sistema de inventario, organizados por modelo y funcionalidad.

## 📋 Índice

- [🏠 Endpoints del Sistema](#-endpoints-del-sistema)
- [🏷️ Familias](#️-familias)
- [🎨 Colores](#-colores)  
- [🏢 Proveedores](#-proveedores)
- [💰 Precios](#-precios)
- [📦 Artículos](#-artículos)
- [🔧 Componentes](#-componentes)
- [🏷️ Productos](#️-productos)
- [📦 Packs](#-packs)
- [📊 Stock](#-stock)
- [🎯 Inventario (Coordinador)](#-inventario-coordinador)
- [📝 Códigos de Estado HTTP](#-códigos-de-estado-http)
- [🔍 Ejemplos de Uso](#-ejemplos-de-uso)

---

## 🏠 Endpoints del Sistema

### Root y Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Estado del servicio y endpoints disponibles |
| `GET` | `/health` | Verificación de salud del sistema y BD |

**Ejemplo de respuesta Root:**
```json
{
  "servicio": "Oficit Stock Service",
  "version": "2.0.0",
  "estado": "✅ Activo",
  "endpoints_disponibles": {
    "familias": "/familias",
    "colores": "/colores",
    "proveedores": "/proveedores"
  }
}
```

---

## 🏷️ Familias

**Base URL:** `/familias`

### Endpoints CRUD Básicos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/familias/` | Crear nueva familia | `nombre`, `descripcion?` |
| `GET` | `/familias/` | Listar familias | `activo?`, `skip?`, `limit?` |
| `GET` | `/familias/{id}` | Obtener familia por ID | `id` |
| `PUT` | `/familias/{id}` | Actualizar familia | `id`, `nombre?`, `descripcion?` |
| `DELETE` | `/familias/{id}` | Eliminar familia | `id` |

### Endpoints Especializados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/familias/{id}/articulos` | Obtener artículos de una familia |
| `GET` | `/familias/{id}/colores` | Obtener colores de una familia |

**Ejemplo de creación:**
```json
POST /familias/
{
  "nombre": "Electrónicos",
  "descripcion": "Productos electrónicos diversos"
}
```

---

## 🎨 Colores

**Base URL:** `/colores`

### Endpoints CRUD Básicos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/colores/` | Crear nuevo color | `nombre`, `codigo_hex?`, `url_imagen?`, `id_familia?` |
| `GET` | `/colores/` | Listar colores | `activo?`, `id_familia?`, `skip?`, `limit?` |
| `GET` | `/colores/{id}` | Obtener color por ID | `id` |
| `PUT` | `/colores/{id}` | Actualizar color | `id`, `nombre?`, `codigo_hex?`, `url_imagen?`, `activo?`, `id_familia?` |
| `DELETE` | `/colores/{id}` | Eliminar color | `id` |

**Ejemplo de creación:**
```json
POST /colores/
{
  "nombre": "Rojo Intenso",
  "codigo_hex": "#FF0000",
  "url_imagen": "https://example.com/rojo.jpg",
  "id_familia": 1
}
```

---

## 🏢 Proveedores

**Base URL:** `/proveedores`

### Endpoints CRUD Básicos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/proveedores/` | Crear nuevo proveedor | `nombre`, `nif?`, `direccion?`, `telefono?`, `email?` |
| `GET` | `/proveedores/` | Listar proveedores | `activo?`, `skip?`, `limit?` |
| `GET` | `/proveedores/{id}` | Obtener proveedor por ID | `id` |
| `PUT` | `/proveedores/{id}` | Actualizar proveedor | `id`, `nombre?`, `nif?`, `direccion?`, `telefono?`, `email?`, `activo?` |
| `DELETE` | `/proveedores/{id}` | Eliminar proveedor | `id` |

### Endpoints Especializados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/proveedores/{id}/componentes` | Obtener componentes de un proveedor |

**Ejemplo de creación:**
```json
POST /proveedores/
{
  "nombre": "TechSupplier S.L.",
  "nif": "B12345678",
  "email": "contacto@techsupplier.es",
  "telefono": "912345678",
  "direccion": "Calle Ejemplo 123, Madrid"
}
```

---

## 💰 Precios

**Base URL:** `/precios`

### Precios de Compra

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/precios/compra` | Crear precio de compra | `valor`, `moneda?`, `fecha_inicio?`, `fecha_fin?` |
| `GET` | `/precios/compra` | Listar precios de compra | `vigente?`, `skip?`, `limit?` |
| `GET` | `/precios/compra/{id}` | Obtener precio de compra | `id` |
| `PUT` | `/precios/compra/{id}` | Actualizar precio de compra | `id`, `valor?`, `moneda?`, `fecha_inicio?`, `fecha_fin?` |

### Precios de Venta

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/precios/venta` | Crear precio de venta | `valor`, `moneda?`, `fecha_inicio?`, `fecha_fin?` |
| `GET` | `/precios/venta` | Listar precios de venta | `vigente?`, `skip?`, `limit?` |
| `GET` | `/precios/venta/{id}` | Obtener precio de venta | `id` |
| `PUT` | `/precios/venta/{id}` | Actualizar precio de venta | `id`, `valor?`, `moneda?`, `fecha_inicio?`, `fecha_fin?` |

**Ejemplo de creación:**
```json
POST /precios/compra
{
  "valor": 45.50,
  "moneda": "EUR",
  "fecha_inicio": "2025-01-01T00:00:00Z"
}
```

---

## 📦 Artículos

**Base URL:** `/articulos`

### Endpoints CRUD Básicos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/articulos/` | Crear nuevo artículo | `nombre`, `id_familia`, `descripcion?`, `sku?`, `id_precio_venta?` |
| `GET` | `/articulos/` | Listar artículos | `activo?`, `id_familia?`, `skip?`, `limit?` |
| `GET` | `/articulos/{id}` | Obtener artículo por ID | `id` |
| `PUT` | `/articulos/{id}` | Actualizar artículo | `id`, `nombre?`, `descripcion?`, `sku?`, `activo?`, `id_familia?`, `id_precio_venta?` |
| `DELETE` | `/articulos/{id}` | Eliminar artículo | `id` |

### Endpoints Especializados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/articulos/{id}/productos` | Obtener productos de un artículo |
| `GET` | `/articulos/{id}/packs` | Obtener packs de un artículo |
| `GET` | `/articulos/buscar/sku/{sku}` | Buscar artículo por SKU |

**Ejemplo de creación:**
```json
POST /articulos/
{
  "nombre": "Smartphone Pro",
  "descripcion": "Smartphone de alta gama",
  "sku": "SPH-PRO-001",
  "id_familia": 1,
  "id_precio_venta": 2
}
```

---

## 🔧 Componentes

**Base URL:** `/componentes`

### Endpoints CRUD Básicos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/componentes/` | Crear nuevo componente | `nombre`, `descripcion?`, `codigo?`, `especificaciones?`, `id_proveedor?`, `id_precio_compra?`, `id_color?` |
| `GET` | `/componentes/` | Listar componentes | `id_proveedor?`, `id_color?`, `skip?`, `limit?` |
| `GET` | `/componentes/{id}` | Obtener componente por ID | `id` |
| `PUT` | `/componentes/{id}` | Actualizar componente | `id`, `nombre?`, `descripcion?`, `codigo?`, `especificaciones?`, `id_proveedor?`, `id_precio_compra?`, `id_color?` |
| `DELETE` | `/componentes/{id}` | Eliminar componente | `id` |

**Ejemplo de creación:**
```json
POST /componentes/
{
  "nombre": "Pantalla LCD 5.5\"",
  "descripcion": "Pantalla LCD de alta resolución",
  "codigo": "LCD-55-HD",
  "especificaciones": "1920x1080, 60Hz",
  "id_proveedor": 1,
  "id_precio_compra": 3,
  "id_color": 2
}
```

---

## 🏷️ Productos

**Base URL:** `/productos`

### Productos Simples

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/productos/simple` | Crear producto simple | `id_articulo`, `especificaciones?`, `id_proveedor?`, `id_precio_compra?`, `id_color?` |

### Productos Compuestos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/productos/compuesto` | Crear producto compuesto | `id_articulo` |

### Endpoints Generales

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `GET` | `/productos/` | Listar productos | `tipo_producto?`, `id_articulo?`, `skip?`, `limit?` |
| `GET` | `/productos/{id}` | Obtener producto por ID | `id` |
| `DELETE` | `/productos/{id}` | Eliminar producto | `id` |

### Gestión de Componentes

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `GET` | `/productos/{id}/componentes` | Obtener componentes del producto | `id` |
| `POST` | `/productos/{id}/componentes/{componente_id}` | Agregar componente a producto | `id`, `componente_id`, `cantidad_necesaria` |

**Ejemplo de creación producto simple:**
```json
POST /productos/simple
{
  "id_articulo": 1,
  "especificaciones": "Modelo básico con 64GB",
  "id_proveedor": 1,
  "id_precio_compra": 5,
  "id_color": 2
}
```

---

## 📦 Packs

**Base URL:** `/packs`

### Endpoints CRUD Básicos

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/packs/` | Crear nuevo pack | `nombre`, `id_articulo`, `descripcion?` |
| `GET` | `/packs/` | Listar packs | `id_articulo?`, `skip?`, `limit?` |
| `GET` | `/packs/{id}` | Obtener pack por ID | `id` |
| `PUT` | `/packs/{id}` | Actualizar pack | `id`, `nombre?`, `descripcion?` |
| `DELETE` | `/packs/{id}` | Eliminar pack | `id` |

### Gestión de Productos en Packs

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `GET` | `/packs/{id}/productos` | Obtener productos del pack | `id` |
| `POST` | `/packs/{id}/productos/{producto_id}` | Agregar producto al pack | `id`, `producto_id`, `cantidad_incluida` |

**Ejemplo de creación:**
```json
POST /packs/
{
  "nombre": "Pack Inicio Smartphone",
  "descripcion": "Pack con smartphone, cargador y funda",
  "id_articulo": 1
}
```

---

## 📊 Stock

**Base URL:** `/stock`

### Creación de Stock

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/stock/producto/{producto_simple_id}` | Crear stock para producto | `producto_simple_id`, `cantidad_actual`, `cantidad_minima?`, `cantidad_maxima?`, `ubicacion_almacen?` |
| `POST` | `/stock/componente/{componente_id}` | Crear stock para componente | `componente_id`, `cantidad_actual`, `cantidad_minima?`, `cantidad_maxima?`, `ubicacion_almacen?` |

### Consultas de Stock

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `GET` | `/stock/` | Listar registros de stock | `bajo_minimo?`, `ubicacion?`, `skip?`, `limit?` |
| `GET` | `/stock/{id}` | Obtener stock por ID | `id` |

### Gestión de Stock

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `PUT` | `/stock/{id}/cantidad` | Actualizar cantidad de stock | `id`, `nueva_cantidad` |
| `POST` | `/stock/{id}/movimiento` | Registrar movimiento | `id`, `cantidad`, `tipo_movimiento`, `motivo?` |

### Alertas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/stock/alertas/bajo-minimo` | Obtener elementos con stock bajo |

**Ejemplo de creación stock:**
```json
POST /stock/producto/1
{
  "cantidad_actual": 100,
  "cantidad_minima": 20,
  "cantidad_maxima": 500,
  "ubicacion_almacen": "Almacén A - Estante 5"
}
```

**Ejemplo de movimiento:**
```json
POST /stock/1/movimiento
{
  "cantidad": 50,
  "tipo_movimiento": "entrada",
  "motivo": "Recepción de mercancía"
}
```

---

## 🎯 Inventario (Coordinador)

**Base URL:** `/inventario`

### Configuración Inicial

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/inventario/setup/completo` | Setup completo del inventario | `datos_setup` (objeto complejo) |

### Análisis y Reportes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/inventario/dashboard` | Datos del dashboard principal |
| `GET` | `/inventario/resumen/general` | Resumen general del inventario |
| `GET` | `/inventario/alertas` | Todas las alertas del inventario |

### Operaciones Complejas

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `POST` | `/inventario/producto/completo` | Crear producto con todos sus elementos | `datos_producto` |
| `POST` | `/inventario/pack/completo` | Crear pack completo | `datos_pack` |

### Consultas Avanzadas

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `GET` | `/inventario/buscar/avanzada` | Búsqueda avanzada | `termino`, `tipo_busqueda?`, `filtros?` |
| `GET` | `/inventario/analisis/costos` | Análisis de costos | `id_producto?`, `id_familia?` |
| `GET` | `/inventario/reporte/valoracion` | Reporte de valoración | `fecha_corte?` |

### Validación y Mantenimiento

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/inventario/validacion/integridad` | Validar integridad de datos |
| `POST` | `/inventario/mantenimiento/limpiar-huerfanos` | Limpiar registros huérfanos |
| `GET` | `/inventario/exportar/{formato}` | Exportar inventario (csv/excel/json) |

**Parámetros para exportar:**
- `formato`: Formato de exportación (csv, excel, json)
- `incluir_stock`: Incluir información de stock (opcional)
- `incluir_precios`: Incluir información de precios (opcional)

**Ejemplo de búsqueda avanzada:**
```json
GET /inventario/buscar/avanzada?termino=smartphone&tipo_busqueda=producto&filtros={"activo": true}
```

---

## 📝 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| `200` | OK - Operación exitosa |
| `201` | Created - Recurso creado exitosamente |
| `400` | Bad Request - Error en los datos enviados |
| `404` | Not Found - Recurso no encontrado |
| `500` | Internal Server Error - Error interno del servidor |

---

## 🔍 Ejemplos de Uso

### Flujo Completo: Crear Producto Simple

```bash
# 1. Crear familia
POST /familias/
{
  "nombre": "Smartphones",
  "descripcion": "Teléfonos inteligentes"
}

# 2. Crear color
POST /colores/
{
  "nombre": "Negro",
  "codigo_hex": "#000000",
  "id_familia": 1
}

# 3. Crear proveedor
POST /proveedores/
{
  "nombre": "TechProvider Inc.",
  "email": "contact@techprovider.com"
}

# 4. Crear precio de compra
POST /precios/compra
{
  "valor": 250.00,
  "moneda": "EUR"
}

# 5. Crear precio de venta
POST /precios/venta
{
  "valor": 399.00,
  "moneda": "EUR"
}

# 6. Crear artículo
POST /articulos/
{
  "nombre": "iPhone Pro",
  "sku": "IPH-PRO-001",
  "id_familia": 1,
  "id_precio_venta": 1
}

# 7. Crear producto simple
POST /productos/simple
{
  "id_articulo": 1,
  "especificaciones": "128GB, Dual SIM",
  "id_proveedor": 1,
  "id_precio_compra": 1,
  "id_color": 1
}

# 8. Crear stock
POST /stock/producto/1
{
  "cantidad_actual": 50,
  "cantidad_minima": 10,
  "cantidad_maxima": 200,
  "ubicacion_almacen": "Almacén Principal - A1"
}
```

### Consulta del Dashboard

```bash
GET /inventario/dashboard

# Respuesta esperada:
{
  "resumen": {
    "total_productos": 25,
    "total_componentes": 48,
    "valor_inventario": 15750.50,
    "alertas_stock": 3
  },
  "alertas": [
    {
      "tipo": "stock_bajo",
      "elemento": "iPhone Pro",
      "cantidad_actual": 8,
      "cantidad_minima": 10
    }
  ]
}
```

---

## 🛠️ Configuración de Desarrollo

Para probar estos endpoints:

1. **Iniciar el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Documentación interactiva:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

3. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## 🔧 Notas Técnicas

- **Autenticación:** Actualmente no implementada. Agregar middleware de autenticación según necesidades.
- **Paginación:** Implementada con parámetros `skip` y `limit`.
- **Filtros:** Disponibles en endpoints de listado con parámetros opcionales.
- **Validaciones:** Implementadas a nivel de servicio con manejo de errores personalizado.
- **Soft Delete:** Implementado donde aplique para mantener integridad referencial.

---

*📅 Última actualización: 29 de Julio, 2025*
*🔧 Versión de la API: 2.0.0*
