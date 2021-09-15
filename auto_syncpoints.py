# for getting YT videos automatically
from __future__ import unicode_literals, absolute_import, division, print_function

import json
import getopt, sys, argparse
from pathlib import Path

import youtube_dl

# Adapted from script at
# https://github.com/CPJKU/madmom/blob/master/bin/DBNDownBeatTracker
from madmom.audio.signal import SignalProcessor
from madmom.features import (ActivationsProcessor,
                             DBNDownBeatTrackingProcessor,
                             RNNDownBeatProcessor)
from madmom.io import write_beats, write_downbeats
from madmom.processors import IOProcessor, io_arguments

class YtLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_notify_hook(d):
    if d['status'] == 'finished':
        print(d)
        print('Done downloading, now converting ...')

def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--input', nargs=1, help='input file path or yt url')
    args = parser.parse_args()
    input_path = args.input[0]

    # credit: https://stackoverflow.com/a/54047181/2618015
    # if you get 403 errors run `youtube-dl --rm-cache-dir`
    if(input_path[0:4] == 'http'):
        # we have a URL instead of a file
        ydl_opts = { 'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}],
                'keepvideo': False,
                'logger': YtLogger(),
                'progress_hooks': [my_notify_hook],
                }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(input_path, download=False)
            video_title = info_dict.get('title', None)

        tmpfile = f'/tmp/{video_title}.mp3'
        ydl_opts.update({'outtmpl': tmpfile})

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([input_path])
        
        input_path = tmpfile

    ActivationsProcessor('out', fps=100, sep=None)
    SignalProcessor(norm=False, gain=0)
    proc = DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)

    in_processor = RNNDownBeatProcessor()(input_path)
    beats = proc(in_processor)

    downbeats = [t for t, b in beats if b == 1.]
    syncpoints_object = str([[i,d] for i, d in enumerate(downbeats)])
    output_json_path = Path(input_path).with_suffix('.json').name

    with open(f'./downbeats-{output_json_path}', 'w') as text_file:
      text_file.write(syncpoints_object)

if __name__ == "__main__":
    main()

