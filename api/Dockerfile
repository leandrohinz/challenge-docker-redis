# ---- Build Stage ----
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---- Run Stage ----
FROM python:3.9-slim AS runner

# Set the working directory in the container
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local /usr/local

# Copy the current directory contents into the container at /app
COPY . .

# Define environment variable
ENV FLASK_APP=main.py

# Run main.py when the container launches
CMD ["flask", "run", "--host","0.0.0.0"]