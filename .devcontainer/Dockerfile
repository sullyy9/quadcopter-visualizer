FROM python:3.6-alpine

# Install basic programs and glibc.
RUN apk --no-cache add ca-certificates wget git build-base \
   && wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
	&& wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.33-r0/glibc-2.33-r0.apk \
	&& apk add glibc-2.33-r0.apk \
	&& rm glibc-2.33-r0.apk

# RUN pip install sip fbs PyQt5