import os
import socket
import logging
from socketserver import BaseRequestHandler

from utils.tls_wrapper import TLSWrapper


class UDPHandler(BaseRequestHandler):


    def handle(self) -> None:
        """
        Receive all the incoming UDP requests and handles the communication with the DoT provider server in a infinite loop
        uses the wrapper utils to send all the UDP request over TCP.

        :return: the response from the DoT provider
        """

        try:
            logging.info(f'Incoming UDP connection from {self.client_address}')

            tls_wrapper = TLSWrapper()

            msg, sock = self.request

            tls_answer = tls_wrapper.wrapper(self.udp_to_tcp(msg), hostname=os.getenv('DOT_SERVER'))

            sock.sendto(tls_answer[2:], self.client_address)

        except socket.timeout as err:
            logging.error('TIMEOUT ERROR: %s', err)
        except socket.error as err:
            logging.error('ERROR OCCURRED: %s', err)

    @staticmethod
    def udp_to_tcp(packet) -> bytes:
        """
        Translate the UDP incoming package into a TCP valid one for their use in the wrapper.

        :param packet: UDP package to convert
        :return: translation of a UDP package in TCP format
        """
        packet_len = bytes([00]) + bytes([len(packet)])

        return packet_len + packet

