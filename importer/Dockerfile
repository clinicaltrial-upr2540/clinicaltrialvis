FROM python:slim-buster
COPY . /import
WORKDIR /import

RUN apt update \
    && apt -y upgrade \
    && apt -y install r-base libxml2-dev libpq-dev unixodbc-dev libmariadbclient-dev \
    && pip install -r requirements.txt \
    && ./modules/install_dependencies.R

ENTRYPOINT [ "python" ]
CMD [ "database_setup.py" ]
