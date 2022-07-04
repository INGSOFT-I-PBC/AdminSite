# Create MySQL for Django project test
FROM mysql
LABEL maintainer="labfernandez2014@gmail.com"

ENV MYSQL_ROOT_PASSWORD root

EXPOSE 3306
