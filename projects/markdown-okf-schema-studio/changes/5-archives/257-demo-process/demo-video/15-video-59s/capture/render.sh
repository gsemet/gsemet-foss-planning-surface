#!/bin/sh
# Rebuilds the video from the storyboard and the last take. TRIAL_SCRATCH holds the take.
set -e
here=$(cd "$(dirname "$0")/.." && pwd)
python3 "$here/capture/story.py" "$here/01-storyboard.md" "$here/remotion/src/story.json"
cd "$here/remotion"
node node_modules/@remotion/cli/remotion-cli.js render src/index.ts Video out/video-59s.mp4 --codec=h264 --pixel-format=yuv420p --crf=18 --log=error
