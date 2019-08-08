from urllib.parse import urljoin

import extruct
from bs4 import BeautifulSoup


class BaseParser:
    def __init__(self, html, url=None):
        self.html = html
        self.url = url
        self._parsed_data = {}

    def parse(self):
        pass


class DefaultParser(BaseParser):

    def parse(self):
        bs = BeautifulSoup(self.html)
        title = bs.title.string
        description = bs.find('meta', attrs={'name': 'description'}).get('content')
        favicon_url = bs.find('link', rel='shortcut icon').get('href')

        if favicon_url:
            favicon_url = urljoin(self.url, favicon_url)

        self._parsed_data = {
            'title': title,
            'description': description,
            'favicon_url': favicon_url,

        }

    @property
    def title(self):
        return self._parsed_data.get('title')

    @property
    def description(self):
        return self._parsed_data.get('description')

    @property
    def favicon_url(self):
        return self._parsed_data.get('favicon_url')


class OpenGraphParser(BaseParser):

    def parse(self):
        extracted_data = extruct.extract(self.html, self.url, errors='ignore', syntaxes=['opengraph'], uniform=True)
        og_data = extracted_data['opengraph']
        if og_data:
            self._parsed_data = og_data[0]

    @property
    def title(self):
        return self._parsed_data.get('og:title')

    @property
    def description(self):
        return self._parsed_data.get('og:description')

    @property
    def favicon_url(self):
        return self._parsed_data.get('og:image')


class JSONLDParser(BaseParser):

    def parse(self):
        extracted_data = extruct.extract(self.html, self.url, errors='ignore', syntaxes=['json-ld'], uniform=True)
        jsld_data = extracted_data['json-ld']
        for jsld_item in jsld_data:
            # Крайне проблематично узнать, какой из объектов нужен
            if set(jsld_item.keys()) & {'name', 'headline', 'description', 'about'}:
                self._parsed_data = jsld_item
                break

    @property
    def title(self):
        return self._parsed_data.get('name') or self._parsed_data.get('headline')

    @property
    def description(self):
        return self._parsed_data.get('description') or self._parsed_data.get('about')

    @property
    def favicon_url(self):
        image = self._parsed_data.get('image')
        if isinstance(image, dict):
            image = image.get('url')
        return image


class SchemaOrgParser(BaseParser):
    def parse(self):
        extracted_data = extruct.extract(self.html, self.url, errors='ignore', syntaxes=['microdata'], uniform=True)
        so_data = extracted_data['microdata']
        for so_item in so_data:
            # Крайне проблематично узнать, какой из объектов нужен
            if set(so_item.keys()) & {'name', 'headline', 'description', 'about'}:
                self._parsed_data = so_item
                break

    @property
    def title(self):
        return self._parsed_data.get('name') or self._parsed_data.get('headline')

    @property
    def description(self):
        return self._parsed_data.get('description') or self._parsed_data.get('about')

    @property
    def favicon_url(self):
        image = self._parsed_data.get('image')
        if isinstance(image, dict):
            image = image.get('url')
        return image
