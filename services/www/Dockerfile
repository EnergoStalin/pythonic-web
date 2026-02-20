# syntax=docker/dockerfile:1
FROM nginx:stable-alpine3.23-perl
WORKDIR /www

COPY ./src/ .
COPY ./nginx/ /etc/nginx/conf.d/
