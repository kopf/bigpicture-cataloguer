import sys

import requests
import logbook

from bpc import __version__ as VERSION


log = logbook.Logger('bpc.http')

MAX_RETRIES = 5

HEADERS = {
    'User-Agent': ('Big Picture Cataloguer {0} - '
                   'http://github.com/kopf/bigpicture-cataloguer'.format(VERSION)),
    'From': 'ventolin+bpc@gmail.com'
}


class DownloadError(Exception):
    pass


def retry_or_fail(url, retries_left, stream):
    if retries_left > 0:
        log.info('Retrying...')
        return get(url, retries_left=retries_left-1, stream=stream)
    else:
        log.critical('Max retries exceeded trying to download {0}'.format(url))
        raise DownloadError()


def get(url, retries_left=MAX_RETRIES, stream=False):
    try:
        resp = requests.get(url, stream=stream)
    except Exception, e:
        log.error('{0} error encountered when trying to download {1}'.format(e, url))
        return retry_or_fail(url, retries_left, stream)
    if not 200 <= resp.status_code < 300:
        log.error('Received status code {0} trying to download {1}'.format(
            resp.status_code, url))
        return retry_or_fail(url, retries_left, stream)
    return resp
