# ----------------------------------------------------------------------
# DOCKERFILE PARA SERVICIO PYTHON (FastAPI + MySQL)
# ----------------------------------------------------------------------

ARG LANG_VERSION=3.12
FROM python:${LANG_VERSION}-slim

# Directorio de trabajo
WORKDIR /usr/src/app

# Copiar requirements primero (mejor cache)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Crear usuario no-root
RUN useradd -m pyuser \
 && chown -R pyuser:pyuser /usr/src/app

USER pyuser

# Exponer puerto interno
EXPOSE 80

# Comando por defecto — Uvicorn como servidor ASGI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
