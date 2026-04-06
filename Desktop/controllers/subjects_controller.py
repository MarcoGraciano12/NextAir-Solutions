
from threading import Lock
from logging import Logger, getLogger
from scripts.decoders import Decoder
from scripts.inputs import StreamInput
from scripts.subjects import StreamSubject
from scripts.subjects import DeviceSubject


class SubjectsController:

    def __init__(self, logger: Logger = None):

        self.__lock = Lock()
        self.__stream_subjects = {}
        self.__subjects = {}
        self.__logger = logger or getLogger(self.__class__.__name__)

    def add_device_subject(self, name: str, **kwargs):
        """
        Add a new device subject to the registry.

        :param name: Unique identifier for the device subject
        :param kwargs: Additional configuration parameters for DeviceSubject
        :return: Tuple (success: bool, error_message: str or None)
        """
        with self.__lock:
            # Check if subject already registered
            if name in self.__subjects:
                return False, f"{name} subject already exists"

            # Create and register new subject
            self.__subjects[name] = DeviceSubject(name, **kwargs)

            return True, None

    def remove_device_subject(self, name: str):
        """
        Remove and stop a device subject from the registry.

        :param name: Unique identifier of the device subject to remove
        :return: Tuple (success: bool, error_message: str or None)
        """
        with self.__lock:
            # Remove subject from registry atomically
            subject = self.__subjects.pop(name, None)

            if not subject:
                return False, f"{name} subject not found"

        # Stop subject outside lock to avoid blocking other operations
        subject.stop()

        return True, None

    def get_subject(self, name: str):
        """
        Retrieve a device subject from the registry.

        :param name: Unique identifier of the device subject
        :return: DeviceSubject instance or None if not found
        """
        with self.__lock:
            return self.__subjects.get(name, None)


    # @property
    # def stream_subjects(self):
    #     return self.__stream_subjects
    #
    # def get_stream_subject(self, name: str):
    #     """
    #     Retrieves a stream subject by name.
    #
    #     :param name: Identifier of the stream subject
    #     :return: StreamSubject or None
    #     """
    #     with self.__lock:
    #         return self.__stream_subjects.get(name, None)
    #
    # def add_stream_subject(self, name: str, **kwargs):
    #     """
    #     Creates and registers a new stream subject with its decoder and subject.
    #
    #     :param name: Unique identifier for the stream subject
    #     :param kwargs: Additional parameters passed to the Decoder constructor
    #     :return: Tuple (success: bool, error_message: str)
    #     """
    #     try:
    #         with self.__lock:
    #             if name in self.__stream_subjects:
    #                 return False, f"{name} already exists"
    #
    #         decoder = Decoder(name=name, **kwargs)
    #         stream_input = StreamInput(name=name, decoder=decoder)
    #         stream_subject = StreamSubject(stream_input=stream_input)
    #
    #         with self.__lock:
    #             if name in self.__stream_subjects:
    #                 self.__logger.warning(f"{name} added by another thread during creation")
    #                 return False, f"{name} already exists"
    #
    #             self.__stream_subjects[name] = stream_subject
    #             return True, None
    #
    #     except Exception as error:
    #         self.__logger.error(f"Failed to create stream subject {name}: {error}")
    #         return False, str(error)
    #
    # def remove_stream_subject(self, name: str):
    #     """
    #     Stops and removes a stream subject from the registry.
    #
    #     :param name: Identifier of the stream subject to remove
    #     :return: Tuple (success: bool, error_message: str)
    #     """
    #     try:
    #         with self.__lock:
    #             subject = self.__stream_subjects.get(name, None)
    #
    #         if not subject:
    #             self.__logger.warning(f"Stream subject {name} not found")
    #             return False, "Not found"
    #
    #         subject.stop()
    #
    #         with self.__lock:
    #             self.__stream_subjects.pop(name, None)
    #
    #         return True, None
    #
    #     except Exception as error:
    #         self.__logger.error(f"Failed to remove stream subject {name}: {error}")
    #         return False, str(error)
