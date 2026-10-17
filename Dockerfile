FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR /app/Analysis

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn Analysis.wsgi:application --bind 0.0.0.0:8000 --workers 1 --timeout 120"]