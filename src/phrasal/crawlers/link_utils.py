"""
A simple utility module module to deal with links. Given a list of links and a base url, it will:

* resolve relative links,
* exclude duplicates,
* strip anchors,
* exclude non HTTP/HTTPs links.

To further filter links pointing to images, PDFs or
other non-text resources, look at the `is_media_link` method (also provided).
"""

from typing import Iterable, Generator, Optional, Union
import urllib.parse as up


MEDIA_EXTENSIONS = dict((s, True) for s in [
    "3dv", "3g2", "3gp", "pi1", "pi2", "pi3", "ai", "amf", "amv", "art", "art", "ase", "asf", "avi", "awg", "blp",
    "bmp", "bw", "bw", "cd5", "cdr", "cgm", "cit", "cmx", "cpt", "cr2", "cur", "cut", "dds", "dib", "djvu", "doc",
    "docx", "drc", "dxf", "e2d", "ecw", "egt", "egt", "emf", "eps", "exif", "f4a", "f4b", "f4p", "f4v", "flv", "flv",
    "flv", "fs", "gbr", "gif", "gif", "gifv", "gpl", "grf", "hdp", "icns", "ico", "iff", "iff", "int", "int", "inta",
    "jfif", "jng", "jp2", "jpeg", "jpg", "jps", "jxr", "lbm", "lbm", "liff", "m2v", "m4p", "m4v", "m4v", "max", "miff",
    "mkv", "mng", "mng", "mov", "mp2", "mp4", "mpe", "mpeg", "mpeg", "mpg", "mpg", "mpv", "msp", "mxf", "nitf", "nrrd",
    "nsv", "odg", "ogg", "ogv", "ota", "pam", "pbm", "pc1", "pc2", "pc3", "pcf", "pct", "pcx", "pcx", "pdd", "pdf",
    "pdn", "pgf", "pgm", "pict", "png", "pnm", "pns", "ppm", "ppt", "pptx", "psb", "psd", "psp", "px", "pxm", "pxr",
    "qfx", "qt", "ras", "raw", "rgb", "rgb", "rgba", "rle", "rm", "rmvb", "roq", "sct", "sgi", "sgi", "sid", "stl",
    "sun", "svg", "svi", "sxd", "tga", "tga", "tif", "tiff", "v2d", "vnd", "vob", "vrml", "vtf", "wdp", "webm", "webp",
    "wmf", "wmv", "x3d", "xar", "xbm", "xcf", "xls", "xlsx", "xpm", "yuv"
])

def process_links(base_url: Optional[str], links: Iterable[str]) -> Generator[str, None, None]:
    """
    Resolve, clean and filter links found in a page. By links we mean here any value of `href` attribute found
    in a page. This is especially useful for the

    In addition to what :py:meth:`fix_url` does, this method will also exclude:

    * the base URL
    * Duplicates

    For two links to be considered duplicates, they need to match exactly. Exceptions are anchors (stripped
    automatically) and trailing slashes (in this case, the first encountered link will be returned).

    :param base_url: the URL of the current page (not returned and used to resolve relative links). Use '' to ignore.
    :param links: a list of links found, relative or absolute
    :return: a generator of unique absolute URLs, all beginning with `http`
    """
    seen = set()  # keep a set of seen urls

    if base_url is not None:
        seen.update([base_url, base_url + '/'])

    for link in links:
        fixed_url, ok = fix_url(link, base_url)
        if ok and fixed_url not in seen:
            yield fixed_url
            # add it as is
            seen.add(fixed_url)
            # avoid duplicate links with just an ending slash that differ
            seen.add(fixed_url[:-1] if fixed_url.endswith('/') else fixed_url + '/')


def fix_url(url: str, base_url: str = None) -> (str, bool):
    """
    Fix/normalize an URL and decide if it is interesting to crawl.

    The URL is potentially transformed by:

        * resolving relative to absolute URLs (only if base_url is set)
        * removing anchors

    The "is interesting" decision will exclude:

        * relative URLs (so ensure to provide a base_url if the url is relative)
        * non HTTP links (`mailto:`, `javascript:`, anchors, ...)

    :param url: the url
    :param base_url: the base url, required if the url is a relative one
    :return: a tuple (fixed_url, is_interesting)
    """
    if base_url is not None:
        # make relative into absolute links
        if base_url.endswith('/'):
            # remove the ending "/", because of a weird behavior of urljoin:
            #  urljoin('http://example.com/page1/', 'page2') => 'http://example.com/page1/page2'
            #  urljoin('http://example.com/page1', 'page2') => 'http://example.com/page2'
            base_url = base_url[:-1]
        url = up.urljoin(base_url, url)

    parsed: up.ParseResult = up.urlparse(url)

    if parsed.fragment:
        parsed = parsed._replace(fragment='')

    # ensure it is a HTTP or HTTPS URL
    if not (parsed.scheme and parsed.scheme.startswith('http')):
        return up.urlunparse(parsed), False  # return what we got so far

    # we got this far, the URL should not be fixed and worth keeping
    return up.urlunparse(parsed), True


def is_media_link(url: Union[up.ParseResult, str]) -> bool:
    """
    Check if an url contains a known media extension
    :param url: a URL, either in form of a string or an already "parsed" URL
    :return: true if most probably a media link (pdf, image, video, audio, etc.) false otherwise
    """
    if isinstance(url, str):
        parsed: up.ParseResult = up.urlparse(url)
    elif isinstance(url, up.ParseResult):
        parsed = url
    else:
        raise Exception(f'Expecting a string or a urlparse.ParseResult, got {type(url)}')

    # path contains a media extension
    # or query ends with a media extension (e.g. ?doc=lala.pdf)
    return '.' in parsed.path and parsed.path.split(".")[-1].lower() in MEDIA_EXTENSIONS or \
           '.' in parsed.query and parsed.query.split(".")[-1].lower() in MEDIA_EXTENSIONS
