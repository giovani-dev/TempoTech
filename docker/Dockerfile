# Use a slim Python image for a smaller final image size
FROM python:3.10-slim

# Set environment variables for the application
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry for dependency management
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the port the application runs on
EXPOSE 8080

# Run the application using uvicorn, as specified in main.py
CMD ["poetry", "run", "uvicorn", "tempotech.api.main:app", "--host", "0.0.0.0", "--port", "8080"]