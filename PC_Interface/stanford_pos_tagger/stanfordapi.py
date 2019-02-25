# -*- coding: utf-8 -*-
import socket
import time
from subprocess import Popen
from unidecode import unidecode


class StanfordAPI:
    """Used to initialize the Stanford POS tagger in servlet mode and then connect to it using a socket"""

    def __init__(self, path_to_model='stanford_pos_tagger/english-bidirectional-distsim.tagger',
                 path_to_jar='stanford_pos_tagger/stanford-postagger.jar', port=5001, buffer_size=4096):
        """Used to initialize the StanfordAPI object with the host, port and buffer"""
        self.host = socket.gethostname()
        self.port = port
        self.buffer = buffer_size
        self.process = Popen(
            ['java', '-mx2g', '-cp', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTaggerServer',
             '-model', path_to_model, '-port', '5001', '-sentenceDeLimiter', 'newline'])
        time.sleep(5)

    def pos_tag(self, message):
        """Used to send requests to the socket"""
        s = socket.socket()
        s.connect((self.host, self.port))
        if message.strip() == '':
            s.close()
            return []
        s.send(to_ascii(message))
        data = s.recv(self.buffer)
        s.close()
        return [tuple(x.rsplit('_', 1)) for x in unidecode(data.decode('ascii', 'ignore')).strip().split()]

    def __del__(self):
        """ Terminating the process """
        self.process.terminate()


def to_ascii(message):
    if message is None or message.strip() == '':
        return ''
    return (unidecode(message) + '\n').encode('ascii', errors='ignore')

