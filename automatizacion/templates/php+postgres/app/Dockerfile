# ----------------------------------------------------------------------
# DOCKERFILE PARA EL SERVICIO PHP (versión PostgreSQL)
# Construye la imagen base del contenedor de aplicación PHP.
# Está pensada para ser flexible: el desarrollador puede agregar
# dependencias o herramientas según su necesidad.
# ----------------------------------------------------------------------

# Imagen base: PHP con Apache (la versión se define en el .env)
# LANG_VERSION se sobrescribe desde docker-compose.yml (valor por defecto: 24)
ARG LANG_VERSION=8.3
FROM php:${LANG_VERSION}-apache

# Asegurarse de que /tmp tiene los permisos correctos
RUN chmod 1777 /tmp

# Instala dependencias necesarias para librerías gráficas y de base de datos
# (GD = imágenes, PDO = conexión a MySQL)
RUN apt-get update && apt-get install -y \
      libpng-dev libjpeg-dev libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql

# Copia el contenido de la carpeta local "app" al contenedor
WORKDIR /var/www/html
COPY . .

# Cambiar permisos de los archivos dentro del contenedor
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# Fix de ServerName para evitar warnings
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expone el puerto 80 (interno) para que el proxy acceda a la app
EXPOSE 80
