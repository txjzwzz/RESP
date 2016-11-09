# -*- coding=utf-8 -*-
"""
redis client
"""
import socket
from resp_exceptions import ResponseTypeException, ProtocolArgLengthException, TimeoutError, ConnectionError
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


# from redis-py
def b(x):
    return x.encode('latin-1') if not isinstance(x, bytes) else x


# from redis-py
def encode(value):
    "Return a bytestring representation of the value"
    if isinstance(value, bytes):
        return value
    elif isinstance(value, (int, long)):
        value = b(str(value))
    elif isinstance(value, float):
        value = b(repr(value))
    elif not isinstance(value, basestring):
        value = unicode(value)
    if isinstance(value, unicode):
        value = value.encode('utf-8')
    return value


class RedisClient(object):

    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port

    def send_command(self, *arguments):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))
        except socket.error as msg:
            print str(msg)
            s.close()
            return
        s.sendall(RedisClient.request_format(*arguments))
        data = list()
        # read from socket code from redis-py in github
        try:
            while True:
                data_str = s.recv(1024)
                if isinstance(data_str, bytes) and len(data_str) == 0:
                    raise socket.error("Server Closed Connection")
                data.append(data_str)
                if len(data_str) < 1024:
                    break
        except socket.timeout:
            raise TimeoutError()
        except socket.error as msg:
            raise ConnectionError("Error while reading from socket {}".format(msg))
        finally:
            s.close()
            data = ''.join(data)
            return RedisClient.resolve_response(data)

    @staticmethod
    def request_format(*arguments):
        """
        transfer to request style
        :param arguments:
        :return: request format
        """
        request_format = ""
        count = 0
        for argument in map(encode, arguments):
            request_format += '${}\r\n'.format(len(argument))
            request_format += '{}\r\n'.format(argument)
            count += 1
        request_format = '*{}\r\n'.format(count) + request_format
        return request_format.encode('utf-8')

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
    # print RedisClient.request_format('set', 'hello', 'word')
    # print RedisClient.resolve_response(':123\r\n')
    # print RedisClient.resolve_response('$6\r\nfoobar\r\n')
    # print RedisClient.resolve_response('*3\r\n$3\r\nfoo\r\n$-1\r\n$3\r\nbar\r\n')
    rc = RedisClient()
    print rc.send_command('set', 'a', 'a1')
    print rc.send_command('del', 'a')
    print rc.send_command('sadd', 'a-set', 'a', 'b', 'c', 'd')
    rc.send_command('sadd', 'a-set', *[i for i in xrange(1024)])
    print rc.send_command('smembers', 'a-set')
    print rc.send_command('smembers', 'b-set')
    print rc.send_command('del', 'a-set')
