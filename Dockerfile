FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Collect static files (served by WhiteNoise)
RUN python manage.py collectstatic --noinput

# Directory for the SQLite database (mounted as a volume in compose)
RUN mkdir -p /app/data /app/mediafiles

# Expose the port Gunicorn will bind to
EXPOSE 8000

# Apply migrations on startup, then serve with Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn warranty_keeper.wsgi:application --bind 0.0.0.0:8000"]
