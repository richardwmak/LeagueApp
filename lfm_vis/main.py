from   controller import start_server
import requests
from   threading import Thread
from   time import sleep
import webview


def run_app():  # noqa
    t = Thread(target=start_server)
    t.daemon = True
    t.start()

    # https://stackoverflow.com/a/15743618
    # https://github.com/r0x0r/pywebview/blob/master/examples/flask_app/src/backend/main.p
    url_accessible = False
    while not url_accessible:
        try:
            r = requests.head("http://127.0.0.1:5000")
            status_code = r.status_code
            if status_code == 200:
                url_accessible = True
        except requests.RequestException:
            url_accessible = False

        sleep(0.5)

    webview.create_window("test", "http://127.0.0.1:5000")


if __name__ == "__main__":
    start_server()

    # TODO: only use if not developing

    # run_app()
