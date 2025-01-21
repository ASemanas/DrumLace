# Use the official Apache image from the Docker Hub
FROM php:7.2-apache

# Install prerequisites and add the deadsnakes PPA for newer Python versions
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        wget \
        libssl-dev \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \
        libnss3-dev \
        libsqlite3-dev \
        libreadline-dev \
        libbz2-dev \
        liblzma-dev \
        libffi-dev  \
        libsndfile1-dev \
        libasound2-dev \
        libjack-jackd2-dev \
        libglib2.0-dev \
        alsa-utils \
        alsa-oss && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Download Python 3.10 source code
RUN wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz && \
    tar xzf Python-3.10.0.tgz && \
    cd Python-3.10.0 && \
    ./configure --enable-optimizations && \
    make -j "$(nproc)" && \
    make altinstall && \
    rm -rf /Python-3.10.0 /Python-3.10.0.tgz

    RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 1
# Copy your local www directory to the Docker container's web root

RUN wget https://github.com/Kitware/CMake/releases/download/v3.25.3/cmake-3.25.3-linux-x86_64.tar.gz && \
    tar -zxvf cmake-3.25.3-linux-x86_64.tar.gz && \
    mv cmake-3.25.3-linux-x86_64 /usr/local/cmake && \
    ln -s /usr/local/cmake/bin/cmake /usr/local/bin/cmake && \
    rm -rf cmake-3.25.3-linux-x86_64.tar.gz

RUN wget https://github.com/FluidSynth/fluidsynth/archive/refs/tags/v2.3.5.tar.gz && \
    tar xzf v2.3.5.tar.gz && \
    cd fluidsynth-2.3.5 && \
    mkdir build && cd build && \
    cmake .. && \
    make && \
    make install && \
    ldconfig && \ 
    cd ../.. && rm -rf fluidsynth-2.3.5 v2.3.5.tar.gz

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.10 get-pip.py && \
    rm get-pip.py

COPY . /var/www

RUN pip3.10 install --no-cache-dir -r /var/www/dependencies.txt

# Expose port 80 comment change
EXPOSE 80

# Start the Apache server
CMD ["apache2ctl", "-D", "FOREGROUND"]