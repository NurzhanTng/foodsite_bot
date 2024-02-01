FROM python:3.9

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ .

COPY main.py .

CMD python main.py
