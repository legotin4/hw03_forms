import pytest
from bs4 import BeautifulSoup


class TestTemplateView:

    @pytest.mark.django_db(transaction=True)
    def test_about_author_tech(self, client):
        urls = ['/about/author/', '/about/tech/']
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
            assert response.status_code != 404, f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
            assert response.status_code == 200, (
                f'Ошибка {response.status_code} при открытиии `{url}`. Проверьте ее view-функцию'
            )

    @pytest.mark.django_db(transaction=True)
    def test_header_urls(self, client):
        urls = ['/about/author/', '/about/tech/']
        response = client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        about = soup.body.header.nav.div.ul.find_all('a')
        hrefs = []

        for page in about:
            hrefs.append(page.get('href'))

        for url in urls:
            assert url in hrefs, (
                f'Убедитесь, что в шапке главной страницы есть ссылка на `{url}`'
            )
