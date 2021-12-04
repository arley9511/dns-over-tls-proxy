import os
import logging
import multiprocessing
from socketserver import ThreadingTCPServer, ThreadingUDPServer

from handler.tcp_handler import TCPHandler
from handler.udp_handler import UDPHandler

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

if 'DOT_SERVER' not in os.environ:
    # Set as default cloudfare if is not configure any other DoT server
    os.environ['DOT_SERVER'] = '1.1.1.1'

def main() -> None:
    logging.info(f"The DoT server configured is: {os.getenv('DOT_SERVER')}")

    port  = 53

    ThreadingTCPServer.allow_reuse_address = True
    ThreadingUDPServer.allow_reuse_address = True

    tcp_proxy = ThreadingTCPServer(('', port), TCPHandler)
    udp_proxy = ThreadingUDPServer(('', port), UDPHandler)

    tcp_process = multiprocessing.Process(target=tcp_proxy.serve_forever)
    udp_process = multiprocessing.Process(target=udp_proxy.serve_forever)

    tcp_process.start()
    logging.info(f'DNS Proxy over TCP started and listening on port {port}')
    udp_process.start()
    logging.info(f'DNS Proxy over UDP started and listening on port {port}')


if __name__ == '__main__':
    main()
