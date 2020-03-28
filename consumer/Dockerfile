FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY consumer_app.py ./

ENTRYPOINT ["python", "-u", "/consumer_app.py"]