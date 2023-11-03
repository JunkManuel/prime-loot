FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY *.py ./
COPY cookies.txt cookies.txt
CMD [ "python", "primelooter.py" , "-c cookies.txt" ]