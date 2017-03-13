import re
from hashlib import sha1
from pathlib import Path
from typing import List


def find_indexes(haystack: List[str], regex: str) -> List[int]:
    """
    Find indexes in a list where a regular expression matches.

    Parameters
    ----------
    haystack
        List of strings.
    regex
        Regular expression to match.

    Returns
    -------
        The indexes where the regular expression was found.
    """
    return [i for i, item in enumerate(haystack) if re.search(regex, item)]


def find_style_file(filename, config):
    """
    TODO
    """
    outpath = config['local_path'] / 'out'
    filepath = outpath / config['style_path'] / config[filename]
    if not filepath.exists():
        filepath = outpath / '_style' / config[filename]
    if not filepath.exists():
        return
    return filepath.relative_to(filepath.parents[1])


def tweak_html_footer(html, footer):
    """
    TODO
    """
    if not footer:
        return False
    text = '<div class="footer">%s</div>' % footer
    for index in find_indexes(html, '<div class=\"reveal\">'):
        html.insert(index + 1, text)
    return True


def tweak_html_header(html, header):
    """
    TODO
    """
    if not header:
        return
    text = '<div class="header">%s</div>' % header
    for index in find_indexes(html, '<div class=\"reveal\">'):
        html.insert(index + 1, text)


def tweak_html_warmup(html, config):
    """
    TODO
    """
    fname = find_style_file('style_warmup', config)
    if not fname:
        return
    text = '<section><img src="%s" /></section>' % fname
    index = find_indexes(html, 'div class="slides"')[0]
    html.insert(index + 1, text)


def tweak_html_logo(html, config):
    """
    TODO
    """
    fname = find_style_file('style_logo', config)
    if not fname:
        return
    text = '<div class="logo"><img src="%s" /></div>' % fname
    for index in find_indexes(html, '<div class=\"reveal\">'):
        html.insert(index + 1, text)


def tweak_html_background(html, config):
    """
    TODO
    """
    fname = find_style_file('style_background', config)
    if not fname:
        return
    text = '<section data-background="%s">' % fname
    for index in find_indexes(html, '<section>'):
        html[index] = html[index].replace('<section>', text)


def tweak_html_css(html, config):
    """
    TODO
    """
    fname = find_style_file('style_custom_css', config)
    if not fname:
        return
    index = find_indexes(html, 'stylesheet.*id="theme"')[0]
    text = '<link rel="stylesheet" href="%s">' % fname
    html.insert(index + 1, text)
    return True


def tweak_html(html, config):
    """
    TODO
    """
    html = html.splitlines()
    style_version = sha1(config['style'].encode('utf')).hexdigest()
    style_path = Path('_style')
    # TODO: footer and header could be added to the style template (i.e.:
    #       within a config.yaml file part of the template which Markdownreveal
    #       should be able to load and override if necessary)
    tweak_html_footer(html, config['footer'])
    tweak_html_header(html, config['header'])
    tweak_html_warmup(html, config)
    tweak_html_logo(html, config)
    tweak_html_background(html, config)
    tweak_html_css(html, config)
    return '\n'.join(html)
