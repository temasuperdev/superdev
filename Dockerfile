FROM python:3.12-slim

WORKDIR /app

# Install build/runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Ensure start script is executable
RUN chmod +x ./start.sh

EXPOSE 8000

ENV DATABASE_URL=sqlite:///./dev.db

CMD ["./start.sh"]
