FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Build wheels for all requirements to speed up final install
RUN apt-get update && apt-get install -y build-essential && \
	pip wheel --no-cache-dir -w /wheels -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY . .
# Install from wheels produced in the builder stage
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

RUN chmod +x ./start.sh
EXPOSE 8000
ENV DATABASE_URL=sqlite:///./dev.db
CMD ["./start.sh"]
