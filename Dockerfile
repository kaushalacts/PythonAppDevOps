# ---- Build stage ----
FROM python:3.9-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Final stage ----
FROM python:3.9-slim
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . /app

# Make sure pip-installed scripts/packages are on PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 80
ENTRYPOINT ["python", "app.py"]