#!/usr/bin/env python

import os
import shutil
import sys

import logbook

import bpc.http as http
from bpc.scraper import list_albums, list_album_photos
from bpc.sync import get_months


log = logbook.Logger('bpc.run')

#def write_caption(path, caption):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(path)
#    metadata.read()
#    metadata['Iptc.Application2.Caption'] = [caption]
#    metadata.write()


def download_album(name, path, url):
    """Downloads a photo album if necessary"""
    if not os.path.exists(path):
        log.info('Downloading: "{0}"'.format(name))
        os.makedirs(path)
        photos = list_album_photos(url)
        i = 0
        for photo in photos:
            i += 1
            orig_filename = photo['url'].split('/')[-1]
            file_path = os.path.join(path, '{0} - {1}'.format(i, orig_filename))
            response = http.get(photo['url'], stream=True)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
    else:
        log.info('Photo album "{0}" already downloaded, skipping...'.format(name))


if __name__ == '__main__':
    months = get_months(sys.argv[-1])
    for dt in months:
        albums = list_albums(dt.year, dt.month)
        for album_name, url in albums.iteritems():
            album_path = os.path.join(sys.argv[-1], str(dt.year),
                                      '{0:02d}'.format(dt.month), album_name)
            download_album(album_name, album_path, url)