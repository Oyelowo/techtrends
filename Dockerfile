FROM python:3.9

WORKDIR /app

COPY ./src .

RUN pip install -r requirements.txt

EXPOSE 3111

CMD [ "python", "./app.py" ]
