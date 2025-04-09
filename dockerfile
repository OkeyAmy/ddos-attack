FROM python:3.12.0

WORKDIR /app

# Copy only the requirements first to leverage Docker layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining files after installing dependencies
COPY app.py .
COPY models/ ./models/

# Run the app with Uvicorn on port 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
