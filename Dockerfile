# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install required system packages (if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the .env file is present
COPY .env /app/.env

# Expose Flask (5000) and Streamlit (8501) ports
EXPOSE 5000
EXPOSE 8501

# Start both Flask and Streamlit services
CMD ["sh", "-c", "python app.py & streamlit run streamlit_app/main.py --server.port 8501 --server.address 0.0.0.0"]
