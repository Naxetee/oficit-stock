DELETE FROM "Composicion_Pack";
DELETE FROM "Composicion_Prod_Compuesto";
DELETE FROM "Stock";
DELETE FROM "Movimiento";
DELETE FROM "Componente";
DELETE FROM "Pack";
DELETE FROM "Producto_Simple";
DELETE FROM "Producto_Compuesto";
DELETE FROM "Producto";
DELETE FROM "Articulo";
DELETE FROM "Proveedor";
DELETE FROM "Color";
DELETE FROM "Familia";

-- Resetear las secuencias (PostgreSQL)
ALTER SEQUENCE IF EXISTS "Componente_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Proveedor_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Color_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Familia_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Articulo_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Pack_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Stock_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "Movimiento_id_seq" RESTART WITH 1;

-- Familias (debe ir primero)
INSERT INTO "Familia" ("id", "nombre", "descripcion", "created_at", "updated_at") VALUES
(1, 'Familia A', 'Descripción A', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Familia B', 'Descripción B', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Familia C', 'Descripción C', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Colores (referencia a Familia, los id_familia deben existir)
INSERT INTO "Color" ("nombre", "hex", "url_imagen", "id_familia", "created_at", "updated_at") VALUES
('Rojo', '#FF0000', 'url_rojo.png', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Verde', '#00FF00', 'url_verde.png', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Azul', '#0000FF', 'url_azul.png', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Proveedores (corrige para que todos los campos requeridos tengan valor)
INSERT INTO "Proveedor" ("nombre", "telefono", "email", "direccion", "activo", "created_at", "updated_at") VALUES
('Proveedor Uno', '111111111', 'uno@proveedor.com', 'Calle Uno', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Proveedor Dos', '222222222', 'dos@proveedor.com', 'Calle Dos', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Proveedor Tres', '333333333', 'tres@proveedor.com', 'Calle Tres', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Packs (hereda de Artículo, añade todos los campos obligatorios)
INSERT INTO "Pack" (
    "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at"
) VALUES
('Pack 1', 'Pack de prueba 1', 'P1', 1, TRUE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Pack 2', 'Pack de prueba 2', 'P2', 2, TRUE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Pack 3', 'Pack de prueba 3', 'P3', 3, FALSE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Producto_Simple (hereda de Producto y Artículo, rellena todos los campos obligatorios)
INSERT INTO "Producto_Simple" (
    "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at", "id_proveedor", "id_color"
) VALUES
('Producto Simple 1', 'Desc PS 1', 'PS1', 1, TRUE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, 1),
('Producto Simple 2', 'Desc PS 2', 'PS2', 2, TRUE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2, 2),
('Producto Simple 3', 'Desc PS 3', 'PS3', 3, FALSE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 3, 3);

-- Producto_Compuesto (hereda de Producto y Artículo, rellena todos los campos obligatorios)
INSERT INTO "Producto_Compuesto" (
    "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at"
) VALUES
('Producto Compuesto 2', 'Desc PC 2', 'PC2', 2, TRUE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Producto Compuesto 3', 'Desc PC 3', 'PC3', 3, TRUE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Producto Compuesto 1', 'Desc PC 1', 'PC1', 1, FALSE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Componente (añade created_at y updated_at)
INSERT INTO "Componente" ("nombre", "descripcion", "id_proveedor", "id_color", "created_at", "updated_at") VALUES
('Comp A', 'Desc Comp A', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Comp B', 'Desc Comp B', 2, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Comp C', 'Desc Comp C', 3, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Composicion_Prod_Compuesto (referencia a Producto_Compuesto y Componente)
INSERT INTO "Composicion_Prod_Compuesto" ("id_producto_compuesto", "id_componente", "cantidad") VALUES
(7, 1, 3),
(7, 2, 1),
(8, 2, 5),
(9, 3, 2),
(9, 1, 1);

-- Composicion_Pack (referencia a Pack y Producto)
INSERT INTO "Composicion_Pack" ("id_pack", "id_producto", "cantidad") VALUES
(1, 4, 5),
(2, 6, 10),
(3, 8, 15);

-- Insertar datos en Stock (con tipo, id_componente e id_producto_simple)
INSERT INTO "Stock" (
    "cantidad", "cantidad_minima", "ubicacion", "tipo", "id_componente", "id_producto_simple", "created_at", "updated_at"
) VALUES
(2, 20, 'Almacen A', 'producto_simple', NULL, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(50, 5, 'Almacen B', 'componente', 1, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(200, 20, 'Almacen C', 'producto_simple', NULL, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(25, 30, 'Almacen D', 'componente', 2, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(150, 15, 'Almacen E', 'producto_simple', NULL, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(17, 20, 'Almacen F', 'componente', 3, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- -- Insertar datos en Movimiento (con id_articulo)
-- INSERT INTO "Movimiento" (
--     "id_producto_simple", "id_componente" , "tipo", "cantidad", "descripcion", "created_at", "updated_at"
-- ) VALUES
-- (4, NULL, 'entrada', 10, 'Entrada de stock PS1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- (5, NULL, 'salida', 5, 'Salida de stock PS2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- (6, NULL, 'entrada', 20, 'Entrada de stock PS3', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- (NULL, 1, 'entrada', 15, 'Entrada de stock Comp A', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- (NULL, 2, 'salida', 10, 'Salida de stock Comp B', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
-- (NULL, 3, 'entrada', 25, 'Entrada de stock Comp C', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

