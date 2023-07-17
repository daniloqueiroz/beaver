# Use the official Python image as the base image
FROM python:3.11-alpine
run pip install --upgrade pip 

# Set the working directory inside the container
WORKDIR /app

# Copy the Python requirements file (if you have one) and install dependencies
COPY pyproject.toml ./
RUN pip install .

# Copy the entire current directory (including the Python app code) into the container at /app
COPY src/ .

# Expose the port your Python app is listening on (if applicable)
EXPOSE 8000

# Command to run your Python app (replace "app.py" with your actual Python script name)
CMD ["uvicorn", "main:app", "--reload"]
