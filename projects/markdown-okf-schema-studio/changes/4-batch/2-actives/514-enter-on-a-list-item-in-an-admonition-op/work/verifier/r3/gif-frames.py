# Frames of the branch's clip GIF: all frames are composed; montages of the frames at the times
# listed (just after each key press, the zooms, the typed word, the end).
import sys
from PIL import Image, ImageSequence, ImageDraw
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src)
frames, times, t = [], [], 0.0
for f in ImageSequence.Iterator(im):
    frames.append(f.convert("RGB")); times.append(t); t += f.info.get("duration", 0) / 1000
print("frames", len(frames), "seconds", round(t, 2), "size", im.size)
want = [0.0,1.2,2.8,4.2,6.0,7.5,8.2,9.2,10.8,12.4,14.0,15.6,17.2,18.8,19.5,20.5,21.7,22.2,22.9,23.8,24.6,25.4,25.8,t-0.05]
def at(s):
    return max(i for i, x in enumerate(times) if x <= s + 1e-6)
w, h = frames[0].size
for n in range(0, len(want), 6):
    sheet = Image.new("RGB", (w * 2, h * 3), "black")
    for k, s in enumerate(want[n:n + 6]):
        i = at(s); tile = frames[i].copy(); d = ImageDraw.Draw(tile)
        d.rectangle([0, h - 18, 110, h], fill="black"); d.text((4, h - 15), f"t={times[i]:.2f}s f{i}", fill="yellow")
        sheet.paste(tile, ((k % 2) * w, (k // 2) * h))
    name = f"{out}/montage-{n // 6 + 1}.png"; sheet.save(name); print(name, sheet.size)
