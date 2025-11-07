FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html
COPY script.js /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80