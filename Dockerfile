# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

COPY . /app

# Install pip requirements
#COPY requirements.txt /app
RUN pip install -r requirements.txt

# WORKDIR /app
#COPY . /app

# RUN echo "$JWT_PUBLIC_KEY" > /app/backend/storage/jwt/public.pem && \
#     echo "$JWT_PRIVATE_KEY" > /app/backend/storage/jwt/private.pem

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
