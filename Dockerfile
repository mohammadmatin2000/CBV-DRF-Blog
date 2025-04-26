# Use the official Python runtime image
FROM python:3.8-buster



# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/

# Upgrade pip
RUN pip install --upgrade pip

# run this command to install all dependencies
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY . /core/app

