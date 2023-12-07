# Use the official Python image
FROM python:3.10.0

# Set the working directory
WORKDIR /root/Hanime

# Copy the local files to the container
COPY . .

# Upgrade pip and setuptools
RUN pip3 install --upgrade pip setuptools

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_17.x | bash - && \
    apt-get install -y nodejs

# Install Python dependencies
RUN pip3 install -U -r requirements.txt

# Set the command to run your application
CMD ["python3", "-m", "Hanime"]
