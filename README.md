# Movie2Comic

![](https://shields.io/github/stars/StardustDL/movie2comic?style=social) ![](https://shields.io/github/forks/StardustDL/movie2comic?style=social) ![Deploy](https://github.com/StardustDL/movie2comic/workflows/Deploy/badge.svg) ![](https://shields.io/github/license/StardustDL/movie2comic) ![](https://shields.io/docker/pulls/stardustdl/movie2comic)

A tool to transfer movie into comics by keyframe extracting, voice recognition and style transfer techniques.

![](https://repository-images.githubusercontent.com/320451414/2ce27f80-3f10-11eb-892b-226f705d200c)

## Usage

1. Use Docker images [stardustdl/movie2comic](https://hub.docker.com/r/stardustdl/movie2comic).

> Docker image mirror: registry.cn-hangzhou.aliyuncs.com/stardustdl/movie2comic

```sh
docker-compose up
```

1. Visit `http://localhost:5000`.

## Dependencies

- [Vue 3](https://github.com/vuejs/vue-next)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [ffmpeg](http://ffmpeg.org/)
- [pocketsphinx](http://cmusphinx.sourceforge.net/)
- [Pillow](https://github.com/python-pillow/Pillow)
- [pydub](https://github.com/jiaaro/pydub)

### Deep Learning Engine

- [White-box-Cartoonization](./backend/m2c/styles/white_box_cartoonization/README.md) Official tensorflow implementation for CVPR2020 paper “Learning to Cartoonize Using White-box Cartoon Representations”. Licensed under the CC BY-NC-SA 4.0.
- [DeepSpeech](https://github.com/mozilla/DeepSpeech) DeepSpeech is an open source embedded (offline, on-device) speech-to-text engine which can run in real time on devices ranging from a Raspberry Pi 4 to high power GPU servers. Licensed under the MPL-2.0.

## Thanks

In 2019, Rivers-Shall, Forewing and I (StardustDL) came up with this idea after discussion, and we wrote a much simpler demo than this. Thesedays (2020), I re-implement this idea by myself and that is this project.

