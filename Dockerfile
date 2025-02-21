# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy application files to the container
COPY ccb.py /app/

# Install dependencies
RUN pip install --no-cache-dir streamlit matplotlib

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app with the correct file name
CMD ["streamlit", "run", "/app/ccb.py", "--server.port=8501", "--server.address=0.0.0.0"]
