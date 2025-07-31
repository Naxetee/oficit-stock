# 📦 Modelo de Datos: Gestión de Stock y Productos

Este documento describe el modelo entidad-relación diseñado para la gestión avanzada de stock, productos, componentes y packs en la empresa. El objetivo es ofrecer una estructura flexible, escalable y trazable para la digitalización de los procesos internos.

---

## 🗂️ Entidades

### 1. 🏷️ **Familia**
Agrupa y clasifica los artículos en categorías lógicas (por ejemplo: mesas, sillas, accesorios). Facilita la organización, búsqueda y análisis de productos.

### 2. 🎨 **Color**
Define los colores disponibles para productos simples y componentes, permitiendo gestionar variantes y opciones de personalización.

### 3. 🏢 **Proveedor**
Almacena la información de los proveedores que suministran productos simples y componentes. Es fundamental para la gestión de compras y relaciones comerciales.

### 4. 📄 **Artículo**
Entidad central que representa cualquier elemento gestionado en el inventario o vendido: producto, componente o pack. Se relaciona con familia.

### 5. 📦 **Producto**
Representa un producto final que se vende. Puede ser de tipo simple o compuesto.

### 6. 🪑 **Producto_Simple**
Producto que se vende tal cual, sin estar formado por otros componentes internos (por ejemplo, una silla comprada a un proveedor).

### 7. 🛠️ **Producto_Compuesto**
Producto que se ensambla a partir de varios componentes (por ejemplo, una mesa formada por tablero, patas y estructura).

### 8. 🔩 **Componente**
Partes individuales que se compran a proveedores y se utilizan para fabricar productos compuestos (por ejemplo, tablero, pata, tornillo).

### 9. 🎁 **Pack**
Conjunto de productos que se venden juntos como una oferta especial.

### 10. 🏬 **Stock**
Registra la cantidad disponible de productos simples y componentes en el almacén.

---

## 🔗 Relaciones

### 1. 📄 **Artículo – Familia**
Cada artículo pertenece a una familia, lo que permite su clasificación y organización.

### 2. 📦 **Producto – Artículo**
Cada producto está vinculado a un artículo, heredando su información general y permitiendo su gestión como elemento vendible.

### 3. 📦 **Producto – Producto_Simple**
Un producto puede ser de tipo simple, en cuyo caso se detalla en la entidad Producto_Simple.

### 4. 📦 **Producto – Producto_Compuesto**
Un producto puede ser de tipo compuesto, en cuyo caso se detalla en la entidad Producto_Compuesto.

### 5. 🪑 **Producto_Simple – Proveedor**
Cada producto simple puede estar asociado a un proveedor, indicando quién lo suministra.

### 6. 🪑 **Producto_Simple – Color**
Un producto simple puede estar disponible en varios colores, gestionando así las variantes de producto.

### 7. 🪑 **Producto_Simple – Stock**
Cada producto simple tiene su cantidad registrada en stock, permitiendo el control de inventario.

### 8. 🛠️ **Producto_Compuesto – Componente**
Un producto compuesto está formado por uno o varios componentes, especificando la cantidad necesaria de cada uno.

### 9. 🔩 **Componente – Proveedor**
Cada componente puede estar asociado a un proveedor, indicando quién lo suministra.

### 10. 🔩 **Componente – Color**
Un componente puede estar disponible en varios colores, gestionando así las variantes de componentes.

### 11. 🔩 **Componente – Stock**
Cada componente tiene su cantidad registrada en stock, permitiendo el control de inventario de materiales.

### 12. 🎁 **Pack – Artículo**
Cada pack está vinculado a un artículo, permitiendo su gestión como elemento vendible.

### 13. 🎁 **Pack – Producto**
Un pack está formado por uno o varios productos, especificando la cantidad de cada uno.

---

## 📝 Notas adicionales

- El modelo permite la trazabilidad completa de cada producto, desde la compra de componentes hasta la venta final.
- La estructura es flexible y permite añadir nuevas variantes, proveedores, colores o familias sin afectar la integridad del sistema.

---