# -*- coding=utf-8 -*-
"""
redis client
"""


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
