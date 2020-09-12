"""Song Downloader"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import csv
from youtube_dl import YoutubeDL
from youtube_dl.postprocessor.ffmpeg import FFmpegMetadataPP


class FFmpegMP3MetadataPP(FFmpegMetadataPP):
    def __init__(self, downloader=None, metadata=None):
        self.metadata = metadata or {}
        super(FFmpegMP3MetadataPP, self).__init__(downloader)

    def run(self, information):
        information = self.purge_metadata(information)
        information.update(self.metadata)
        return super(FFmpegMP3MetadataPP, self).run(information)

    def purge_metadata(self, info):
        info.pop('title', None)
        info.pop('track', None)
        info.pop('upload_date', None)
        info.pop('description', None)
        info.pop('webpage_url', None)
        info.pop('track_number', None)
        info.pop('artist', None)
        info.pop('creator', None)
        info.pop('uploader', None)
        info.pop('uploader_id', None)
        info.pop('genre', None)
        info.pop('album', None)
        info.pop('album_artist', None)
        info.pop('disc_number', None)
        return info


class MyLogger(object):
    def debug(self, msg):
        print("DEBUG: ", msg)
        # pass

    def warning(self, msg):
        print("WARN: ", msg)
        # pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

    if d['status'] == 'downloading':
        if d.get('eta') is not None:
            print(d['_percent_str'])
        else:
            print('Unknown ETA')


def download(ydl, links):
    ydl.download(links)


def read_csv(infile):
    names = []
    artists = []
    links = []
    with open(infile, 'r') as csvfile:
        csvobj = csv.reader(csvfile, delimiter=',')
        for row in csvobj:
            names.append(row[0])
            artists.append(row[1])
            links.append(row[2])
    return names, artists, links


def main(csvfile, filepath):
    # input path
    names, artists, links = read_csv(csvfile)

    ydl_opts = {
            'verbose': True,
            'geo_verification_proxy': '',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': filepath+'/'
            }

    for i in range (0, len(links)):
        path = os.path.join(filepath, '{} - {}.%(ext)s'.format(names[i], artists[i]))

        metadata = {
            "title": names[i],
            "artist": artists[i],
        }

        url = [links[i]]
        ydl_opts['outtmpl'] = path
        ydl = YoutubeDL(ydl_opts)
        MyLogger().debug("DOWNLOADING {} : {} ".format(path, url))

        ffmpeg_mp3_metadata_pp = FFmpegMP3MetadataPP(ydl, metadata)
        ydl.add_post_processor(ffmpeg_mp3_metadata_pp)
        download(ydl, url)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        inputs = sys.argv[1:]
        csvfile = inputs[0]
        filepath = inputs[1]
        main(csvfile, filepath)

    else:
        print("Enter excel file and folder name => downloader.py feb_songs.csv song_drop")
        exit(0)