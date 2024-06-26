# parent image
FROM python:3.9.4-slim

# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install libgl1-mesa-glx libglib2.0-0 -y \
 && apt-get install --reinstall build-essential -y \
 && rm -rf /var/lib/apt/lists/* \
 && echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


# install wkhtmltopdf
RUN apt-get update \
 && apt-get install -y wget \
 && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
 && apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb \
 && rm wkhtmltox_0.12.6-1.buster_amd64.deb
# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt .
# install pyodbc (and, optionally, sqlalchemy)
RUN pip install   -r requirements.txt  && rm -rf /root/.cache 
COPY . .
# Instala la utilidad ping
RUN apt-get update && apt-get install -y iputils-ping &&  apt-get install -y openssh-client
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]



