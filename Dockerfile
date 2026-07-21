# Use python base image
FROM python:3.13-slim-bullseye

# Update packages, install uuidgen, and clean up
RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
#update pip & install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# Set the timezone to Africa/Nairobi
RUN ln -sf /usr/share/zoneinfo/Africa/Nairobi /etc/localtime

EXPOSE 8000



# alembic upgrade head

# python -m scripts.seed_super_admin --name "Admin" --email admin@hmis.com --password "Admin@123"

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
