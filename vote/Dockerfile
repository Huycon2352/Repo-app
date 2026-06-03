# # base defines a base stage that uses the official python runtime base image
# FROM python:3.13-slim AS base

# # Add curl for healthcheck
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends curl && \
#     rm -rf /var/lib/apt/lists/*

# # Set the application directory
# WORKDIR /usr/local/app

# # Install our requirements.txt
# COPY requirements.txt ./requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # dev defines a stage for development, where it'll watch for filesystem changes
# FROM base AS dev
# RUN pip install watchdog
# ENV FLASK_ENV=development
# CMD ["python", "app.py"]

# # final defines the stage that will bundle the application for production
# FROM base AS final

# # Copy our code from the current folder to the working directory inside the container
# COPY . .

# # Make port 80 available for links and/or publish
# EXPOSE 80

# # Define our command to be run when launching the container
# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]

#v2 ( pass sonarq )

# base defines a base stage that uses the official python runtime base image
FROM python:3.11-slim AS base

# [Trivy Fix]: Cập nhật hệ thống và cài curl cho healthcheck (Gộp thành 1 layer)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/app

# [SonarQube Fix]: Copy file cấu hình gốc vào SỚM để phục vụ chuỗi lệnh RUN phía sau
COPY --chmod=444 requirements.in ./requirements.in

# [SonarQube PASSED]: Gộp toàn bộ lệnh khởi tạo User, cài pip-tools, dịch hash và cài đặt vào 1 Layer duy nhất!
RUN useradd -m appuser && \
    chown -R appuser /usr/local/app && \
    pip install --no-cache-dir pip-tools==7.4.1 --only-binary=:all: && \
    pip-compile --generate-hashes requirements.in && \
    pip install --no-cache-dir -r requirements.txt --only-binary=:all: --require-hashes


# dev defines a stage for development, where it'll watch for filesystem changes
FROM base AS dev
RUN pip install watchdog
ENV FLASK_ENV=development
CMD ["python", "app.py"]

# final defines the stage that will bundle the application for production
FROM base AS final

# Copy our code from the current folder to the working directory inside the container
COPY . .

# Make port 80 available for links and/or publish
EXPOSE 80

# Define our command to be run when launching the container
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
