# -*- coding: utf-8 -*-
import re

from BeautifulSoup import BeautifulSoup

import bpc.http as http


ALBUMS = 'http://www.boston.com/bigpicture/{year}/{month:02d}/'


def list_albums(year, month):
    """Returns list of dictionaries representing all
    photo albums for a given month
    """
    html = http.get(ALBUMS.format(year=year, month=month)).text
    soup = BeautifulSoup(html)
    divs = soup.findAll('div', {'class': 'headDiv2'})
    retval = []
    if not divs:
        # old version of the site
        table = soup.findAll('table')[1]
        links = [a for a in soup.findAll('table')[1].findAll('a') \
                 if a.text and a.text != 'comments']
        for link in links:
            retval.append({'name': link.text, 'url': link['href']})
    else:
        for div in divs:
            retval.append({'name': div.a.text, 'url': div.a['href']})
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for album in retval:
        for char in invalid_chars:
            album['name'] = album['name'].replace(char, '_')
        album['name'] = album['name'].replace(u"\x92", "'")\
                                     .replace(u'\u201d', '"')\
                                     .strip('.')
    return retval[::-1]


def list_album_photos(url):
    """Returns a list of dictionaries representing images in
    the form [{'url': url, 'caption': caption}, ...]
    """
    html = http.get(url).text
    soup = BeautifulSoup(html)

    # Process top image, prepending album intro text to caption
    top_image_div = soup.find('div', {'class': 'bpImageTop'})
    if not top_image_div:
        # Not a gallery - probably a blog post.
        return []
    entry = make_image_dict(top_image_div)
    intro_text = get_album_intro_text(soup)
    entry['caption'] = u'{0} || {1}'.format(
        intro_text, entry['caption'])
    retval = [entry]

    # Process rest of images
    divs = soup.findAll('div', {'class': 'bpBoth'})
    for div in divs:
        image = make_image_dict(div)
        if image:
            retval.append(image)
    return retval


def get_album_intro_text(soup):
    """Returns an album's intro text"""
    return clean_caption_text(soup.find('div', {'class': 'bpBody'}))


def make_image_dict(div):
    """Returns a dict in the form {'url': url, 'caption': '...'} for an
    image div
    """
    image = div.find('img')
    if not image or not image['src']:
        return {}
    caption = div.find('div', {'class': 'bpCaption'}) or ''
    return {
        'url': image['src'],
        'caption': clean_caption_text(caption)
    }


def clean_caption_text(div):
    """Removes links from captions, "(x photos total)" messages, etc"""
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
    replacements = {u'\xb4': u"'", u'\xd7': u'x',
                    u'\xa0': u' ', u'&rsquo;': u"'",
                    u'\xf2': u'o', u'\xe1': u'a',
                    u'&copy;': u'Copyright'}
    for orig, replacement in replacements.iteritems():
        retval = retval.replace(orig, replacement)
    return retval.strip()
