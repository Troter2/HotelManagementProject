FROM python:3.12-slim

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory
WORKDIR /app

# Install dependencies using pip
RUN pip install -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
