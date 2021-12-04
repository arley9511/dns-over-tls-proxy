import ssl
import socket

class TLSWrapper:

    def wrapper(self, packet, hostname) -> bytes:
        """
        wrapper for send a incoming request to the DoT provider server, apply a 5 seconds timeout and uses the standard
        socket certificates to encrypt the communication.

        :param packet: message package
        :param hostname: Dot provider address
        :return: response form the Dot server
        """

        context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)

        with socket.create_connection((hostname, 853), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as tls_sock:
                tls_sock.send(packet)

                return tls_sock.recv(1024)
