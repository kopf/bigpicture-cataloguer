from BeautifulSoup import BeautifulSoup

import bpc.http as http


ALBUMS = 'http://www.boston.com/bigpicture/{year}/{{month:02d}}/'


def get_albums(year, month):
    html = http.get(ALBUMS.format(year=year, month=month))
    soup = BeautifulSoup(html)
    table = soup.findAll('table')[1]
    links = [a for a in soup.findAll('table')[1].findAll('a') if a.text and a.text != 'comments']
    retval = {}
    for link in links:
        retval[link.text] = link['href']
    return retval
