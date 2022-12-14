FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y python3-pip build-essential libffi-dev python-dev

RUN pip3 install flask pynacl
RUN pip3 install ecdsa
RUN pip install requests
# RUN npm install @mui/material @emotion/react @emotion/styled
# RUN npm install @mui/icons-material

WORKDIR /shared

# EXPOSE 5000