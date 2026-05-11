# ─── Stage 1: Dependencies ───────────────────────────────────────────────────
FROM node:20.18-alpine AS deps

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy workspace manifests
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY packages/shared/package.json ./packages/shared/
COPY apps/backend/package.json ./apps/backend/

# Install all dependencies (including dev — needed for build)
RUN pnpm install --frozen-lockfile

# ─── Stage 2: Builder ────────────────────────────────────────────────────────
FROM node:20.18-alpine AS builder

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy installed node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/packages/shared/node_modules ./packages/shared/node_modules
COPY --from=deps /app/apps/backend/node_modules ./apps/backend/node_modules

# Copy source files
COPY packages/shared/ ./packages/shared/
COPY apps/backend/ ./apps/backend/
COPY turbo.json ./

# Build shared package first, then backend
RUN pnpm --filter @taskflow/shared build
RUN pnpm --filter @taskflow/backend build

# Generate Prisma client
RUN pnpm --filter @taskflow/backend exec prisma generate

# ─── Stage 3: Production runner ───────────────────────────────────────────────
FROM node:20.18-alpine AS runner

# Security: run as non-root
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 taskflow

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy workspace manifests for production install
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY packages/shared/package.json ./packages/shared/
COPY apps/backend/package.json ./apps/backend/

# Production-only install
RUN pnpm install --frozen-lockfile --prod

# Copy built artifacts
COPY --from=builder /app/apps/backend/dist ./apps/backend/dist
COPY --from=builder /app/packages/shared/dist ./packages/shared/dist

# Copy Prisma schema + generated client
COPY --from=builder /app/apps/backend/prisma ./apps/backend/prisma
COPY --from=builder /app/apps/backend/node_modules/.prisma ./apps/backend/node_modules/.prisma
COPY --from=builder /app/apps/backend/node_modules/@prisma ./apps/backend/node_modules/@prisma

# Copy entrypoint script
COPY apps/backend/docker-entrypoint.sh ./apps/backend/docker-entrypoint.sh
RUN chmod +x ./apps/backend/docker-entrypoint.sh

# Set ownership
RUN chown -R taskflow:nodejs /app

USER taskflow

WORKDIR /app/apps/backend

EXPOSE 4000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD wget -qO- http://localhost:4000/health || exit 1

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["node", "dist/server.js"]
