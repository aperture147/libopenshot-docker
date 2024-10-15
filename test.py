import openshot
import math
import os

r = openshot.FFmpegReader(os.path.join(os.path.dirname(__file__), "video.mp4"))
r.Open()

c1 = openshot.Clip(r)
c1.Open()

w = openshot.FFmpegWriter("output1.mp4")

# w.info.pixel_format = 0

w.SetAudioOptions(False, "libvorbis", 44100, 2, openshot.LAYOUT_STEREO, 128000)
w.SetVideoOptions(True, "libx265", r.info.fps, r.info.width, r.info.height, r.info.pixel_ratio, r.info.interlaced_frame, r.info.top_field_first, math.ceil(r.info.video_bit_rate * 0.5))

w.PrepareStreams()

w.SetOption(openshot.VIDEO_STREAM, "crf", "28")
# w.SetOption(openshot.VIDEO_STREAM, 'colorspace', 'yuv420p')
# w.SetOption(openshot.VIDEO_STREAM, "pix_fmt", 'yuv420p')

w.WriteHeader()
w.Open()
w.WriteFrame(c1, 1, r.info.video_length)
w.WriteTrailer()

w.Close()
c1.Close()
r.Close()
