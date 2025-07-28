# 🛠️ Arquitectura de Servicios - Sistema de Inventario

Este directorio contiene la arquitectura de servicios del sistema de inventario, organizados de manera modular y especializada.

## 📁 Estructura de Servicios

```
app/services/
├── __init__.py              # Importaciones centralizadas
├── base_service.py          # Clase base con funcionalidades comunes
├── familia_service.py       # Gestión de familias de productos
├── color_service.py         # Gestión de colores
├── proveedor_service.py     # Gestión de proveedores
├── precio_service.py        # Gestión de precios (venta y compra)
├── articulo_service.py      # Gestión de artículos
├── producto_service.py      # Gestión de productos (simples y compuestos)
├── componente_service.py    # Gestión de componentes
├── pack_service.py          # Gestión de packs
├── stock_service.py         # Gestión de inventario y stock
├── inventario_service.py    # Servicio coordinador principal
├── ejemplos.py              # Ejemplos de uso prácticos
└── README.md               # Esta documentación
```

## 🎯 Principios de Diseño

### 1. **Separación de Responsabilidades**
- Cada servicio se enfoca en un modelo o grupo de modelos relacionados
- Operaciones específicas del dominio están encapsuladas en su servicio correspondiente

### 2. **Reutilización de Código**
- `BaseService` proporciona operaciones CRUD comunes
- Métodos específicos del dominio se implementan en cada servicio

### 3. **Coordinación Centralizada**
- `InventarioService` actúa como coordinador para operaciones complejas
- Combina múltiples servicios para transacciones que involucran varias entidades

### 4. **Manejo de Errores Consistente**
- Logging estructurado en todos los servicios
- Manejo de transacciones con rollback automático en caso de error

## 🚀 Servicios Disponibles

### BaseService
Clase abstracta que proporciona:
- Operaciones CRUD básicas (crear, obtener, actualizar, eliminar)
- Métodos de búsqueda y filtrado
- Manejo de errores consistente
- Logging estructurado

### Servicios Especializados

| Servicio | Responsabilidad | Operaciones Principales |
|----------|----------------|------------------------|
| `FamiliaService` | Gestión de familias | CRUD, estadísticas, artículos asociados |
| `ColorService` | Gestión de colores | CRUD, búsqueda, validación hex |
| `ProveedorService` | Gestión de proveedores | CRUD, validación NIF/CIF, productos |
| `PrecioService` | Gestión de precios | CRUD precios venta/compra, históricos |
| `ArticuloService` | Gestión de artículos | CRUD, relaciones polimórficas |
| `ProductoService` | Gestión de productos | Simple/compuesto, componentes, validaciones |
| `ComponenteService` | Gestión de componentes | CRUD, integración con stock |
| `PackService` | Gestión de packs | CRUD, productos incluidos, descuentos |
| `StockService` | Gestión de inventario | Movimientos, alertas, resumen |
| `InventarioService` | Coordinador principal | Operaciones complejas, dashboard |

## 💡 Patrones de Uso

### 1. **Uso Individual**
Para operaciones específicas de un modelo:

```python
from app.services import FamiliaService

# Crear servicio específico
familia_service = FamiliaService(db_session)

# Operación específica
familia = familia_service.crear_familia(
    nombre="Electrónicos",
    descripcion="Productos electrónicos"
)
```

### 2. **Uso Coordinado**
Para operaciones que involucran múltiples entidades:

```python
from app.services import InventarioService

# Crear servicio coordinador
inventario = InventarioService(db_session)

# Operación compleja que coordina múltiples servicios
producto = inventario.crear_producto_simple_completo(
    nombre_articulo="Smartphone",
    precio_venta=299.99,
    precio_compra=150.00,
    stock_inicial=50
)
```

### 3. **Uso Combinado**
Para máxima flexibilidad:

```python
from app.services import InventarioService, StockService

inventario = InventarioService(db_session)
stock_service = StockService(db_session)

# Usar coordinador para crear producto
producto = inventario.crear_producto_simple_completo(...)

# Usar servicio específico para operación especializada
alertas = stock_service.obtener_stock_bajo_minimo()
```

## 🔧 Características Técnicas

### Manejo de Transacciones
- Cada operación se ejecuta en una transacción
- Rollback automático en caso de error
- Commit explícito para confirmar cambios

### Logging
- Logs estructurados con niveles apropiados
- Mensajes descriptivos con emojis para facilitar lectura
- Registro de errores con contexto completo

### Validaciones
- Validaciones de datos de entrada
- Verificación de integridad referencial
- Manejo de casos edge específicos del dominio

### Performance
- Consultas optimizadas con lazy loading apropiado
- Bulk operations para operaciones masivas
- Caché de resultados frecuentes (donde aplique)

## 📊 Ejemplo de Dashboard

El `InventarioService` proporciona un dashboard completo:

```python
dashboard = inventario.obtener_dashboard_inventario()

# Resultado:
{
    'resumen_stock': {
        'total_productos': 150,
        'valor_total': 25000.50,
        'productos_bajo_minimo': 5
    },
    'alertas_reposicion': 5,
    'total_familias': 8,
    'total_proveedores': 12,
    'total_articulos': 150,
    'productos_simples': 120,
    'productos_compuestos': 30
}
```

## 🔍 Búsqueda Global

Búsqueda integrada en todos los elementos del inventario:

```python
resultados = inventario.buscar_elementos_inventario("smartphone")

# Resultado:
{
    'familias': [...],
    'colores': [...],
    'proveedores': [...],
    'articulos': [...],
    'componentes': [...]
}
```

## 🚀 Cómo Empezar

1. **Importar servicios necesarios:**
```python
from app.services import InventarioService, ProductoService
```

2. **Crear instancia con sesión de BD:**
```python
inventario = InventarioService(db_session)
```

3. **Ejecutar operaciones:**
```python
producto = inventario.crear_producto_simple_completo(
    nombre_articulo="Mi Producto",
    precio_venta=99.99
)
```

## 📖 Ejemplos Completos

Ver el archivo `ejemplos.py` para casos de uso detallados:
- Uso de servicios individuales
- Operaciones coordinadas complejas
- Análisis y reportes avanzados

## 🔄 Extensibilidad

### Agregar Nuevo Servicio

1. **Crear clase heredando de BaseService:**
```python
from .base_service import BaseService
from app.models.mi_modelo import MiModelo

class MiModeloService(BaseService[MiModelo]):
    def __init__(self, db_session):
        super().__init__(db_session, MiModelo)
    
    def operacion_especifica(self):
        # Lógica específica del dominio
        pass
```

2. **Agregar al `__init__.py`:**
```python
from .mi_modelo_service import MiModeloService
__all__.append('MiModeloService')
```

3. **Integrar en InventarioService si es necesario:**
```python
self.mi_modelo_service = MiModeloService(db_session)
```

## 🛡️ Mejores Prácticas

### ✅ Hacer
- Usar el servicio coordinador para operaciones complejas
- Manejar errores específicos del dominio
- Implementar validaciones de negocio
- Usar logging descriptivo
- Mantener transacciones atómicas

### ❌ Evitar
- Acceder directamente a modelos desde controladores
- Operaciones de BD fuera de servicios
- Transacciones largas sin control
- Lógica de negocio en modelos
- Servicios con múltiples responsabilidades

---

**🎯 Esta arquitectura proporciona una base sólida, escalable y mantenible para el sistema de inventario, con separación clara de responsabilidades y reutilización máxima de código.**
