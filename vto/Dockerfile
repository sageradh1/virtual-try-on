FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install Poetry
RUN pip install poetry==1.8.2

# Install dependencies using Poetry
RUN poetry install

# Set the entry point to your app.py
ENTRYPOINT ["poetry", "run", "python", "vto/app.py"]
