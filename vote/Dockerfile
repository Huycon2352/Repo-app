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

#v2

# ==============================================================================
# STAGE 1: BASE - Định nghĩa môi trường nền sạch
# ==============================================================================
FROM python:3.13-slim AS base

# [Trivy Fix]: Cập nhật hệ thống và cài curl cho healthcheck
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/app

# [SonarQube Fix]: Tạo user non-root SỚM ở lớp base để các stage sau thừa kế
RUN useradd -m appuser && chown -R appuser /usr/local/app

# [SonarQube Fix]: Copy file requirements với quyền CHỈ ĐỌC (chmod 444), thuộc về root
COPY --chmod=444 requirements.txt ./requirements.txt

# [SonarQube Fix]: Ép pip chỉ cài file binary (.whl) từ file requirements đã khóa cứng version
RUN pip install --no-cache-dir -r requirements.txt --only-binary=:all:


# ==============================================================================
# STAGE 2: DEV - Môi trường dành cho lập trình viên (Watchdog)
# ==============================================================================
FROM base AS dev

# Chuyển sang quyền root tạm thời để cài tool dev nếu cần, hoặc chạy thẳng bằng root tùy cấu hình local mount
USER root

# [SonarQube Fix]: Khóa version cố định + Ép chỉ dùng file binary tĩnh (.whl)
RUN pip install --no-cache-dir watchdog==4.0.1 --only-binary=:all:

ENV FLASK_ENV=development

# Ở môi trường dev, thường bạn sẽ mount code từ máy tính vào, nên có thể giữ quyền root để không bị lệch UID
CMD ["python", "app.py"]


# ==============================================================================
# STAGE 3: FINAL - Bundle môi trường Production an toàn tuyệt đối
# ==============================================================================
FROM base AS final

# [SonarQube Fix]: Copy toàn bộ source code thuộc sở hữu của root, appuser CHỈ CÓ QUYỀN ĐỌC (chmod 444)
# Điều này chặn đứng hacker chạy lệnh bẻ khóa chmod nếu chúng chiếm được container
COPY --chmod=444 . .

# [SonarQube & Trivy Fix]: Kích hoạt user thường để chạy Gunicorn
USER appuser

# Khai báo Port chạy ứng dụng
EXPOSE 80

# Chạy Production bằng Gunicorn trực tiếp với tư cách appuser
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
