FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /TransactionsApi

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /TransactionsApi/DjangoApp

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
