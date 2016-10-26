# -*- coding=utf-8 -*-
"""
redis server
"""
from resp_exceptions import ProtocolArgLengthException, RequestFormatStartException, ProtocolArgsNumberException


class ServerSide(object):

    @staticmethod
    def get_request(request_for_mat_str):
        """
        将格式化后的request format转换为命令
        :param request_for_mat_str: request format str from client
        :return: list of command args list
        """
        request_splits = request_for_mat_str.split('\r\n')
        commands = []
        if not request_splits:
            return commands
        index_ = 0
        current_command, current_command_length = None, 0
        while index_ < len(request_splits):
            if not request_splits[index_].startswith('*'):
                raise RequestFormatStartException()
            if request_splits[index_].startswith('*'):
                if current_command:
                    commands.append(current_command)
                current_command = []
                current_command_length = int(request_splits[index_][1:])
                if index_ + current_command_length * 2 + 1 >= len(request_splits):
                    raise ProtocolArgsNumberException()
                for i in xrange(current_command_length):
                    index_ += 1
                    current_arg_size = int(request_splits[index_][1:])
                    index_ += 1
                    if len(request_splits[index_]) != current_arg_size:
                        raise ProtocolArgLengthException(len(request_splits[index_]), current_arg_size)
                    current_command.append(request_splits[index_])
        return commands

