import time
import threading
from flask import Flask, request

from write_thread import setup_driver, write_thread

app = Flask(__name__)
driver = setup_driver()

# 書きこみ設定
# body is Noneのとき書き込まれない
# cycle is Noneのとき1度だけ書き込まれる
server, board, thread = None, None, None
body, name, mail = None, None, None
cycle, count = None, 0
status, err_str = None, None


def write_loop():
    global body, count, status, err_str

    while True:
        if body is not None:
            if count > 0:
                count -= 1
            else:
                count = cycle
                try:
                    status, err_str = write_thread(driver, server, board, thread, body, name, mail)
                except Exception as e:
                    status, err_str = False, f"internal server error: {e}"

                if cycle is None:
                    body = None
                    count = 0
        time.sleep(1)


@app.route('/stop/', methods=['POST'])
def stop():
    global body
    body = None
    return "ok", 200


@app.route('/<server_>/<board_>/<thread_>/', methods=['POST'])
def register(server_, board_, thread_):
    global server, board, thread
    global body, name, mail
    global cycle, count
    global status
    server, board, thread = server_, board_, thread_
    name = request.form.get('name', type=str)
    mail = request.form.get('mail', type=str)
    cycle = request.form.get('cycle', type=int)
    count = 0
    status = None
    body = request.form.get('body', type=str)

    while status is None:
        time.sleep(0.5)

    return f"status: {status}\n{err_str}", 200


@app.route('/')
def index():
    return app.send_static_file(filename='index.html')


@app.route('/restart/', methods=['POST'])
def restart():
    global driver, body
    body = None
    driver.quit()
    time.sleep(2)
    driver = setup_driver()
    return "ok", 200


if __name__ == '__main__':
    threading.Thread(target=write_loop).start()
    app.run(host='0.0.0.0', port=8080)
