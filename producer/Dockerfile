FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY producer_app.py ./

ENTRYPOINT ["python", "-u", "/producer_app.py"]
