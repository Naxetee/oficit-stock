# 🏢 Oficit Stock Service

Microservicio para la gestión avanzada de stock, productos, componentes, packs y proveedores de Tienda Oficit SL.

## 🚀 Descripción general

Este proyecto es el primer microservicio del sistema de digitalización interna de Tienda Oficit SL. Permite gestionar el inventario, la composición de productos, los packs y los proveedores, con una estructura flexible y escalable.

- Arquitectura orientada a microservicios
- Gestión detallada de stock y trazabilidad de componentes
- Preparado para integrarse con otros servicios (pedidos, facturación, etc.)

## 🏗️ Arquitectura y tecnologías

- 🐍 **Python**  
  Lenguaje principal para el desarrollo del backend.

- ⚡ **FastAPI**  
  Framework moderno y rápido para la creación de APIs, ideal para microservicios. [FastAPI](https://fastapi.tiangolo.com/)

- 🛠️ **FastAPI-Admin**  
  Panel de administración listo para usar, integrado con FastAPI para gestionar entidades de stock, productos, componentes y más.

- 🔗 **GraphQL**  
  API flexible para consultas y mutaciones avanzadas, implementada sobre FastAPI (usando [Strawberry GraphQL](https://strawberry.rocks/))

- 🐘 **PostgreSQL**  
  Base de datos relacional robusta y escalable usando [PostGreSQL](https://www.postgresql.org/), perfecta para modelos de datos complejos.

- 🐳 **Docker** 
  Para facilitar el despliegue y la portabilidad del servicio.

- 🧰 **ORM**  
  [SQLAlchemy](https://www.sqlalchemy.org/) para el mapeo de modelos a la base de datos.

- 📝 **Documentación**  
  Documentación automática de la API con Swagger/OpenAPI y Code Playground de GraphQL. Además de Markdown para guías y DRAW.IO para diagramas.

## 📚 Documentación

- [Modelo de datos y diagrama ER](docs/diagram/README-diagram.md)
- [Guía de instalación y uso](docs/INSTALL.md)

## 🔒 Licencia y uso

> ⚠️ **Este software es propiedad de Tienda Oficit SL. Queda prohibida su copia, distribución o uso fuera de la empresa sin autorización expresa.**

## 👥 Colaboradores

- Ignacio Ávila Reyes [@Naxetee](https://github.com/Naxetee)

## 🛡️ Buenas prácticas

- **No subas datos sensibles ni archivos de base de datos.**
- Usa archivos `.env` para credenciales y agrégalos a `.gitignore`.
- Mantén la documentación y los diagramas actualizados.
- Usa ramas y mensajes de commit claros.

## 🛠️ Instalación rápida

Sigue la guía de instalación en [INSTALL.md](docs/INSTALL.md) para configurar el entorno de desarrollo y producción.