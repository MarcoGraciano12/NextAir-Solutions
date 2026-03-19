"""
Module: icecast.py

Basic Icecast client for sending audio streams.

Author: Marco Graciano
Date: March 18, 2026
"""

import socket
from base64 import b64encode
from logging import Logger, getLogger
from threading import Event, Lock
from urllib.parse import urlparse


class Icecast:
    """
    Basic client to connect and stream audio to an Icecast server.
    """

    ICECAST_PORT = 8000
    SUPPORTED_SCHEMES = ("http",)

    def __init__(self, name: str, url: str, user: str, password: str, logger: Logger = None, **headers):
        """
        Initialize Icecast client settings.

        :param name: Identifier for this Icecast instance
        :param url: Icecast server URL with mountpoint
        :param user: Source username
        :param password: Source password
        :param logger: Logger instance
        :param headers: Extra Icecast headers
        """
        self.__name = name or self.__class__.__name__
        self.__logger = logger or getLogger(self.__name)

        parsed = urlparse(url)

        if parsed.scheme not in self.SUPPORTED_SCHEMES:
            raise ValueError(f"Protocol '{parsed.scheme}' is not supported")

        if not parsed.hostname:
            raise ValueError("Host is required in URL")

        if not parsed.path or parsed.path == "/":
            raise ValueError("Mountpoint is required in URL")

        self.__user = user
        self.__password = password
        self.__host = parsed.hostname
        self.__port = parsed.port or self.ICECAST_PORT
        self.__mount = parsed.path
        self.__headers = headers

        self.__lock = Lock()
        self.__stop_event = Event()
        self.__connection = None

    @property
    def name(self) -> str:
        """
        Get Icecast instance name.
        """
        return self.__name

    @property
    def user(self) -> str:
        """
        Get source username.
        """
        return self.__user

    @property
    def host(self) -> str:
        """
        Get Icecast server host.
        """
        return self.__host

    @property
    def port(self) -> int:
        """
        Get Icecast server port.
        """
        return self.__port

    @property
    def mount(self) -> str:
        """
        Get stream mountpoint.
        """
        return self.__mount

    @property
    def headers(self) -> dict:
        """
        Get custom headers.
        """
        return self.__headers

    @property
    def is_alive(self) -> bool:
        """
        Check if Icecast connection is active.
        """
        return not self.__stop_event.is_set()

    def is_connected(self) -> bool:
        """
        Check if the Icecast connection is active.

        :return: True when connection is active, else False.
        """
        with self.__lock:
            return self.__connection is not None

    def __build_source_request(self, content_type: str) -> str:
        """
        Build HTTP SOURCE request with authentication headers.

        :param content_type: Stream content type
        :return: Complete HTTP request string
        """
        # Build Basic authentication token
        auth_raw = f"{self.__user}:{self.__password}".encode("utf-8")
        auth_token = b64encode(auth_raw).decode("ascii")

        # Build HTTP SOURCE request with headers
        request = (
            f"SOURCE {self.__mount} HTTP/1.0\r\n"
            f"Authorization: Basic {auth_token}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"icy-pub: 1\r\n"
        )

        # Add custom headers if provided
        for key, value in self.__headers.items():
            request += f"{key}: {value}\r\n"

        # End headers with double newline
        request += "\r\n"

        return request

    def connect(self, content_type: str = "application/ogg") -> bool:
        """
        Open connection to Icecast and send source headers.

        :param content_type: Stream content type
        :return: True if connected successfully, False otherwise
        """
        with self.__lock:
            if self.__connection is not None:
                self.__logger.warning("Already connected to Icecast")
                return False

        # Build HTTP SOURCE request
        request = self.__build_source_request(content_type)

        # Create TCP socket with connection timeout
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(10.0)

        try:
            connection.connect((self.__host, self.__port))
            connection.sendall(request.encode("utf-8"))

            # Icecast responds with HTTP status
            response = connection.recv(4096).decode("utf-8", errors="replace")

            if "200 OK" not in response:
                self.__logger.error(f"Icecast rejected: {response.strip()}")
                connection.close()
                return False

            # Remove timeout for streaming
            connection.settimeout(None)

            with self.__lock:
                self.__connection = connection
                self.__stop_event.clear()

            self.__logger.info(f"Connected to Icecast at {self.__host}:{self.__port}{self.__mount}")
            return True

        except Exception as error:
            self.__logger.error(f"Failed to connect: {error}")
            connection.close()
            return False

    def send(self, data: bytes) -> bool:
        """
        Send audio data to Icecast server.

        :param data: Encoded audio data to transmit
        :return: True if sent successfully, False otherwise
        """
        if self.__stop_event.is_set():
            return False

        try:
            self.__connection.sendall(data)
            return True

        except (BrokenPipeError, ConnectionResetError) as error:
            self.__logger.error(f"Connection lost: {error}")
            self.__stop_event.set()  # Signal failure, let disconnect() clean up
            return False

        except Exception as error:
            self.__logger.error(f"Failed to send data: {error}")
            self.__stop_event.set()
            return False

    def disconnect(self) -> bool:
        """
        Close connection to Icecast server.

        :return: True if disconnected successfully, False if not connected
        """
        with self.__lock:
            if self.__connection is None:
                self.__logger.warning("Not connected to Icecast")
                return False

            self.__stop_event.set()
            connection = self.__connection
            self.__connection = None

        try:
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
            self.__logger.info("Disconnected from Icecast")
            return True

        except Exception as error:
            self.__logger.error(f"Error closing connection: {error}")
            return False
