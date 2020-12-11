import sys
from typing import List, Tuple
import ffmpeg
import os
import json
from multiprocessing import Process
from . import Frame, FrameExtractorResult
from ..session import Session, SessionStage
from ..serialization import PropertySerializable
from ..serialization.json import Encoder


def _getFrames(source, outputDir, frameType) -> FrameExtractorResult:
    info = ffmpeg.probe(source, v="quiet", select_streams="v",
                        show_entries="frame=pkt_pts_time,pict_type")
    frames_info = info["frames"]
    times = [f["pkt_pts_time"]
             for f in frames_info if f["pict_type"] == frameType]

    stream = ffmpeg.input(source)
    stream = stream.filter('select', f"eq(pict_type,{frameType})")
    stream = stream.output(os.path.join(
        outputDir, "%08d.jpg"), format="image2", vsync="vfr", **{"qscale:v": 2})

    success = True

    out, err = b"", b""
    try:
        out, err = stream.run(capture_stdout=True, capture_stderr=True)
    except:
        success = False

    results = []
    for i, t in enumerate(times):
        results.append(Frame("%08d.jpg" % (i+1), float(t)))

    return FrameExtractorResult(success, results, out.decode("utf-8"), err.decode("utf-8"))


class KeyframeExtractor(Process):
    def __init__(self, sid):
        super().__init__(daemon=True)
        self.sid = sid

    def run(self):
        session = Session(self.sid)

        result = _getFrames(session.input_file, session.keyframe_dir, "I")

        with open(session.keyframe_file, "w") as file:
            json.dump(result, file, ensure_ascii=False, cls=Encoder)


if __name__ == "__main__":
    from ..settings import DATA_PATH

    outputPath = os.path.join(DATA_PATH, "test", "keyframes")
    os.makedirs(outputPath, exist_ok=True)

    source = sys.argv[1]

    frames = _getFrames(source, outputPath, "I").frames

    print(json.dumps([f.__dict__ for f in frames], indent=4))
