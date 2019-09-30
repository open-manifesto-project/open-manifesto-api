from werkzeug.middleware.proxy_fix import ProxyFix

from manifesto.app import create_app
from manifesto.config import ProConfig


app = create_app(config=ProConfig)
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == "__main__":
    app.run()
