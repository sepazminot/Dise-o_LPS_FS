# === Frontend Dockerfile (Multi-stage) ===
# Stage 1: Node/Vite build
FROM node:20-alpine AS node-builder

RUN corepack enable && corepack prepare pnpm@9.12.3 --activate

WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --no-frozen-lockfile

COPY src/ ./src/
COPY resources/ ./resources/
COPY postcss.config.js tailwind.config.js vite.config.js ./
RUN pnpm run build

# Stage 2: PHP Runtime with Octane (compatible base)
FROM php:8.3-cli-bookworm AS runtime

ENV PHP_OPCACHE_ENABLE=1 \
    PHP_OPCACHE_JIT=1255 \
    PHP_OPCACHE_JIT_BUFFER_SIZE=100M \
    OCTANE_SERVER=roadrunner

# Install system deps + PHP extensions commonly required by Laravel/Octane/roadrunner
# Se añade 'curl' que es necesario tanto para Octane/RoadRunner como para el HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends \
      git \
      unzip \
      zip \
      libpq-dev \
      libzip-dev \
      zlib1g-dev \
      libxml2-dev \
      libonig-dev \
      curl \
    && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-configure zip \
    && docker-php-ext-install -j"$(nproc)" \
         pdo \
         pdo_pgsql \
         pgsql \
         mbstring \
         xml \
         zip \
         bcmath \
         opcache \
         sockets \
         pcntl \
    && pecl install redis \          
    && docker-php-ext-enable redis

# Composer (for installing PHP deps at runtime)
COPY --from=composer:2.7 /usr/bin/composer /usr/bin/composer
ENV COMPOSER_ALLOW_SUPERUSER=1

RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /var/www/html

# Install PHP deps
COPY composer.json composer.lock* ./
COPY app/ ./app/
RUN composer install --no-dev --no-interaction --no-ansi --prefer-dist --no-scripts

# App code + assets
COPY --chown=app:app . .
COPY --from=node-builder --chown=app:app /app/public/build ./public/build

# Ensure required directories exist with proper permissions
RUN mkdir -p storage bootstrap/cache && \
    chown -R app:app storage bootstrap/cache && \
    chmod -R 775 storage bootstrap/cache

USER root
# === CAMBIO CLAVE AQUI ===
# Forzamos a que el binario de RoadRunner se descargue explícitamente usando el CLI oficial 
# de spiral y le asignamos los permisos correctos al usuario 'app'.
RUN composer require spiral/roadrunner-cli --no-interaction --no-ansi \
    && vendor/bin/rr get-binary \
    && chown app:app rr \
    && chmod +x rr

# Inicializamos la configuración de Octane
RUN php artisan octane:install --server=roadrunner --no-interaction

# Create .rr.yaml file to prevent permission issues at runtime
RUN touch /var/www/html/.rr.yaml && \
    chown app:app /var/www/html/.rr.yaml

USER app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:8080/health/live || exit 1

CMD ["php", "artisan", "octane:start", "--server=roadrunner", "--host=0.0.0.0", "--port=8080", "--workers=auto"]
#CMD ["./vendor/bin/rr", "serve", "-c", ".rr.yaml"]
