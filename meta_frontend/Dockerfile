FROM node:slim as builder
RUN mkdir /app && mkdir /app/openapi
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY openapi/openapi.json ./openapi/openapi.json
RUN npm run gen-api

COPY . .
RUN npm run build


FROM nginx:alpine-slim
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist/meta_frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY certs /etc/nginx/certs

EXPOSE 443 80
CMD ["nginx", "-g", "daemon off;"]

