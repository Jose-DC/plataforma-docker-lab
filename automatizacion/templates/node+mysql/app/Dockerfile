# ----------------------------------------------------------------------
# DOCKERFILE PARA SERVICIO NODE.JS (Node + Express)
# Usa ARG LANG_VERSION, pasado desde el .env mediante el docker-compose.
# ----------------------------------------------------------------------

# Imagen base (versión tomada desde el .env)
# LANG_VERSION se sobrescribe desde docker-compose.yml (valor por defecto: 24)
ARG LANG_VERSION=24
FROM node:${LANG_VERSION}-alpine

# Directorio de trabajo
WORKDIR /usr/src/app

# Copiar package.json y lock
COPY package*.json ./

# Instalar dependencias
RUN npm install --production

# Copiar el resto de la aplicación
COPY . .

# Crear usuario no root
RUN adduser -D nodeuser \
 && chown -R nodeuser:nodeuser /usr/src/app

USER nodeuser

# Exponer puerto interno (80)
EXPOSE 80

# Comando por defecto
CMD ["npm", "start"]
