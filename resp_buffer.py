# -*- coding=utf-8 -*-
"""
buffer
@author wei.zheng
@date 2016.10.26
"""
from resp_exceptions import OutOfIndexException


class ResponseBuffer(object):

    def __init__(self, response_str):
        self.buffer = response_str.split('\r\n') if response_str else []
        self.buffer_index = -1

    def read_buffer(self):
        self.buffer_index += 1
        if self.buffer_index >= len(self.buffer):
            raise OutOfIndexException(self.buffer_index, len(self.buffer))
        return self.buffer[self.buffer_index]
