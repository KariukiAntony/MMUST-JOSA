FROM python:3.8-slim-buster

RUN mkdir /Josa

WORKDIR /Josa

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "5000"]