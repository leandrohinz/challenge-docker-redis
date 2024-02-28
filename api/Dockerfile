# Stage 1: Build dependencies
FROM python:3.9 AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port Flask is running on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "main.py"]