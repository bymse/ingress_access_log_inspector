FROM python:3.12-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc python3-dev

COPY requirements.txt .

RUN python3 -m pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.12-slim as app

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

RUN apt-get update && apt-get install libpq5 -y

COPY ./src ./src
RUN addgroup --system app && adduser --system --group app
USER app

ENTRYPOINT ["python", "-u", "./src/main.py"]