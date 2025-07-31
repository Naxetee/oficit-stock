# 📊 Modelos de Datos - Sistema de Inventario

Este directorio contiene todos los modelos de datos del sistema de inventario, implementados con SQLAlchemy ORM y optimizados con restricciones de integridad a nivel de base de datos.

## 🏗️ Arquitectura de Modelos

### **Modelos Principales**

#### 📦 **Familia** (`familia.py`)
- **Propósito**: Categorización de productos por familias
- **Campos**: `nombre`, `descripcion`
- **Relaciones**: Uno a muchos con `Articulo` y `Color`

#### 🎨 **Color** (`color.py`)
- **Propósito**: Variantes de color para productos y componentes
- **Campos**: `nombre`, `codigo_hex`, `url_imagen`, `id_familia`
- **Relaciones**: Muchos a uno con `Familia`

#### 🏪 **Proveedor** (`proveedor.py`)
- **Propósito**: Información de proveedores de productos y componentes
- **Campos**: `nombre`, `nif_cif`, `direccion`, `telefono`, `email`
- **Relaciones**: Uno a muchos con `ProductoSimple` y `Componente`

### **Modelos Centrales**

#### 📋 **Articulo** (`articulo.py`)
- **Propósito**: Entidad central que puede ser Producto o Pack
- **Campos**: `nombre`, `descripcion`, `codigo`, `id_familia`,
- **Relaciones**: 
  - Polimórfica con `Producto` y `Pack`
  - Muchos a uno con `Familia`

#### 📦 **Producto** (`producto.py`)
- **Propósito**: Productos que se venden (simples o compuestos)
- **Campos**: `tipo_producto`, `id_articulo`
- **Restricciones**: 
  - ✅ `tipo_producto IN ('simple', 'compuesto')` - Tipos válidos
- **Relaciones**: 
  - Uno a uno con `Articulo`
  - Polimórfica con `ProductoSimple` y `ProductoCompuesto`

#### 🔧 **ProductoSimple** (`producto_simple.py`)
- **Propósito**: Productos vendidos tal como se compran
- **Campos**: `especificaciones`, `id_proveedor` `id_color`
- **Relaciones**: 
  - Uno a uno con `Producto`
  - Muchos a uno con `Proveedor`, `Color`
  - Uno a uno con `Stock`

#### ⚙️ **ProductoCompuesto** (`producto_compuesto.py`)
- **Propósito**: Productos ensamblados a partir de componentes
- **Campos**: `descripcion_compuesto`
- **Relaciones**: 
  - Uno a uno con `Producto`
  - Muchos a muchos con `Componente` (a través de `ComponenteProducto`)

#### 🔩 **Componente** (`componente.py`)
- **Propósito**: Piezas necesarias para ensamblar productos compuestos
- **Campos**: `nombre`, `descripcion`, `codigo`, `especificaciones`, `unidad_medida`
- **Relaciones**: 
  - Muchos a uno con `Proveedor`, `Color`
  - Uno a uno con `Stock`
  - Muchos a muchos con `ProductoCompuesto` (a través de `ComponenteProducto`)

#### 📦 **Pack** (`pack.py`)
- **Propósito**: Conjunto de productos vendidos como una unidad
- **Campos**: `nombre`, `descripcion`, `descuento_porcentaje`, `activo`
- **Relaciones**: 
  - Uno a uno con `Articulo`
  - Muchos a muchos con `Producto` (a través de `PackProducto`)

### **Modelos de Relación (Many-to-Many)**

#### 🔗 **ComponenteProducto** (`componente_producto.py`)
- **Propósito**: Relación entre componentes y productos compuestos
- **Campos**: `cantidad_necesaria`, `id_componente`, `id_producto_compuesto`
- **Restricciones**: 
  - ✅ `cantidad_necesaria > 0` - Cantidades positivas
  - ✅ `UniqueConstraint` - Sin duplicados
- **Relaciones**: Muchos a uno con `Componente` y `ProductoCompuesto`

#### 🔗 **PackProducto** (`pack_producto.py`)
- **Propósito**: Relación entre packs y productos incluidos
- **Campos**: `cantidad_incluida`, `id_pack`, `id_producto`
- **Restricciones**: 
  - ✅ `cantidad_incluida > 0` - Cantidades positivas
  - ✅ `UniqueConstraint` - Sin duplicados
- **Relaciones**: Muchos a uno con `Pack` y `Producto`

### **Modelo de Inventario**

