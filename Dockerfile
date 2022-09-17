FROM python:3.10.0
ENV PYTHONUNBUFFERED = 1
WORKDIR /library_management
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /library_management/
