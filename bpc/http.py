import sys

import requests
import logbook


log = logbook.Logger('bpc.http')
MAX_RETRIES = 5


def retry_or_fail(url, retries_left, stream):
    if retries_left > 0:
        log.info('Retrying...')
        return get(url, retries_left=retries_left-1, stream=stream)
    else:
        log.critical('Max retries exceeded trying to download {0}'.format(url))
        log.critical('Aborting...')
        sys.exit(-1)


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
