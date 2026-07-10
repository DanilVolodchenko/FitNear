import webbrowser

import jinja2

from application.interfaces.template import IHTMLTemplate
from core.config_path import BASE_PATH


class HTMLTemplate(IHTMLTemplate):
    async def generate(self, **kwargs: str | int) -> str:
        path = BASE_PATH / 'infrastructure'

        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(BASE_PATH / 'infrastructure'))
        template = environment.get_template('confirm_email_template.html')

        rend_html = template.render(
            language='en', title='Test', description='Для подтверждения электронной почты нажмите на кнопку'
        )

        output_file = path / 'ready_page.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rend_html)

        webbrowser.open(output_file.as_uri())
