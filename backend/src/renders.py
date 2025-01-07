import io

from rest_framework import renderers


class CSVShopingCartDataRenderer(renderers.BaseRenderer):

    media_type = "text/plain"
    format = 'txt'
    charset = 'cp1251'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        text_buffer = io.StringIO()

        for index, item in enumerate(data, start=1):
            line = (
                f"{index}) {item['ingredient__name']} - "
                f"{item['total_amount']} "
                f"{item['ingredient__measurement_unit']};"
            )
            text_buffer.write(line)
        return text_buffer.getvalue().encode(self.charset)
