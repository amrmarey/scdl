# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app
COPY ./index.html /app
COPY ./server.py /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Create Download folder to support download 
RUN mkdir -p /app/downloads && chmod -R 777 /app/downloads

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
