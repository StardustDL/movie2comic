from abc import abstractmethod
import sys
import time
from typing import List, Tuple
import ffmpeg
import os
import json
from ..model import StageResult
from .model import Frame, FrameStageResult
from ..worker import StageWorker


class FrameExtractor(StageWorker):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_frames(self, input_file_path, output_dir) -> FrameStageResult:
        raise NotImplementedError()

    def metafile_path(self) -> str:
        return self.session.frame_file

    def work(self) -> StageResult:
        return self.get_frames(self.session.video_file, self.session.frame_dir)


class DefaultFrameExtractor(FrameExtractor):
    def __init__(self):
        super().__init__()

    def get_frames(self, input_file_path, output_dir) -> FrameStageResult:
        frameType = "I"

        info = ffmpeg.probe(input_file_path, v="quiet", select_streams="v",
                            show_entries="frame=pkt_pts_time,pict_type")
        frames_info = info["frames"]
        times = [f["pkt_pts_time"]
                 for f in frames_info if f["pict_type"] == frameType]

        stream = ffmpeg.input(input_file_path)
        stream = stream.filter('select', f"eq(pict_type,{frameType})")
        stream = stream.output(os.path.join(
            output_dir, "%08d.jpg"), format="image2", vsync="vfr", **{"qscale:v": 2})

        success = True

        out, err = b"", b""
        try:
            out, err = stream.run(capture_stdout=True, capture_stderr=True)
        except:
            success = False

        frames = []
        for i, t in enumerate(times):
            frames.append(Frame("%08d.jpg" % (i+1), float(t)))

        res = FrameStageResult()
        res.success = success
        res.log = f"stdout: {out.decode('utf-8')}\nstderr: {err.decode('utf-8')}"
        res.frames = frames
        return res


if __name__ == "__main__":
    from ..settings import DATA_PATH

    outputPath = os.path.join(DATA_PATH, "test", "frames")
    os.makedirs(outputPath, exist_ok=True)

    source = sys.argv[1]

    worker = DefaultFrameExtractor()

    result = worker.get_frames(source, outputPath)

    print(json.dumps(result.as_dict(), indent=4))
