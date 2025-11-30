web: gunicorn recommendationSystem.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --threads 2 --worker-class gthread --max-requests 1000 --max-requests-jitter 50
