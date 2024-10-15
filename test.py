import openshot

r = openshot.FFmpegReader("video.mp4")
r.Open()
c1 = openshot.Clip(r)
c1.Open()


w = openshot.FFmpegWriter("output.webm")

w.SetAudioOptions(True, "libvorbis", 44100, 2, openshot.LAYOUT_STEREO, 128000)
w.SetVideoOptions("libvpx", 1280, 720, openshot.Fraction(24, 1), 3000000)

w.Open()

w.WriteFrame(c1, 1, 5)

w.Close()
c1.Close()
r.Close()
