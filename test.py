import openshot
import math
import os

setting = openshot.Settings.Instance()
setting.VIDEO_CACHE_PERCENT_AHEAD = 24
setting.FF_THREADS = 16
setting.VIDEO_CACHE_PERCENT_AHEAD = 0
setting.VIDEO_CACHE_MIN_PREROLL_FRAMES = 0
setting.VIDEO_CACHE_MAX_PREROLL_FRAMES = 0
setting.VIDEO_CACHE_MAX_FRAMES = 0
setting.ENABLE_PLAYBACK_CACHING = False
setting.HIGH_QUALITY_SCALING = True
# setting.DEBUG_TO_STDERR = False

location = os.path.dirname(__file__)
r = openshot.FFmpegReader(os.path.join(location, "video.mp4"))
r.Open()

c = openshot.Clip(r)
c.Open()

w = openshot.FFmpegWriter(os.path.join(location, "output.mp4"))

# w.info.pixel_format = 0

w.SetAudioOptions(False, "libvorbis", 44100, 2, openshot.LAYOUT_STEREO, 128000)
w.SetVideoOptions(True, "libx265", r.info.fps, r.info.width, r.info.height, r.info.pixel_ratio, r.info.interlaced_frame, r.info.top_field_first, math.ceil(r.info.video_bit_rate * 0.5))

w.PrepareStreams()

w.SetOption(openshot.VIDEO_STREAM, "crf", "28")
# w.SetOption(openshot.VIDEO_STREAM, 'colorspace', 'yuv420p')
# w.SetOption(openshot.VIDEO_STREAM, "pix_fmt", 'yuv420p')

w.WriteHeader()
w.Open()
w.WriteFrame(c, 1, r.info.video_length)
w.WriteTrailer()

w.Close()
c.Close()
r.Close()
