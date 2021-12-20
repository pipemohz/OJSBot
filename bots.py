from bs4 import BeautifulSoup
import requests
from requests.models import HTTPError
from requests.exceptions import Timeout


BASE_URL = "https://revistas.uexternado.edu.co/index.php/"
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
            requests.get(url=url, timeout=3).raise_for_status()
        except (HTTPError, Timeout):
            return False
        else:
            return True

    def inspect_page_components(self, soup: BeautifulSoup) -> dict:

        checklist = {
            'titulo articulo': '.media-heading a',
            'autores': '.authors',
            'vistas_pdf': '.issue-stats.text-muted',
            'galerada_pdf': '.galley-link.btn.obj_galley_link.pdf',
            'logo_revista': '.navbar-brand-logo.logo_revista'
        }

        components = {name: 'SI' for name, selector in checklist.items(
        ) if soup.select_one(selector=selector) != None}

        components['metric_buttons'] = {a.text.lower(): a.get(
            'href') for a in soup.select(selector='.btn.btn-default.analytics_btn')}
        return components

    def inspect_navigation_bar(self, soup: BeautifulSoup) -> dict:
        nav_bar_items = [
            item.text.strip('\n\t').lower() for item in soup.select('#main-navigation li')]
        nav_bar_URLs = [a.get('href') for a in soup.select(
            selector="#main-navigation li a")]

        nav_bar = {}

        for i in range(len(nav_bar_items)):
            if self.valid_URL(nav_bar_URLs[i]):
                nav_bar[nav_bar_items[i]] = nav_bar_URLs[i]

        return nav_bar

    def inspect_sidebar_blocks(self, soup: BeautifulSoup) -> dict:

        block_names = [block.text.lower() for block in soup.select(
            selector=".title")]
        custom_blocks = {
            'block_names': block_names
        }
        return custom_blocks

    def inspect_journal_home(self, url: str) -> dict:
        try:
            request = requests.get(url=url, headers=headers, timeout=10)
        except Timeout:
            return {}
        else:
            soup = BeautifulSoup(request.text, "html.parser")

            checklist = {
                'journal': soup.title.text.strip('\n\t')
            }

            nav_bar = self.inspect_navigation_bar(soup)
            blocks = self.inspect_sidebar_blocks(soup)
            components = self.inspect_page_components(soup)

            checklist.update(nav_bar)
            checklist.update(blocks)
            checklist.update(components)

            return checklist

    def extract_urls(self) -> list:
        sitemap_url = f"{BASE_URL}index/sitemap"
        soup = BeautifulSoup(requests.get(
            url=sitemap_url, headers=headers).text, "lxml-xml")
        urls = [tag.text.strip('sitemap') for tag in soup.find_all(name="loc")]
        return urls

    def audit_journals(self) -> None:
        self.create_report()
        for journal_url in self.extract_urls():
            checklist = self.inspect_journal_home(url=journal_url)
            self.fill_report(checklist=checklist)

    def create_report(self) -> None:
        with open('report.csv', mode='w') as file:
            file.write(
                'Revista,Tutoriales,Acerca de,Formatos,Indexada en,Scholar,mas_leidos,Palabras clave,Más descargados,\
                Código QR,Información,Inicio revista,Avisos,Actual,Archivos,titulo articulo,autores,vistas pdf,\
                galerada pdf,logo revista,métricas,estadísticas de la revista,analíticas\n')

    def fill_report(self, checklist: dict) -> None:
        columns = ['tutoriales', 'acerca de', 'formatos',
                   'indexada en', 'scholar', 'mas_leidos', 'palabras clave', 'más descargados en los ultimos 30 días',
                   'código qr', 'información', 'inicio revista', 'avisos', 'actual', 'archivos', 'titulo articulo',
                   'autores', 'vistas_pdf', 'galerada_pdf', 'logo_revista', 'métricas', 'estadísticas de la revista', 'analíticas']
        with open(file='report.csv', mode='a') as file:
            file.write(f"{checklist.get('journal')},")
            for column in columns:
                if column in checklist.keys():
                    file.write('SI,')
                elif checklist.get('block_names') != None:
                    if column in checklist['block_names']:
                        file.write('SI,')
                    else:
                        file.write('NO,')
                elif checklist.get('metric_buttons') != None:
                    if column in checklist['metric_buttons'].keys():
                        file.write('SI,')
                    else:
                        file.write('NO,')
                else:
                    file.write('NO,')

            file.write('\n')
