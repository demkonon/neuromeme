import secrets

from server.bp import bp
from server.website import Website
from server.backend import Backend_Api
from server.babel import create_babel
from json import load
from flask import Flask


def start_app():

    # Определение Flask-приложения
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)

    # Настройка Babel
    create_babel(app)

    # Настройка маршрутов сайта
    site_config = None
    url_prefix = None
    site = None
    backend_api = None

    # Функция для загрузки конфигурации и настройки приложения
    def setup_app():
        global site_config, url_prefix, site, backend_api
        # Загрузка конфигурации из config.json
        config = load(open('config.json', 'r'))
        site_config = config['site_config']
        url_prefix = config.pop('url_prefix')

        # Настройка маршрутов сайта
        site = Website(bp, url_prefix)
        for route in site.routes:
            bp.add_url_rule(
                route,
                view_func=site.routes[route]['function'],
                methods=site.routes[route]['methods'],
            )
        # Настройка маршрутов API
        backend_api = Backend_Api(bp, config)
        for route in backend_api.routes:
            bp.add_url_rule(
                route,
                view_func=backend_api.routes[route]['function'],
                methods=backend_api.routes[route]['methods'],
            )
        # Регистрация blueprint
        app.register_blueprint(bp, url_prefix=url_prefix)

        print(f"Running on {site_config['port']}{url_prefix}")
        app.run(**site_config)
        print(f"Closing port {site_config['port']}")


    setup_app()

start_app()