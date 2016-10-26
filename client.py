# -*- coding=utf-8 -*-
"""
redis client
"""
from resp_exceptions import ResponseTypeException, ProtocolArgLengthException
from resp_buffer import ResponseBuffer


def phrase_response(response_buffer):
    """
    处理回复
    :param response_buffer: ResponseBuffer对象
    :return: res list
    """
    res_str = response_buffer.read_buffer()
    start_str = res_str[0]
    if start_str == '+' or start_str == '-':
        return [res_str[1:]]
    elif start_str == ':':
        return [long(res_str[1:])]
    elif start_str == '$':
        arg_length = long(res_str[1:])
        if arg_length == -1:
            return None
        elif arg_length == 0:
            return []
        true_res_str = response_buffer.read_buffer()
        if len(true_res_str) != arg_length:
            raise ProtocolArgLengthException(len(true_res_str), arg_length)
        return [true_res_str]
    elif start_str == '*':
        response_size = long(res_str[1:])
        if response_size == 0:
            return []
        if response_size == -1:
            return None
        res = []
        for index_ in xrange(response_size):
            current_res = phrase_response(response_buffer)
            res = res + current_res if current_res is not None else res + [current_res]
        return res
    else:
        raise ResponseTypeException(start_str)


class RedisClient(object):

    @staticmethod
    def request_format(*arguments):
        """
        transfer to request style
        :param arguments:
        :return: request format
        """
        request_format = ""
        count = 0
        for argument in arguments:
            request_format += '${}\r\n'.format(len(argument))
            request_format += '{}\r\n'.format(argument)
            count += 1
        request_format = '*{}\r\n'.format(count) + request_format
        return request_format

    @staticmethod
    def resolve_response(response_str):
        """
        解析response
        :param response_str: 回复的字符串
        :return: res list
        """
        if not response_str:
            return None
        response_buffer = ResponseBuffer(response_str)
        return phrase_response(response_buffer)


if __name__ == '__main__':
    print RedisClient.request_format('set', 'hello', 'word')
    print RedisClient.resolve_response(':123\r\n')
    print RedisClient.resolve_response('$6\r\nfoobar\r\n')
    print RedisClient.resolve_response('*3\r\n$3\r\nfoo\r\n$-1\r\n$3\r\nbar\r\n')
