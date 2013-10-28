import re

from BeautifulSoup import BeautifulSoup

import bpc.http as http


ALBUMS = 'http://www.boston.com/bigpicture/{year}/{{month:02d}}/'


def list_albums(year, month):
    """Returns a dictionary of the form {title: url} for
    photo albums for a given month
    """
    html = http.get(ALBUMS.format(year=year, month=month))
    soup = BeautifulSoup(html)
    divs = soup.findAll('div', {'class': 'headDiv2'})
    retval = {}
    if not divs:
        # old version of the site
        table = soup.findAll('table')[1]
        links = [a for a in soup.findAll('table')[1].findAll('a') if a.text and a.text != 'comments']
        for link in links:
            retval[link.text] = link['href']
    else:
        for div in divs:
            retval[div.a.text] = div.a['href']
    return retval


def get_album_intro_text(soup):
    """Returns an album's intro text
    """
    return clean_caption_text(soup.find('div', {'class': 'bpBody'}))


def make_image_dict(div):
    """Returns a dict in the form {'url': url, 'caption': '...'} for an
    image div
    """
    return {
        'url': div.find('img')['src'],
        'caption': clean_caption_text(div.find('div', {'class': 'bpCaption'}))
    }


def clean_caption_text(div):
    """Removes links from captions, "(x photos total)" messages, etc
    """
    segments = []
    regex = re.compile(r"#photo(\d*)")
    for link in div.findAll('a'):
        # first, remove all meaningless links
        if regex.match(link['href']):
            link.extract()
    for content in div.contents:
        if isinstance(content, basestring):
            segments.append(content)
        else:
            segments.append(content.text)
    retval = u''.join(segments)
    retval = re.sub(r'\(\d\d photos total\)', '', retval)
    return retval.strip()


def list_album_photos(url):
    """Returns a list of dictionaries representing images in
    the form [{'url': url, 'caption': caption}, ...]
    """
    html = http.get(url)
    soup = BeautifulSoup(html)

    # Process top image, prepending album intro text to caption
    top_image_div = soup.find('div', {'class': 'bpImageTop'})
    entry = make_image_dict(top_image_div)
    intro_text = get_album_intro_text(soup)
    entry['caption'] = u'{0} || {1}'.format(
        intro_text, entry['caption'])
    retval = [entry]

    # Process rest of images
    divs = soup.findAll('div', {'class': 'bpBoth'})
    for div in divs:
        retval.append(make_image_dict(div))
    return retval
