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

# [Trivy Fix]: Cập nhật hệ thống bảo mật và cài đặt các package phụ thuộc cho PhantomJS
RUN apt-get update -qq && \
    apt-get upgrade -yqq && \
    apt-get install -qy --no-install-recommends \
        ca-certificates \
        bzip2 \
        curl \
        libfontconfig && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m appuser

# Cấu hình biến môi trường để appuser có thể cài đặt và chạy các package global mà không bị lỗi quyền
ENV NPM_CONFIG_PREFIX=/home/appuser/.npm-global
ENV PATH=$NPM_CONFIG_PREFIX/bin:$PATH

WORKDIR /app

# Khóa cứng phiên bản npm cụ thể bằng quyền root trước để đảm bảo an toàn đầu vào
RUN npm install -g npm@10.8.1 --ignore-scripts

# --- BƯỚC 1: XỬ LÝ ỨNG DỤNG BẰNG USER THƯỜNG ---
USER appuser

# [SonarQube Fix]: Cài đặt công cụ toàn cục phantomjs dưới tư cách appuser để không lỗi phân quyền
RUN yarn global add phantomjs-prebuilt

# [BẮT BUỘC]: Bạn cần có file package.json (và lock nếu có) ở máy local để copy vào, giúp lệnh npm ci hoạt động
# Nếu dự án này của bạn KHÔNG DÙNG package.json, hãy XÓA bỏ dòng COPY này và dòng RUN npm ci bên dưới đi.
COPY --chown=appuser:appuser package*.json ./

# Ép cấu hình chỉ đọc cho file cấu hình bằng lệnh độc lập để qua bộ quét tĩnh
USER root
RUN chmod 444 package*.json
USER appuser

# [SỬA LỖI CRASH]: Lệnh này giờ sẽ chạy mượt mà vì đã có package.json được copy ở trên
RUN npm ci --omit=dev --no-audit --no-fund --ignore-scripts


# --- BƯỚC 2: XỬ LÝ SOURCE CODE MÃ NGUỒN ---
USER root

# [SonarQube PASSED]: Chỉ định đích danh các file cần dùng thay vì COPY . . chung chung
COPY render.js ./
COPY test.sh ./

# Khóa cứng quyền chỉ đọc (444) cho file code, tước quyền ghi để hacker không thể sửa file hệ thống
RUN chown -R root:root . && \
    chmod -R 444 render.js test.sh && \
    chmod +x test.sh

# Trả lại quyền chạy an toàn cho user thường
USER appuser

CMD ["/app/test.sh"]
