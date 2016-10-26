# -*- coding=utf-8 -*-


class ProtocolArgLengthException(Exception):

    def __init__(self, current_length, protocal_arg_length):
        message = 'current length is {}, protocal length is {}'.format(current_length, protocal_arg_length)
        super(ProtocolArgLengthException, self).__init__(message)


class ProtocolArgsNumberException(Exception):

    def __init__(self):
        message = 'wrong Args Number'
        super(ProtocolArgsNumberException, self).__init__(message)


class RequestFormatStartException(Exception):

    def __init__(self):
        message = 'not start with *'
        super(RequestFormatStartException, self).__init__(message)


class ResponseTypeException(Exception):

    def __init__(self, start_character):
        message = 'start with {} raise Response Type Error'.format(start_character)
        super(ResponseTypeException, self).__init__(message)


class OutOfIndexException(Exception):

    def __init__(self, current_index, current_size):
        message = 'try to visit {}, but current size is {}'.format(current_index, current_size)
        super(OutOfIndexException, self).__init__(message)
