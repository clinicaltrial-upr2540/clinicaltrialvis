FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN apk --no-cache --update-cache add gcc gfortran build-base libpng freetype
RUN pip install --upgrade pip Cython
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
