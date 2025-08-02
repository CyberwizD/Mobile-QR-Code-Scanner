FROM python:3.10-slim

# Avoid prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Android build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    git zip unzip curl wget \
    build-essential \
    python3-dev python3-pip python3-setuptools python3-wheel \
    libffi-dev libssl-dev libjpeg-dev zlib1g-dev \
    libncurses5 libncurses5-dev libreadline-dev libgdbm-dev \
    libbz2-dev liblzma-dev libsqlite3-dev \
    libxml2-dev libxslt1-dev \
    libegl1-mesa libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set locale
ENV LANG=C.UTF-8

# Install Cython and Buildozer
RUN pip install --upgrade pip cython buildozer

# Install Android SDK & NDK (automatically downloaded by buildozer)
ENV ANDROID_HOME="/root/.buildozer/android/platform/android-sdk"
ENV PATH="${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${PATH}"

# Set working directory
WORKDIR /app

# Copy your buildozer.spec and app source (optional if you want prebuild)
COPY . .

# Default command (override in `docker run` if needed)
CMD ["buildozer", "android", "debug"]
