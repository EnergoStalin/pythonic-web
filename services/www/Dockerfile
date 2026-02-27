# syntax=docker/dockerfile:1
FROM nginx:stable-alpine3.23-perl
WORKDIR /www

COPY ./nginx/ /etc/nginx/conf.d/
COPY ./src/ .
