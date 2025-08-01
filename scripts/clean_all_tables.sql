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
-- ================================================

-- Composicion_Prod.Compuesto (depende de Producto_Compuesto y Componente)
DELETE FROM "Composicion_Prod.Compuesto" WHERE EXISTS (SELECT 1 FROM "Composicion_Prod.Compuesto");

-- Composicion_Pack (depende de Pack y Producto)
DELETE FROM "Composicion_Pack" WHERE EXISTS (SELECT 1 FROM "Composicion_Pack");

-- ================================================
-- PASO 2: Eliminar registros de tablas intermedias
-- ================================================

-- Producto_Simple (depende de Producto, Proveedor, Color)
DELETE FROM "Producto_Simple" WHERE EXISTS (SELECT 1 FROM "Producto_Simple");

-- Producto_Compuesto (depende de Producto)
DELETE FROM "Producto_Compuesto" WHERE EXISTS (SELECT 1 FROM "Producto_Compuesto");

-- Pack (depende de Articulo)
DELETE FROM "Pack" WHERE EXISTS (SELECT 1 FROM "Pack");

-- Producto (depende de Articulo)
DELETE FROM "Producto" WHERE EXISTS (SELECT 1 FROM "Producto");

-- ================================================
-- PASO 3: Eliminar registros de tablas principales
-- ================================================

-- Componente (depende de Proveedor, Color)
DELETE FROM "Componente" WHERE EXISTS (SELECT 1 FROM "Componente");

-- Articulo (depende de Familia)
DELETE FROM "Articulo" WHERE EXISTS (SELECT 1 FROM "Articulo");

-- Color (depende de Familia)
DELETE FROM "Color" WHERE EXISTS (SELECT 1 FROM "Color");

-- ================================================
-- PASO 4: Eliminar registros de tablas base
-- ================================================

-- Proveedor (tabla independiente)
DELETE FROM "Proveedor" WHERE EXISTS (SELECT 1 FROM "Proveedor");

-- Familia (tabla base)
DELETE FROM "Familia" WHERE EXISTS (SELECT 1 FROM "Familia");

-- ================================================
-- PASO 5: Reiniciar secuencias de IDs (opcional)
-- ================================================

-- Reiniciar contadores de auto-incremento
ALTER SEQUENCE "Familia_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Color_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Proveedor_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Articulo_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Componente_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Pack_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Producto_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Producto_Simple_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Producto_Compuesto_id_seq" RESTART WITH 1;
ALTER SEQUENCE "Composicion_Pack_id_seq" RESTART WITH 1;
-- Si Composicion_Prod.Compuesto usa secuencia, añádela aquí:
-- ALTER SEQUENCE "Composicion_Prod.Compuesto_id_seq" RESTART WITH 1;

-- ================================================
-- VERIFICACIÓN FINAL
-- ================================================

SELECT 
    'Familia' as tabla, COUNT(*) as registros FROM "Familia"
UNION ALL SELECT 
    'Color' as tabla, COUNT(*) as registros FROM "Color"
UNION ALL SELECT 
    'Proveedor' as tabla, COUNT(*) as registros FROM "Proveedor"
UNION ALL SELECT 
    'Articulo' as tabla, COUNT(*) as registros FROM "Articulo"
UNION ALL SELECT 
    'Componente' as tabla, COUNT(*) as registros FROM "Componente"
UNION ALL SELECT 
    'Pack' as tabla, COUNT(*) as registros FROM "Pack"
UNION ALL SELECT 
    'Producto' as tabla, COUNT(*) as registros FROM "Producto"
UNION ALL SELECT 
    'Producto_Simple' as tabla, COUNT(*) as registros FROM "Producto_Simple"
UNION ALL SELECT 
    'Producto_Compuesto' as tabla, COUNT(*) as registros FROM "Producto_Compuesto"
UNION ALL SELECT 
    'Composicion_Pack' as tabla, COUNT(*) as registros FROM "Composicion_Pack"
UNION ALL SELECT 
    'Composicion_Prod.Compuesto' as tabla, COUNT(*) as registros FROM "Composicion_Prod.Compuesto"
ORDER BY tabla;

COMMIT;

-- ================================================
-- MENSAJE FINAL
-- ================================================
SELECT 'LIMPIEZA COMPLETADA EXITOSAMENTE' as resultado;
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
