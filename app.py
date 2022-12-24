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


def write_loop():
    global body, count

    while True:
        if body is not None:
            if count > 0:
                count -= 1
            else:
                count = cycle
                try:
                    write_thread(driver, server, board, thread, body, name, mail)
                except:
                    pass

                if cycle is None:
                    body = None
                    count = 0
        time.sleep(1)


@app.route('/stop/', methods=['POST'])
def stop():
    global body
    body = None
    print("stop request.")
    return "ok", 200


@app.route('/<server_>/<board_>/<thread_>/', methods=['POST'])
def register(server_, board_, thread_):
    global server, board, thread
    global body, name, mail
    global cycle, count
    server, board, thread = server_, board_, thread_
    body = request.form.get('body', type=str)
    name = request.form.get('name', type=str)
    mail = request.form.get('mail', type=str)
    cycle = request.form.get('cycle', type=int)
    count = 0
    print(f"register request at {server}/{board}/{thread}:")
    print(f"name: {name}, mail: {mail}, body: {body}")
    print(f"cycle: {cycle}, count: {count}")
    return "ok", 200


@app.route('/')
def index():
    return app.send_static_file(filename='index.html')


if __name__ == '__main__':
    threading.Thread(target=write_loop).start()
    app.run(host='0.0.0.0', port=5000)
