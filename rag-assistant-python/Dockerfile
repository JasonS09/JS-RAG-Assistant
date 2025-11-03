FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ rag_assistant/

# Copy the scripts
COPY scripts/ scripts/

# Set the entry point for the application
CMD ["python", "rag_assistant/main.py"]