import gc
import logging
import signal
import tempfile
from multiprocessing import Process, Manager, Value
from pathlib import Path
from queue import Empty
from subprocess import Popen, PIPE
from time import sleep, time

from config import RADARE_PORTS, RADARE_TIMEOUT, QUEUE_BLOCK_TIMEOUT


class OutOfPortsError(Exception):
    pass


class RadareRunner:
    def __init__(self, request_timeout=30):
        self._request_timeout = request_timeout
        self._queue_manager = Manager()

        self._in_queue = self._queue_manager.Queue()

        self._ports = self._queue_manager.Queue()
        for port in RADARE_PORTS:
            self._ports.put(port)

        self._shutdown_condition = Value('i', 0)
        self._worker = self._start_worker()

    def _start_worker(self):
        processes = list()
        for _ in RADARE_PORTS:
            worker = Process(target=self.look_for_tasks)
            worker.start()
            processes.append(worker)
        return processes

    def __del__(self):
        self._shutdown_condition.value = 1
        for worker in self._worker:
            worker.join()
        gc.collect()

    def look_for_tasks(self):
        logging.debug('{} Enter function'.format(time()))
        while self._shutdown_condition.value == 0:
            try:
                task = self._in_queue.get(timeout=QUEUE_BLOCK_TIMEOUT)
            except Empty:
                pass
            except Exception as exception:
                logging.debug('Finished with {}'.format(type(exception)))
                break
            else:
                self.add_radare_task(task)
        if self._shutdown_condition.value == 1:
            logging.warning('Finished with shutdown condition')
        logging.info('{} Shutting down worker gracefully ..'.format(time()))

    def pseudo_start(self, binary):
        try:
            port = self._retrieve_free_port()
        except Empty:
            raise OutOfPortsError('Timeout for open port exceeded. Please try again later.')
        self._in_queue.put((port, binary))
        return port

    def _retrieve_free_port(self):
        return self._ports.get(timeout=self._request_timeout)

    def add_radare_task(self, task):
        port, binary = task
        wrap_radare_call(port=port, binary=binary)
        self._ports.put(port)


def start_radare_instance(port, binary_path):
    command = 'r2 -q -c=H -e http.bind=0.0.0.0 -e http.port={} -e http.browser= {}'.format(port, binary_path)
    with Popen(command.split(' '), shell=False, stdout=PIPE, stderr=PIPE) as radare_process:
        sleep(RADARE_TIMEOUT)
        radare_process.send_signal(signal.SIGKILL)
        logging.info('Killed radare instance')


def wrap_radare_call(port, binary):
    temporary_file = create_file_from_binary(binary)
    start_radare_instance(port, temporary_file.name)
    temporary_file.close()


def create_file_from_binary(binary):
    temporary_file = tempfile.NamedTemporaryFile()
    with Path(temporary_file.name) as path:
        path.write_bytes(binary)
    return temporary_file
