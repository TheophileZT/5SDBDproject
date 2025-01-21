# Build image

FROM node:18 AS builder

WORKDIR /app

COPY package.json .

RUN npm ci
RUN npm install next

COPY . .

RUN npm run build

# Production image

FROM node:18

WORKDIR /app

COPY package.json .

RUN npm ci --only=production

COPY --from=builder /app/.next ./.next

COPY public ./public

EXPOSE 3000

CMD npm start