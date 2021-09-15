# Syncpoint generator

#### Not official in any way - just a proof of concept at this point

## Instructions

* Clone this repo

* `pip install -r requirements.txt`

For an audio file on your computer

```
$ python auto_syncpoints.py --input ./path_to_my_audio.m4a
```

For a video directly from YouTube (audio will be saved under `/tmp`)

```
$ python auto_syncpoints.py --input https://www.youtube.com/watch?v=nSxKi5AXqEw
```

These will output a `.json` file in this folder which contains the syncpoints ready for importing.
