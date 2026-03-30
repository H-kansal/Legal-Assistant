FROM python:3.10-slim

WORKDIR /app

# System deps (VERY IMPORTANT for your stack)
RUN apt-get update && apt-get install -y \
    build-essential \
    graphviz \
    libgraphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache optimization)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Environment settings
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 8000

# Run your app
CMD ["python", "app.py"]