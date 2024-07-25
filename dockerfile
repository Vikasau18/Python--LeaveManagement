# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /leavemanagement

# Copy the requirements file into the container
COPY requirement.txt .

# Install any dependencies
RUN pip install -r requirement.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=leavemanagement.settings
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for Django
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
