from bs4 import BeautifulSoup
import requests
from requests.models import HTTPError


BASE_URL = "https://revistas.uexternado.edu.co/index.php/"
article_route = ""
headers = {
    "Accept-Language": "en,es-ES;q=0.9,es;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}


class AuditBot():
    def __init__(self) -> None:
        self.audit_journals()
        # pass

    def valid_URL(self, url: str) -> bool:
        try:
            requests.get(url=url).raise_for_status()
        except HTTPError:
            return False
        else:
            return True

    def inspect_sidebar_blocks(self, url: str):
        soup = BeautifulSoup(requests.get(
            url=url, headers=headers).text, "html.parser")
        block_names = [block.text.lower() for block in soup.select(
            selector=".title")]
        custom_blocks = {
            'journal': soup.title.text.strip('\n\t'),
            'block_names': block_names
        }
        return custom_blocks

    def inspect_journal_home(self, url: str):
        soup = BeautifulSoup(requests.get(
            url=url, headers=headers).text, "html.parser")
        nav_bar_items = [
            item.text.strip('\n\t').lower() for item in soup.select('#main-navigation li')]
        nav_bar_URLs = [a.get('href') for a in soup.select(
            selector="#main-navigation li a")]

        nav_bar = {}
        for i in range(len(nav_bar_items)):
            if self.valid_URL(nav_bar_URLs[i]):
                nav_bar[nav_bar_items[i]] = nav_bar_URLs[i]
        return nav_bar

    def extract_urls(self):
        sitemap_url = f"{BASE_URL}index/sitemap"
        soup = BeautifulSoup(requests.get(
            url=sitemap_url, headers=headers).text, "lxml-xml")
        urls = [tag.text.strip('sitemap') for tag in soup.find_all(name="loc")]
        return urls

    def audit_journals(self):
        self.create_report()
        for journal_url in self.extract_urls():
            blocks = self.inspect_sidebar_blocks(url=journal_url)
            nav_bar = self.inspect_journal_home(url=journal_url)
            self.fill_report(blocks=blocks, nav_bar=nav_bar)

    def create_report(self):
        with open('report.csv', mode='w') as file:
            file.write(
                'Revista,Tutoriales,Acerca de,Formatos,Indexada en,Scholar,mas_leidos,Palabras clave,Más descargados,Código QR,Información,Inicio revista,Avisos,Actual,Archivos\n')

    def fill_report(self, blocks: dict, nav_bar: dict):
        check_list = ['tutoriales', 'acerca de', 'formatos',
                      'indexada en', 'scholar', 'mas_leidos', 'palabras clave', 'más descargados en los ultimos 30 días', 'código qr', 'información', 'inicio revista', 'avisos', 'actual', 'archivos']
        with open(file='report.csv', mode='a') as file:
            file.write(f"{blocks.get('journal')},")
            for item in check_list:
                if item in blocks.get('block_names'):
                    file.write('SI,')
                elif item in nav_bar.keys():
                    file.write('SI,')
                else:
                    file.write('NO,')

            file.write('\n')
