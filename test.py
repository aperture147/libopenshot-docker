import openshot
import os

setting = openshot.Settings.Instance()
setting.OMP_THREADS = 24
setting.FF_THREADS = 16
setting.VIDEO_CACHE_PERCENT_AHEAD = 0
setting.VIDEO_CACHE_MIN_PREROLL_FRAMES = 0
setting.VIDEO_CACHE_MAX_PREROLL_FRAMES = 0
setting.VIDEO_CACHE_MAX_FRAMES = 0
setting.ENABLE_PLAYBACK_CACHING = False
setting.HIGH_QUALITY_SCALING = True
# setting.DEBUG_TO_STDERR = False

width = 1920
height = 1080
fps = openshot.Fraction(30, 1)
audio_bitrate = 44100
audio_channels = 2
audio_channel_layout = openshot.LAYOUT_STEREO
pixel_ratio = openshot.Fraction(1, 1)

location = os.path.dirname(__file__)


timeline = openshot.Timeline(width, height, fps, audio_bitrate, audio_channels, audio_channel_layout)


r = openshot.FFmpegReader(os.path.join(location, "video.mp4"))
r.Open()


blur_effect = openshot.Blur()
blur_effect.iterations.AddPoint(1, 5)
# blur_effect.iterations.AddPoint(30, 0)
blur_effect.horizontal_radius.AddPoint(1, 5)
blur_effect.horizontal_radius.AddPoint(1, 5)
blur_effect.horizontal_radius.AddPoint(60, 0)
blur_effect.horizontal_radius.AddPoint(60, 0)
blur_effect.sigma.AddPoint(1, 10)
blur_effect.Position(0)
blur_effect.Layer(2)



c = openshot.Clip(r)
c.AddEffect(blur_effect)
c.Position(0)
c.gravity = openshot.GRAVITY_CENTER
c.Layer(1)
c.Open()

timeline.AddClip(c)
timeline.Open()

w = openshot.FFmpegWriter(os.path.join(location, "output.mp4"))

# w.info.pixel_format = 0

w.SetAudioOptions(False, "libvorbis", 44100, 2, openshot.LAYOUT_STEREO, 128000)
w.SetVideoOptions(True, "libx265", fps, width, height, pixel_ratio, False, False, 3000000)

w.PrepareStreams()

w.SetOption(openshot.VIDEO_STREAM, "crf", "28")
w.SetOption(openshot.VIDEO_STREAM, "preset", "veryslow")
# w.SetOption(openshot.VIDEO_STREAM, "args", "-pix_fmt yuv420p")

w.WriteHeader()
w.Open()
w.WriteFrame(c, 1, r.info.video_length)
w.WriteTrailer()

w.Close()
timeline.Close()
c.Close()
r.Close()
