FROM buildpack-deps:bookworm AS build_stage

WORKDIR /build

RUN git clone --depth=1 https://github.com/OpenShot/libopenshot.git && \
    git clone --depth=1 https://github.com/OpenShot/libopenshot-audio.git

RUN sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        cmake \
        pkg-config dpkg \
        libfreetype-dev \
        libasound2-dev \
        libavcodec-dev \
        libavformat-dev \
        libavutil-dev \
        libswresample-dev \
        libswscale-dev \
        libpostproc-dev \
        libfdk-aac-dev \
        libjsoncpp-dev \
        cppzmq-dev libzmq3-dev \
        qtbase5-dev \
        libqt5svg5-dev \
        libbabl-dev \
        libopencv-dev \
        libprotobuf-dev \
        protobuf-compiler \
        python3-zmq python3-pyqt5.qtwebengine python3-dev \
        swig zlib1g \
        libgcc-s1 libstdc++6 \
        libmagick++-6.q16-dev libmagick++-dev \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN cd libopenshot-audio && \
    cmake -B build -S . && cmake --build build -j$(nproc) && cmake --install build && \
    cd ../libopenshot && \
    cmake -B build -S . && cmake --build build -j$(nproc)

FROM debian:bookworm-slim AS run_stage

RUN --mount=from=build_stage,source=/build,target=/build,rw \
    sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        cmake \
        libfreetype6 \
        libasound2 \
        libavcodec59 \
        libavformat59 \
        libavutil57 \
        libswresample4 \
        libswscale6 \
        libpostproc56 \
        libfdk-aac2 \
        libjsoncpp25 \
        libzmq5 \
        libqt5concurrent5 libqt5core5a \
        libqt5dbus5 libqt5svg5 \
        gir1.2-babl-0.1 libbabl-0.1-0 \
        libopencv-contrib406 libopencv-core406 \
        libopencv-dnn406 libopencv-features2d406 \
        libopencv-highgui406 libopencv-imgcodecs406 \
        libopencv-imgproc406 libopencv-videoio406 \
        libopencv-video406 \
        libprotobuf32 libprotobuf-lite32 \
        python3 python3-zmq python3-pyqt5.qtwebengine \
        swig zlib1g \
        libc6 libstdc++6 \
        imagemagick-6-common libmagick++-6.q16-8 \
        && \
    cd /build/libopenshot-audio && cmake --install build && \
    cd /build/libopenshot && cmake --install build && \
    ldconfig && \
    apt-get autoremove -y \
        cmake \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/*