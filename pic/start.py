import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8000
URL = f'http://{HOST}:{PORT}'
ROOT = Path(__file__).resolve().parent


def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def wait_for_port(host: str, port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_port_open(host, port):
            return True
        time.sleep(0.1)
    return False


def main() -> None:
    if is_port_open(HOST, PORT):
        print(f'检测到服务已在运行：{URL}')
        webbrowser.open(URL)
        return

    server_script = ROOT / 'server.py'
    process = subprocess.Popen([sys.executable, str(server_script)], cwd=ROOT)

    if wait_for_port(HOST, PORT, timeout=10.0):
        print(f'服务已启动：{URL}')
        webbrowser.open(URL)
    else:
        print('服务启动超时，请检查 server.py 输出日志。')

    try:
        process.wait()
    except KeyboardInterrupt:
        print('\n正在停止服务...')
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == '__main__':
    main()