#### 🏬 **Stock** (`stock.py`)
- **Propósito**: Control de inventario físico
- **Campos**: `cantidad_actual`, `cantidad_minima`, `cantidad_maxima`, `ubicacion_almacen`
- **Restricciones**: 
  - ✅ `cantidad_actual >= 0` - No negativas
  - ✅ `cantidad_minima >= 0` - No negativas
  - ✅ `cantidad_maxima >= cantidad_minima` - Rango lógico
  - ✅ Relación exclusiva con `ProductoSimple` O `Componente`
- **Relaciones**: Uno a uno con `ProductoSimple` o `Componente` (exclusivo)

### **Servicio de Negocio**

#### 🎯 **InventarioService** (`inventario_service.py`)
- **Propósito**: Lógica de negocio centralizada
- **Funcionalidades**:
  - CRUD completo para todas las entidades
  - Gestión de stock con transacciones
  - Cálculo de costos de productos compuestos
  - Alertas de reposición
  - Validaciones de negocio

## 🛡️ Restricciones de Integridad Implementadas

### **Restricciones de Valor**
- Todos las cantidades son **positivas**
- Las fechas de fin son **posteriores** a las de inicio
- Los rangos de stock son **lógicos** (máximo >= mínimo)

### **Restricciones de Relación**
- Stock tiene relación **exclusiva** con ProductoSimple O Componente
- Producto debe ser **'simple' o 'compuesto'**
- Las relaciones many-to-many **no permiten duplicados**

### **Restricciones de Unicidad**
- `ComponenteProducto`: Un componente por producto compuesto
- `PackProducto`: Un producto por pack (sin repeticiones)
- Códigos únicos donde corresponde

## 📈 Diagrama de Relaciones

```
Familia ──┐
          ├── Articulo ──┬── Producto ──┬── ProductoSimple ── Stock
          │              │              └── ProductoCompuesto ──┐
Color ────┘              └── Pack ──────── PackProducto ─-──────┼── Producto
                                                                │
Proveedor ──┬── ProductoSimple                                  │
            └── Componente ── ComponenteProducto ───────-───────┘
                    │
                   Stock

```

## 🚀 Optimizaciones Implementadas

1. **Constructores SQLAlchemy**: Se eliminaron constructores personalizados innecesarios
2. **Restricciones DB**: Validaciones a nivel de base de datos para mejor rendimiento
3. **Índices**: Claves primarias y foráneas indexadas automáticamente
4. **Timestamps**: Control automático de creación y modificación
5. **Lazy Loading**: Relaciones optimizadas para consultas eficientes

## 📝 Uso con SQLAlchemy

### **Crear Instancias (sin constructores personalizados)**
```python
# Crear familia
familia = Familia(nombre="Sillas de Oficina", descripcion="Sillas ergonómicas")

# Crear producto con restricción automática
producto = Producto(tipo_producto="simple", id_articulo=1)  # Validado por CheckConstraint

# Crear stock con restricciones automáticas  
stock = Stock(
    cantidad_actual=100,    # >= 0 (validado)
    cantidad_minima=10,     # >= 0 (validado) 
    cantidad_maxima=500,    # >= cantidad_minima (validado)
    id_producto_simple=1    # Exclusivo con id_componente (validado)
)
```

### **Usando el Servicio de Inventario**
```python
from app.models.inventario_service import InventarioService

# Instanciar servicio
service = InventarioService(db_session)

# Crear producto compuesto completo
producto_compuesto = service.crear_producto_compuesto(
    nombre="Silla Ejecutiva Premium",
    descripcion="Silla ejecutiva con respaldo alto",
    familia_id=1
)

# Gestionar stock con alertas
service.actualizar_stock(producto_id=1, nueva_cantidad=150)
alertas = service.obtener_alertas_reposicion()  # Productos con stock bajo
```

## 🔧 Patrones Implementados

### **Patrón de Herencia**
- `Articulo` → `Producto` | `Pack` (polimorfismo)
- `Producto` → `ProductoSimple` | `ProductoCompuesto` (polimorfismo)

### **Patrón de Composición**
- `ProductoCompuesto` se compone de múltiples `Componente`
- `Pack` agrupa múltiples `Producto`

### **Patrón de Servicio**
- `InventarioService` centraliza la lógica de negocio
- Transacciones automáticas con rollback

## 📝 Convenciones de Código

- **Emojis en docstrings**: Para mejor legibilidad visual
- **Type hints completos**: En todos los métodos y atributos
- **Documentación exhaustiva**: Cada modelo y campo documentado
- **Nombres descriptivos**: Variables y métodos auto-explicativos
- **Separación de responsabilidades**: Modelos vs Servicios vs Controladores
- **Restricciones DB**: Validaciones a nivel de base de datos para máxima integridad
