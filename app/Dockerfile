FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./

COPY cookies.txt cookies.txt
CMD [ "python", "app" ]