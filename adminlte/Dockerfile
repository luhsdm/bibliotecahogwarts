# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Create virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment and install dependencies
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set environment variables for virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port (if needed, adjust to your application's needs)
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
