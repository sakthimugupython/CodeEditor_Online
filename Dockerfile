FROM python:3.11-slim

# Install system dependencies including Java and Node.js
RUN apt-get update && apt-get install -y \
    default-jdk \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn code_editor.wsgi:application --bind 0.0.0.0:$PORT"]
