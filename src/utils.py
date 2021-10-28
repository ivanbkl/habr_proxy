import re

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Comment, Tag

from settings import ProxySettings


def modify_html(html: str, new_hostname: str) -> str:
    soup = BeautifulSoup(html, 'html5lib')

    for tag in soup.find_all(name=True):
        if tag.name in ('script', 'style'):
            continue
        modify_attrs(tag, new_hostname, 'href', 'xlink:href', 'action')
        for child in tag.children:
            if isinstance(child, NavigableString) and not isinstance(child, Comment):
                modified_string = add_trademark(child.string)
                child.string.replace_with(modified_string)

    return soup.prettify()


def modify_attrs(tag: Tag, new_hostname: str, *attr_names: str) -> None:
    for attr_name in attr_names:
        if attr := tag.attrs.get(attr_name):
            tag[attr_name] = modify_url(attr, new_hostname)


def add_trademark(line: str) -> str:
    """Add trademark to each six-letter word in line"""
    return re.sub(r'\b(?P<match>\w{6})\b', r'\g<match>™', line)


def modify_url(url: str, new_hostname: str) -> str:
    return url.replace(f'https://{ProxySettings.DOMAIN}/', new_hostname, 1)
