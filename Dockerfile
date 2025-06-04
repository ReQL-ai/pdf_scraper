FROM python:3.11-slim

# System dependencies for Playwright
RUN apt-get update && apt-get install -y \
    curl wget unzip \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install Python packages and Playwright browsers
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install --with-deps

# Expose port
EXPOSE 8080

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
