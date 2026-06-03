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

FROM node:22-bookworm-slim

RUN apt-get update -qq && apt-get install -qy \
    ca-certificates \
    bzip2 \
    curl \
    libfontconfig \
    --no-install-recommends && \
    useradd -m appuser

RUN yarn global add phantomjs-prebuilt

COPY . /app

WORKDIR /app

USER appuser

CMD ["/app/tests.sh"]
