# FROM python:slim-buster
# COPY . /import
# WORKDIR /import

# RUN apt update \
#     && apt -y install r-base unixodbc odbc-postgresql unixodbc-dev libxml2-dev libpq-dev libmariadbclient-dev \
#     && pip install --no-cache-dir -r requirements.txt \
#     && ./modules/install_dependencies.R

# ENTRYPOINT [ "python", "-u" ]
# CMD [ "database_setup.py" ]



FROM r-base:latest
COPY . /import
WORKDIR /import

RUN echo "# deb http://snapshot.debian.org/archive/debian/20200422T000000Z bullseye main" > /etc/apt/sources.list \
    && echo "deb http://deb.debian.org/debian bullseye main" >> /etc/apt/sources.list \
    && apt update \
    && apt -y install python3 python3-pip libcurl4-openssl-dev libssl-dev libgit2-dev unixodbc-dev libxml2-dev libpq-dev libmariadbclient-dev postgresql-client \
    && pip3 install --no-cache-dir -r requirements.txt \
    && ./modules/install_dependencies.R \
    && apt clean

ENTRYPOINT [ "python3", "-u" ]
CMD [ "database_setup.py" ]



# FROM centos:latest
# COPY . /import
# WORKDIR /import

# RUN yum -y install epel-release dnf-plugins-core \
#     && yum config-manager --set-enabled PowerTools \
#     && yum -y update \
#     && yum -y install --nobest R python3 python3-pip libxml2-devel libpq-devel mariadb-devel openssl-devel libcurl-devel unixODBC-devel libgit2 \
#     && pip3 install --no-cache-dir -r requirements.txt \
#     && ./modules/install_dependencies.R \
#     && yum clean all

# ENTRYPOINT [ "python3", "-u" ]
# CMD [ "database_setup.py" ]
