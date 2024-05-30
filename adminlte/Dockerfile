# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

# Install pip cache and virtualenv
RUN --mount=type=cache,id=s/659fd05a-bfea-40dd-961a-2b35fe8c58a1-/root/cache/pip,target=/root/.cache/pip \
    python -m venv /opt/venv

# Activate virtual environment and install Python packages
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Set environment variables for virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
COPY . /app/

# Expose the port (if needed, adjust to your application's needs)
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
