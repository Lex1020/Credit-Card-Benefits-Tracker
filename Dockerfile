# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project directory to the container
COPY . /app/

# Ensure the `data/` directory exists inside the container
RUN mkdir -p /app/data

# Install dependencies from a requirements file
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variables to avoid Streamlit warnings
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_RUN_ON_SAVE=true \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app using 'sh -c' to avoid execution issues
CMD ["sh", "-c", "streamlit run /app/ccb.py --server.port=8501 --server.address=0.0.0.0"]
