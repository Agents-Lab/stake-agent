# Choose the base image with the appropriate Python version
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files and folders from the current directory to the container's working directory
ADD . .

# Specify the command to run your application (agent.py)
CMD ["python", "agent.py", "--port=$PORT"]