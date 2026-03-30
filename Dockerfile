# FROM python:3.10-slim

# WORKDIR /app

# # System deps (VERY IMPORTANT for your stack)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     graphviz \
#     libgraphviz-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements first (cache optimization)
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Copy full project
# COPY . .

# # Environment settings
# ENV PYTHONUNBUFFERED=1

# # Expose FastAPI port
# EXPOSE 8000

# # Run your app

FROM python:3.10-slim

WORKDIR /app

# Install only required system dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    libgraphviz-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Prevent Python from writing pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies (no cache → smaller image)
RUN pip install --no-cache-dir -r requirements.txt && \
rm -rf /root/.cache/pip

# Copy project files
COPY . .

# Pre-download small embedding model (avoids runtime delay)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Expose port
EXPOSE 8000

# Run FastAPI (PRODUCTION WAY)
CMD ["python", "app.py"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]