# Step 1: Use an official lightweight Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set environment variables to keep Python clean
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the dependencies file first to leverage Docker caching
COPY requirements.txt /app/

# Step 5: Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of your local application code into the container
COPY . /app/

# Step 7: Expose the port Flask will run on (5000 is standard)
EXPOSE 5000


# Step 8: Define the command to run your app using Gunicorn (Production Server)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT run:app"]