FROM nvidia/cuda:7.5-devel-ubuntu14.04
MAINTAINER Yigit Ozen

ADD optix /usr/local/optix
ENV LD_LIBRARY_PATH /usr/local/optix/lib64:${LD_LIBRARY_PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential software-properties-common pkg-config \
        zsh nano vim wget curl git rsync cmake unzip ssh \
        freeglut3 libxmu6 libglu1-mesa \
        python3-dev python3-pip python3-setuptools python3-numpy \
        python3-pillow python3-pil.imagetk libboost-python-dev \
        python3-pyqt5 python3-pyqt5.qtmultimedia python3-pyqt5.qtopengl \
        python3-pyqt5.qtpositioning python3-pyqt5.qtquick python3-pyqt5.qtx11extras

WORKDIR /usr/src/pyoptix

COPY . .

RUN python3 setup.py install

CMD /bin/bash
