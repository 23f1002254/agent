# Use Python 3.12 slim Bookworm base image
FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Install required Python packages
RUN pip install uv pandas numpy faker matplotlib seaborn scikit-learn

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
