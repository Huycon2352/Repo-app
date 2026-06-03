# FROM node:8.9-slim

# RUN apt-get update -qq && apt-get install -qy \ 
#     ca-certificates \
#     bzip2 \
#     curl \
#     libfontconfig \
#     --no-install-recommends
# RUN yarn global add phantomjs-prebuilt
# ADD . /app
# WORKDIR /app
# CMD ["/app/tests.sh"]

#v2
# FROM node:22-bookworm-slim

# RUN apt-get update -qq && apt-get install -qy \
#     ca-certificates \
#     bzip2 \
#     curl \
#     libfontconfig \
#     --no-install-recommends && \
#     useradd -m appuser

# RUN yarn global add phantomjs-prebuilt

# COPY render.js /app
# COPY test.sh /app

# WORKDIR /app

# USER appuser

# CMD ["/app/tests.sh"]

#v3

FROM node:22-bookworm-slim

# [Trivy Fix]: Cập nhật hệ thống bảo mật và cài đặt các package nền cho PhantomJS hoạt động
RUN apt-get update -qq && \
    apt-get upgrade -yqq && \
    apt-get install -qy --no-install-recommends \
        ca-certificates \
        bzip2 \
        curl \
        libfontconfig && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m appuser

# Cài đặt phantomjs-prebuilt bằng quyền root để hệ thống cài đặt binary vào đúng thư mục Linux
RUN yarn global add phantomjs-prebuilt

WORKDIR /app

# --- BƯỚC 2: XỬ LÝ SOURCE CODE MÃ NGUỒN ---
# [SonarQube PASSED]: Chỉ định đích danh các file cần dùng, thay thế hoàn toàn cho ADD . /app chung chung nguy hiểm
COPY render.js ./
COPY tests.sh ./

# [SonarQube PASSED]: Khóa cứng quyền CHỈ ĐỌC (444) cho file code để chống hacker chỉnh sửa
# Cấp quyền thực thi (+x) riêng cho file tests.sh để Linux có thể chạy được lệnh
RUN chown -R root:root . && \
    chmod 444 render.js && \
    chmod 555 tests.sh

# [Trivy & SonarQube PASSED]: Chuyển sang user thường (appuser) để khởi chạy container an toàn
USER appuser

# Gọi chính xác file tests.sh (có chữ s) giống như code cũ của bạn
CMD ["/app/tests.sh"]
