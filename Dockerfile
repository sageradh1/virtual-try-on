# # Stage 1: Build stage
# FROM python:3.10-slim AS builder

# # Set the working directory to /app
# WORKDIR /app

# # Copy only the necessary files for generating requirements.txt
# COPY pyproject.toml poetry.lock ./

# # Install Poetry
# RUN pip install poetry==1.8.2

# # Export the dependencies to requirements.txt
# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Production stage
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# # Copy requirements.txt from the builder stage
# COPY --from=builder /app/requirements.txt ./

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc g++
RUN pip install --upgrade pip
# Install dependencies from requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run run.py when the container launches
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=8080"]
