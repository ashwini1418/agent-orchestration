# ─── Stage 1: Dependencies ───────────────────────────────────────────────────
FROM node:20.18-alpine AS deps

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY packages/shared/package.json ./packages/shared/
COPY apps/frontend/package.json ./apps/frontend/

RUN pnpm install --frozen-lockfile

# ─── Stage 2: Builder ────────────────────────────────────────────────────────
FROM node:20.18-alpine AS builder

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/packages/shared/node_modules ./packages/shared/node_modules
COPY --from=deps /app/apps/frontend/node_modules ./apps/frontend/node_modules

COPY packages/shared/ ./packages/shared/
COPY apps/frontend/ ./apps/frontend/
COPY turbo.json ./

# Build args become VITE_ env vars at build time
ARG VITE_API_URL
ARG VITE_SOCKET_URL
ARG VITE_GOOGLE_CLIENT_ID
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_SOCKET_URL=$VITE_SOCKET_URL
ENV VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID

RUN pnpm --filter @taskflow/shared build
RUN pnpm --filter @taskflow/frontend build

# ─── Stage 3: Nginx production server ────────────────────────────────────────
FROM nginx:1.27-alpine AS runner

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY infrastructure/docker/nginx/nginx-frontend.conf /etc/nginx/conf.d/default.conf

# Copy built static files
COPY --from=builder /app/apps/frontend/dist /usr/share/nginx/html

# Security: run nginx as non-root
RUN chown -R nginx:nginx /usr/share/nginx/html \
    && chmod -R 755 /usr/share/nginx/html \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /var/log/nginx \
    && chown -R nginx:nginx /etc/nginx/conf.d \
    && touch /var/run/nginx.pid \
    && chown -R nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1
