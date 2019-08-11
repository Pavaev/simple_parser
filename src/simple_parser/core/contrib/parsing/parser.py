from urllib.parse import urljoin

import extruct
from bs4 import BeautifulSoup


class BaseParser:
    """
    If you want to create your custom parser, you should extend this base class
    """
    def __init__(self, html, url=None):
        self.html = html
        self.url = url
        self._parsed_data = {}

    def parse(self):
        pass


class DefaultParser(BaseParser):
    """
    Default parser based on <meta> tags
    """

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
    """
    Parser based on opengraph.
    See: https://ogp.me
    """
    def _get_extracted_data(self):
        extracted_data = extruct.extract(self.html, self.url, errors='ignore', syntaxes=['opengraph'], uniform=True)
        return extracted_data['opengraph']

    def parse(self):
        og_data = self._get_extracted_data()
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


class SchemaOrgParser(BaseParser):
    """
    Parser based on schema.org.
    See: http://schema.org
    """
    def _get_extracted_data(self):
        extracted_data = extruct.extract(self.html, self.url, errors='ignore', syntaxes=['microdata'], uniform=True)
        return extracted_data['microdata']

    def parse(self):
        data = self._get_extracted_data()
        main_entity_data = {}
        webpage_data = {}
        website_data = {}

        # Если item всего один, то выбор невелик, и считаем, что это то, что
        # нам нужно
        if len(data) == 1:
            self._parsed_data = data[0]
            return

        # Пытаемся достать по mainEntity или mainEntityOfPage
        for item in data:
            lower_keys_tuples = list(map(lambda x: (x[0].lower(), x[1]), item.items()))
            for k, v in lower_keys_tuples:

                # https://schema.org/mainEntity
                if k == 'mainentity':
                    main_entity_data = v
                    break

                # https://schema.org/mainEntityOfPage
                elif k == 'mainentityofpage':
                    # может быть строка или словарь
                    url = v
                    # нашелся сайт, где возможен и bool
                    # https://gtxtymt.xyz/blog/json-ld-base-structure-for-blog-on-laravel
                    if v is True:
                        main_entity_data = item
                        break

                    if isinstance(v, dict):
                        url = v.get('id', v.get('@id', ''))
                    if url == self.url:
                        main_entity_data = item

            if main_entity_data:
                break

            # Если mainEntity и mainEntityOfPage не будет, ищем тип webpage или
            # хотя бы website
            so_item_type = item['@type'].lower()
            if so_item_type == 'webpage':
                webpage_data = item
            elif so_item_type == 'website':
                website_data = item

        self._parsed_data = main_entity_data or webpage_data or website_data

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
            image = image.get('contentUrl', image.get('url'))
            if image and isinstance(image, list):
                image = image[0]
        return image


class JSONLDParser(SchemaOrgParser):
    """
    Parser based on json-ld using schema.org dictionary
    See: https://json-ld.org
    """

    def _get_extracted_data(self):
        extracted_data = extruct.extract(self.html, self.url, errors='ignore', syntaxes=['json-ld'], uniform=True)
        return extracted_data['json-ld']
