FROM python:3.11-slim

WORKDIR /app

# Copy the built artifact produced by Jenkins and extract it
COPY todo-api-build.tar.gz .
RUN tar -xzf todo-api-build.tar.gz && rm todo-api-build.tar.gz

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]