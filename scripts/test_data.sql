DELETE FROM "Composicion_Pack";
DELETE FROM "Composicion_Prod.Compuesto";
DELETE FROM "Componente";
DELETE FROM "Producto_Compuesto";
DELETE FROM "Producto_Simple";
DELETE FROM "Producto";
DELETE FROM "Pack";
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
ALTER SEQUENCE IF EXISTS "Composicion_Pack_id_pack_seq" RESTART WITH 1;

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

-- Artículos (referencia a Familia)
INSERT INTO "Articulo" ("nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at") VALUES
('Articulo 1', 'Desc 1', 'A1', 1, TRUE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Articulo 2', 'Desc 2', 'A2', 2, TRUE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Articulo 3', 'Desc 3', 'A3', 3, FALSE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Packs (hereda de Artículo, añade todos los campos obligatorios)
INSERT INTO "Pack" (
    "id", "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at"
) VALUES
(1, 'Pack 1', 'Pack de prueba 1', 'P1', 1, TRUE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Pack 2', 'Pack de prueba 2', 'P2', 2, TRUE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Pack 3', 'Pack de prueba 3', 'P3', 3, FALSE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Productos (hereda de Artículo, añade todos los campos obligatorios)
INSERT INTO "Producto" (
    "id", "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at"
) VALUES
(1, 'Producto 1', 'Producto de prueba 1', 'PR1', 1, TRUE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Producto 2', 'Producto de prueba 2', 'PR2', 2, TRUE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Producto 3', 'Producto de prueba 3', 'PR3', 3, FALSE, 'pack', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Producto_Simple (hereda de Producto y Artículo, rellena todos los campos obligatorios)
INSERT INTO "Producto_Simple" (
    "id", "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at", "id_proveedor", "id_color"
) VALUES
(1, 'Producto Simple 1', 'Desc PS 1', 'PS1', 1, TRUE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, 1),
(2, 'Producto Simple 2', 'Desc PS 2', 'PS2', 2, TRUE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2, 2),
(3, 'Producto Simple 3', 'Desc PS 3', 'PS3', 3, FALSE, 'simple', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 3, 3);

-- Producto_Compuesto (hereda de Producto y Artículo, rellena todos los campos obligatorios)
INSERT INTO "Producto_Compuesto" (
    "id", "nombre", "descripcion", "codigo_tienda", "id_familia", "activo", "tipo", "created_at", "updated_at"
) VALUES
(2, 'Producto Compuesto 2', 'Desc PC 2', 'PC2', 2, TRUE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Producto Compuesto 3', 'Desc PC 3', 'PC3', 3, TRUE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Producto Compuesto 1', 'Desc PC 1', 'PC1', 1, FALSE, 'compuesto', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Componente (añade created_at y updated_at)
INSERT INTO "Componente" ("nombre", "descripcion", "id_proveedor", "id_color", "created_at", "updated_at") VALUES
('Comp A', 'Desc Comp A', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Comp B', 'Desc Comp B', 2, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Comp C', 'Desc Comp C', 3, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Composicion_Prod.Compuesto (referencia a Producto_Compuesto y Componente)
INSERT INTO "Composicion_Prod.Compuesto" ("id_producto_compuesto", "id_componente", "cantidad") VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 30);

-- Composicion_Pack (referencia a Pack y Producto)
INSERT INTO "Composicion_Pack" ("id_pack", "id_producto", "cantidad") VALUES
(1, 1, 5),
(2, 2, 10),
(3, 3, 15);
