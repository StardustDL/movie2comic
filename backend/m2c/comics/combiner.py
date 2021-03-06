from abc import abstractmethod
import math
from ..inputs.model import VideoInfo
from ..subtitles.model import Subtitle
from ..styles.model import StyledFrame
from ..frames.model import Frame
import shutil
import sys
import time
from typing import List, Tuple
import ffmpeg
import os
import json
from ..model import StageResult
from .model import ComicStageResult
from ..worker import StageWorker
from PIL import Image, ImageDraw, ImageFont


class ComicCombiner(StageWorker):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def combine(self, info, frames, subtitles, styledFrames, output_dir) -> ComicStageResult:
        raise NotImplementedError()

    def metafile_path(self) -> str:
        return self.session.output_file

    def work(self) -> StageResult:
        try:
            result = self.combine(self.session.result_input().info, self.session.result_frames().frames, self.session.result_subtitles(
            ).subtitles, self.session.result_styles().frames, self.session.output_dir)
            return result
        except Exception as ex:
            result = ComicStageResult()
            result.log = str(ex)
            return result


def add_text_to_image(image, text, font=None):
    if font is None:
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 32)

    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    font_size = 32
    while text_size_x > rgba_image.size[0] - 20 or text_size_y > rgba_image.size[1] - 20:
        if font_size <= 2:
            break
        font_size -= 2
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', font_size)
        text_size_x, text_size_y = image_draw.textsize(text, font=font)

    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', font_size)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    text_xy = (rgba_image.size[0] - text_size_x - 20,
               rgba_image.size[1] - text_size_y - 20)

    image_draw.text((text_xy[0] - 1, text_xy[1] - 1), text, font=font, fill=(0, 0, 0, 255))
    image_draw.text((text_xy[0] - 1, text_xy[1] + 1), text, font=font, fill=(0, 0, 0, 255))
    image_draw.text((text_xy[0] + 1, text_xy[1] - 1), text, font=font, fill=(0, 0, 0, 255))
    image_draw.text((text_xy[0] + 1, text_xy[1] + 1), text, font=font, fill=(0, 0, 0, 255))

    image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 255))

    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    return image_with_text.convert("RGB")


class DefaultComicCombiner(ComicCombiner):
    def __init__(self):
        super().__init__()

    def combine(self, info: VideoInfo, frames: List[Frame], subtitles: List[Subtitle], styledFrames: List[StyledFrame], output_dir) -> ComicStageResult:
        OUTPUT_NAME = "output.jpg"
        FRAME_COUNT = 20
        WORD_IN_ONE_LINE = 10
        MIN_SEGMENT_DURATION = 5

        # TODO: duration minimum, multi page, frame count one page

        duration = info.duration
        
        frame_count = min(FRAME_COUNT, len(frames))
        segment_duration = max(MIN_SEGMENT_DURATION, duration / frame_count)

        frame_ind = 0
        subtitle_ind = 0
        position = 0

        pieces = []

        while position < duration:
            np = min(duration, position + segment_duration)

            select_frame = -1

            while frame_ind < len(frames):
                if frames[frame_ind].time < position:
                    frame_ind += 1
                else:
                    break

            frame_left = frame_ind

            while frame_ind < len(frames):
                if frames[frame_ind].time < np:
                    frame_ind += 1
                else:
                    break

            frame_right = frame_ind

            select_frame = (frame_left + frame_right) // 2
            if select_frame >= len(frames):
                select_frame = -1

            select_subtitle = ""

            while subtitle_ind < len(subtitles):
                if subtitles[subtitle_ind].end < position:
                    subtitle_ind += 1
                else:
                    break

            subtitle_left = subtitle_ind

            while subtitle_ind < len(subtitles):
                if subtitles[subtitle_ind].start < np:
                    subtitle_ind += 1
                else:
                    break

            subtitle_right = subtitle_ind

            for i in range(subtitle_left, subtitle_right):
                words = subtitles[i].text.split()
                for i in range(0, len(words), WORD_IN_ONE_LINE):
                    select_subtitle += " ".join(words[i: i + WORD_IN_ONE_LINE])
                    if i+WORD_IN_ONE_LINE < len(words):
                        select_subtitle += "\n"
                select_subtitle += ".\n"

            if select_frame != -1:
                pieces.append((select_frame, select_subtitle))

            position += segment_duration

        frame_cnt = len(pieces)

        # Styled frame max size 1280*720
        width, height = min(1280,int(info.width)), min(720,int(info.height)) * int(math.ceil(frame_cnt / 2))

        result_img = Image.new('RGB', (2*width, height))
        current_width, current_height = 0, 0
        for i, (f_ind, subtitle) in enumerate(pieces):
            im = Image.open(self.session.styled_image_path(
                styledFrames[f_ind].name))
            img = add_text_to_image(im, subtitle)
            if i % 2 == 0:
                result_img.paste(
                    img, (0, current_height, img.width, current_height + img.height))
            else:
                result_img.paste(
                    img, (width, current_height, width + img.width, current_height + img.height))
                current_height += img.height

        result_img.save(os.path.join(output_dir, OUTPUT_NAME))

        res = ComicStageResult()
        res.success = True
        res.file = OUTPUT_NAME
        return res
