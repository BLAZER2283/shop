FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install --upgrade pip setuptools wheel

# Install system build dependencies needed for some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

ENV DJANGO_SETTINGS_MODULE=app.settings
EXPOSE 8000

CMD ["gunicorn", "app.wsgi:application", "--bind", "127.0.0.1:8000"]
