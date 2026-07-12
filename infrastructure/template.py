import webbrowser
from pathlib import Path

import jinja2

from application.interfaces.template import IHTMLTemplate
from core.config_path import BASE_PATH

CONFIRM_EMAIL_TEMPLATE: str = """
<html lang="{{ language }}">
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        <div>{{ description }}</div>
    </body>
</html>
"""


class HTMLTemplate(IHTMLTemplate):
    async def generate(self, template_path: Path, **kwargs: str | int) -> str:

        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path.parent),
            autoescape=True,
            enable_async=True,
        )

        # template = jinja2.Template(tmpl, enable_async=True)
        template = environment.get_template('confirm_email.html')

        rend_html = await template.render_async(**kwargs)
        import io
        import tempfile

        bytes_io_buffer = io.BytesIO(rend_html.encode('utf-8'))

        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
            temp_file.write(bytes_io_buffer.getvalue())
            temp_file_path = temp_file.name

        webbrowser.open(f'file://{temp_file_path}')
