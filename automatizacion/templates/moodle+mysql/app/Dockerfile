# Imagen base oficial MoodleHQ con PHP + Apache
FROM moodlehq/moodle-php-apache:8.1-bullseye

USER root

# Dependencias adicionales mínimas
RUN apt-get update && apt-get install -y git unzip && rm -rf /var/lib/apt/lists/*

# --- NUEVA LÍNEA: Arregla el error de "Permission Denied" ---
RUN chmod -R 755 /usr/local/etc/php/conf.d
# ---------------------------------------------------------

# Argumento para rama/version Moodle
ARG MOODLE_BRANCH=MOODLE_405_STABLE

# Descargar Moodle dentro del contenedor
WORKDIR /var/www/html
RUN rm -rf ./* && \
    git clone -b ${MOODLE_BRANCH} --depth=1 https://github.com/moodle/moodle.git . && \
    rm -rf .git

# Crear carpeta moodledata dentro del contenedor
RUN mkdir -p /var/www/moodledata

# Permisos -> www-data
RUN chown -R www-data:www-data /var/www/html /var/www/moodledata && \
    find /var/www/html -type f -exec chmod 0644 {} \; && \
    find /var/www/html -type d -exec chmod 0755 {} \;

WORKDIR /var/www/html
