# Movie2Comic

A tool to transfer movie into comics by keyframe extracting, voice recognition and style transfer techniques.

## Dependencies

- [Vue 3](https://github.com/vuejs/vue-next)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [ffmpeg](http://ffmpeg.org/)
- [pocketsphinx](http://cmusphinx.sourceforge.net/)
- [Pillow](https://github.com/python-pillow/Pillow)
- [pydub](https://github.com/jiaaro/pydub)

### Deep Learning Engine

- [White-box-Cartoonization](./backend/styles/white_box_cartoonization/README.md) Official tensorflow implementation for CVPR2020 paper “Learning to Cartoonize Using White-box Cartoon Representations”. Licensed under the CC BY-NC-SA 4.0.
- [DeepSpeech](https://github.com/mozilla/DeepSpeech) DeepSpeech is an open source embedded (offline, on-device) speech-to-text engine which can run in real time on devices ranging from a Raspberry Pi 4 to high power GPU servers. Licensed under the MPL-2.0.

## Thanks

In 2019, Rivers-Shall, Forewing and I came up with this idea after discussion, and we wrote a much simpler demo than this. Thesedays, I re-implement this idea by myself and that is this project.

