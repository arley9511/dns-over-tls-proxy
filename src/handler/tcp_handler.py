import os
import socket
import logging
from socketserver import BaseRequestHandler

from utils.tls_wrapper import TLSWrapper


class TCPHandler(BaseRequestHandler):


    def handle(self) -> None:
        """
        Receive all the incoming TCP requests and handles the communication with the DoT provider server in a infinite loop

        :return: the response from the DoT provider
        """
        try:
            logging.info(f'Incoming TCP connection from {self.client_address}')

            tls_wrapper = TLSWrapper()

            while True:
                msg = self.request.recv(1024)

                if not msg:
                    break

                answer = tls_wrapper.wrapper(msg, hostname=os.getenv('DOT_SERVER'))

                self.request.send(answer)

        except socket.timeout as err:
            logging.error('TIMEOUT ERROR: %s', err)
        except socket.error as err:
            logging.error('ERROR OCCURRED: %s', err)

            self.request.close()
