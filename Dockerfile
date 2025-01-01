FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will bind to
EXPOSE 8000

# Run Gunicorn with Django serving static files
CMD ["gunicorn", "warranty_keeper.wsgi:application", "--bind", "0.0.0.0:8000"]
