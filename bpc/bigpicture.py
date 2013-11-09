#!/usr/bin/env python

import argparse
import os
import shutil
import sys

import logbook
import pyexiv2

from bpc import __version__ as VERSION
import bpc.http as http
from bpc.scraper import list_albums, list_album_photos
from bpc.sync import get_months


log = logbook.Logger('bpc.run')


def write_caption(path, caption):
    metadata = pyexiv2.ImageMetadata(path)
    metadata.read()
    metadata['Iptc.Application2.Caption'] = [caption]
    metadata.write()


def download_album(name, path, url):
    """Downloads a photo album if necessary"""
    if not os.path.exists(path):
        photos = list_album_photos(url)
        if not photos:
            return
        log.info(u'Downloading: "{0}"'.format(name))
        os.makedirs(path)
        i = 0
        for photo in photos:
            i += 1
            orig_filename = photo['url'].split('/')[-1]
            file_path = os.path.join(path, '{0} - {1}'.format(i, orig_filename))
            try:
                response = http.get(photo['url'], stream=True)
            except http.DownloadError:
                continue
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            if not file_path.endswith('.gif'):
                write_caption(file_path, photo['caption'])
    else:
        log.info(u'Photo album "{0}" already downloaded, skipping...'.format(name))


if __name__ == '__main__':
    print 'Big Picture Cataloguer v{0}'.format(VERSION)
    print 'Aengus Walton - http://ventolin.org'
    print '==========================='
    print ''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", help="The directory in which photos are to be stored")
    args = parser.parse_args()
    if not os.path.exists(args.directory):
        log.info('{0} does not exist, creating...'.format(args.directory))
        os.makedirs(args.directory)
    months = get_months(args.directory)
    for dt in months:
        albums = list_albums(dt.year, dt.month)
        for album in albums:
            album_path = os.path.join(sys.argv[-1], str(dt.year),
                                      '{0:02d}'.format(dt.month), album['name'])
            download_album(album['name'], album_path, album['url'])
