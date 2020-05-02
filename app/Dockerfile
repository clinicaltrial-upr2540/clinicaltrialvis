FROM python:alpine3.8
COPY . /app
WORKDIR /app

RUN buildDeps='gcc gfortran build-base libpng freetype wget freetype-dev libpng-dev openblas-dev' \
    && set -x \
    && apk --no-cache --update-cache add $buildDeps \
    && pip install --upgrade pip Cython \
    && pip install -r requirements.txt \
    && apk del $buildDeps

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
