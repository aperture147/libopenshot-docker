[libopenshot](https://github.com/OpenShot/libopenshot) Docker:
=====

Introduction
-----

Containerized [libopenshot](https://github.com/OpenShot/libopenshot), with Python/C++ support

How to use
-----

1. Pull the image

```bash
docker pull aperture147/libopenshot:latest
```

2. Download your test video (skip if you've already had one):

```bash
curl -L https://videos.pexels.com/video-files/28830734/12488932_1920_1080_30fps.mp4 -o video.mp4
```

2. Run the test container

```bash
docker run --cap-add SYS_NICE --shm-size 4G -v $(pwd):/work --rm -it aperture147/libopenshot:latest python3 /work/test.py
```

How to build:
-----

Run:

```bash
docker build . -t openshot
```