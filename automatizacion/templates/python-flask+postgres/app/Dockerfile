# ----------------------------------------------------------------------
# DOCKERFILE PARA SERVICIO PYTHON (Flask + PostgreSQL)
# Usa ARG LANG_VERSION, pasado desde el .env mediante el docker-compose.
# ----------------------------------------------------------------------

# Imagen base: versión definida en .env
ARG LANG_VERSION=3.12
FROM python:${LANG_VERSION}-slim

# Directorio de trabajo
WORKDIR /usr/src/app

# Copiar requirements primero (cache eficiente)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la app
COPY . .

# Crear usuario no root (igual que las otras plantillas)
RUN useradd -m pyuser \
 && chown -R pyuser:pyuser /usr/src/app

USER pyuser

# Exponer puerto interno (80)
EXPOSE 80

# Comando por defecto
CMD ["python", "main.py"]
