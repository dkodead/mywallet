FROM python:3.11-slim

WORKDIR /app

# Copy repository into container
COPY ./wallet_dkoded /app/wallet_dkoded

# Install Python dependencies
COPY ./wallet_dkoded/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "wallet_dkoded.apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
