import importlib


def _load_flask():
    try:
        return importlib.import_module("flask")
    except ModuleNotFoundError:
        class _Flask:
            def __init__(self, name):
                self.name = name

            def route(self, path):
                def decorator(func):
                    return func

                return decorator

            def run(self, port=5000, **kwargs):
                print(f"Flask is not installed. Running fallback mode on port {port}.")

        return type("_FallbackFlaskModule", (), {"Flask": _Flask})()


flask_module = _load_flask()
Flask = flask_module.Flask

app = Flask(__name__)


@app.route("/")
def merhaba():
    return "Ortam calisiyor!"


if __name__ == "__main__":
    app.run(port=5000)