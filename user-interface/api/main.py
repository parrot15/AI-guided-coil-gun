from gevent import monkey

monkey.patch_all()

from endpoints import app, server_socket
from parse_config_file import config

if __name__ == "__main__":
    server_socket.run(
        app,
        debug=config.getboolean("Server", "debug"),
        host=config.get("Server", "host"),
        port=config.getint("Server", "port"),
    )
