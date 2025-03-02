import mesop as me
from mesop.server.wsgi_app import create_app

from wsd.parsers import XLWSDParser

parser = XLWSDParser()
X, y = parser.parse("ja")

style_grid = me.Style(
    display="grid",
    grid_template_rows="auto 1fr auto",
    height="100%"
)
style_header = me.Style(
    background="#f0f0f0",
    padding=me.Padding.all(24)
)
style_body = me.Style(
    padding=me.Padding.all(24),
    overflow_y="auto"
)
style_footer = me.Style(
    background="#f0f0f0",
    padding=me.Padding.all(24)
)


@me.page(path="/")
def app():
    with me.box(style=style_grid):
        with me.box(style=style_header):
            me.text("SEMCOR WSD")

        with me.box(style=style_body):
            me.text(''.join(X[0]))

        with me.box(style=style_footer):
            me.text("Footer")


if __name__ == "__main__":
    app = create_app(prod_mode=True)
    app._flask_app.run(host="localhost", port=8080, use_reloader=True)
