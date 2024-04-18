FROM python:3.10-slim


WORKDIR /app
ENV PYTHONPATH=/app

COPY . /app/

RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:app", "--reload" ]

EXPOSE 8000