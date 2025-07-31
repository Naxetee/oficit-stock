-- ================================================
-- 🗑️  SCRIPT DE LIMPIEZA COMPLETA DE BASE DE DATOS
-- ================================================
-- Este script elimina todos los registros de las tablas
-- respetando las relaciones de clave foránea.
--
-- ⚠️  ADVERTENCIA: Esta operación es IRREVERSIBLE
-- Asegúrate de tener un backup antes de ejecutar
-- ================================================

-- Desactivar temporalmente las restricciones de clave foránea
-- (opcional, para mayor control)
-- SET session_replication_role = replica;

BEGIN;

-- ================================================
-- PASO 1: Eliminar registros de tablas dependientes
-- (en orden inverso de dependencias)
-- ================================================

-- 1.1 Tabla: stock (depende de producto_simple y componente)
DELETE FROM stock 
WHERE EXISTS (SELECT 1 FROM stock);

-- 1.2 Tabla: componente_producto (depende de componente y producto_compuesto)
DELETE FROM componente_producto 
WHERE EXISTS (SELECT 1 FROM componente_producto);

-- 1.3 Tabla: pack_producto (depende de pack y producto)
DELETE FROM pack_producto 
WHERE EXISTS (SELECT 1 FROM pack_producto);

-- ================================================
-- PASO 2: Eliminar registros de tablas intermedias
-- ================================================

-- 2.1 Tabla: producto_simple (depende de producto, proveedor, color)
DELETE FROM producto_simple 
WHERE EXISTS (SELECT 1 FROM producto_simple);

-- 2.2 Tabla: producto_compuesto (depende de producto)
DELETE FROM producto_compuesto 
WHERE EXISTS (SELECT 1 FROM producto_compuesto);

-- 2.3 Tabla: pack (depende de articulo)
DELETE FROM pack 
WHERE EXISTS (SELECT 1 FROM pack);

-- 2.4 Tabla: producto (depende de articulo)
DELETE FROM producto 
WHERE EXISTS (SELECT 1 FROM producto);

-- ================================================
-- PASO 3: Eliminar registros de tablas principales
-- ================================================

-- 3.1 Tabla: componente (depende de proveedor, color)
DELETE FROM componente 
WHERE EXISTS (SELECT 1 FROM componente);

-- 3.2 Tabla: articulo (depende de familia)
DELETE FROM articulo 
WHERE EXISTS (SELECT 1 FROM articulo);

-- 3.3 Tabla: color (depende de familia)
DELETE FROM color 
WHERE EXISTS (SELECT 1 FROM color);

-- ================================================
-- PASO 4: Eliminar registros de tablas base
-- ================================================

-- 4.1 Tabla: proveedor (tabla independiente)
DELETE FROM proveedor 
WHERE EXISTS (SELECT 1 FROM proveedor);

-- 4.2 Tabla: familia (tabla base)
DELETE FROM familia 
WHERE EXISTS (SELECT 1 FROM familia);

-- ================================================
-- PASO 5: Reiniciar secuencias de IDs (opcional)
-- ================================================

-- Reiniciar contadores de auto-incremento
ALTER SEQUENCE familia_id_seq RESTART WITH 1;
ALTER SEQUENCE color_id_seq RESTART WITH 1;
ALTER SEQUENCE proveedor_id_seq RESTART WITH 1;
ALTER SEQUENCE articulo_id_seq RESTART WITH 1;
ALTER SEQUENCE componente_id_seq RESTART WITH 1;
ALTER SEQUENCE pack_id_seq RESTART WITH 1;
ALTER SEQUENCE producto_id_seq RESTART WITH 1;
ALTER SEQUENCE producto_simple_id_seq RESTART WITH 1;
ALTER SEQUENCE producto_compuesto_id_seq RESTART WITH 1;
ALTER SEQUENCE pack_producto_id_seq RESTART WITH 1;
ALTER SEQUENCE componente_producto_id_seq RESTART WITH 1;
ALTER SEQUENCE stock_id_seq RESTART WITH 1;

-- ================================================
-- VERIFICACIÓN FINAL
-- ================================================

-- Mostrar el conteo de registros en cada tabla después de la limpieza
SELECT 
    'familia' as tabla, COUNT(*) as registros FROM familia
UNION ALL SELECT 
    'color' as tabla, COUNT(*) as registros FROM color
UNION ALL SELECT 
    'proveedor' as tabla, COUNT(*) as registros FROM proveedor
UNION ALL SELECT 
    'articulo' as tabla, COUNT(*) as registros FROM articulo
UNION ALL SELECT 
    'componente' as tabla, COUNT(*) as registros FROM componente
UNION ALL SELECT 
    'pack' as tabla, COUNT(*) as registros FROM pack
UNION ALL SELECT 
    'producto' as tabla, COUNT(*) as registros FROM producto
UNION ALL SELECT 
    'producto_simple' as tabla, COUNT(*) as registros FROM producto_simple
UNION ALL SELECT 
    'producto_compuesto' as tabla, COUNT(*) as registros FROM producto_compuesto
UNION ALL SELECT 
    'pack_producto' as tabla, COUNT(*) as registros FROM pack_producto
UNION ALL SELECT 
    'componente_producto' as tabla, COUNT(*) as registros FROM componente_producto
UNION ALL SELECT 
    'stock' as tabla, COUNT(*) as registros FROM stock
ORDER BY tabla;

-- Reactivar las restricciones de clave foránea
-- SET session_replication_role = DEFAULT;

COMMIT;

-- ================================================
-- MENSAJE FINAL
-- ================================================
SELECT 'LIMPIEZA COMPLETADA EXITOSAMENTE' as resultado;
