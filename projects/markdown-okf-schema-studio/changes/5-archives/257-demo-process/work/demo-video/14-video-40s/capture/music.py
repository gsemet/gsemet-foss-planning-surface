"""Writes a soft original backing track: a warm pad and a quiet arpeggio, with no sampled audio."""
import math, struct, sys, wave
out, seconds, rate = sys.argv[1], 40.0, 44100
count = int(seconds * rate)
left, right = [0.0] * count, [0.0] * count
bar = 60 / 76 * 4
chords = [[48, 55, 64, 67], [45, 52, 60, 67], [41, 53, 60, 65], [43, 50, 59, 67]]
hz = lambda n: 440 * 2 ** ((n - 69) / 12)
tau = 2 * math.pi

def add(start, length, gain, pan, sample):
    first = int(start * rate)
    for i in range(first, min(count, first + int(length * rate))):
        v = gain * sample(i / rate - start)
        left[i] += v * (1 - pan)
        right[i] += v * pan

for b in range(int(seconds / bar) + 1):
    notes, start = chords[b % 4], b * bar
    span = bar + 1.5
    for k, n in enumerate(notes):
        f = hz(n)
        add(start, span, 0.05, 0.35 + 0.1 * k, lambda u, f=f: min(u / 0.9, 1) * min((span - u) / 1.5, 1) * (
            math.sin(tau * f * u) + 0.3 * math.sin(tau * 2 * f * u + 0.4) + 0.5 * math.sin(tau * f * 1.003 * u)))
    for j, pick in enumerate([1, 2, 3, 2, 1, 3, 2, 3]):
        f = hz(notes[pick] + 12)
        add(start + j * bar / 8, 1.2, 0.07, 0.3 + 0.4 * (j % 2), lambda u, f=f: math.exp(-u * 3.2) * min(u / 0.006, 1) * (
            math.sin(tau * f * u) + 0.25 * math.sin(2 * tau * f * u)))

delay = int(0.33 * rate)
wet_l, wet_r = left[:], right[:]
for i in range(delay, count):
    left[i] += 0.28 * wet_r[i - delay]
    right[i] += 0.28 * wet_l[i - delay]
peak = max(max(map(abs, left)), max(map(abs, right)))
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(rate)
    data = bytearray()
    for i in range(count):
        t = i / rate
        g = 0.5 / peak * min(t / 1.5, 1) * max(0.0, min((seconds - t) / 2.5, 1)) * 32767
        data += struct.pack("<hh", int(left[i] * g), int(right[i] * g))
    w.writeframes(bytes(data))
