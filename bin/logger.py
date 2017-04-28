#! /usr/bin/env python
import datetime

DEBUG = 3
"""The debug trace level"""
INFO = 2
"""The normal trace level"""
WARNING = 1
"""The warning trace level"""
ERROR = 0
"""The error trace level"""
__trace_names = {
    DEBUG: "DBUG",
    INFO: "INFO",
    WARNING: "WARN",
    ERROR: "CRIT"
}

class Logger:
        @property
        def trace_level(self):
            return self.__trace_lvl
        
        @trace_level.setter
        def trace_level(self, value):
            assert isinstance(value, int)
            self.__trace_lvl = value
        
        @property
        def log_format(self):
            """The format of each write to the log,
            including the current trace level and current time of the log."""
            return self.__log_fmt
        
        @log_format.setter
        def log_format(self, value):
            assert isinstance(value, str)
            self.__log_fmt = value

        def __init__(self, log_path):
            self.__trace_lvl = INFO
            self.__log_fmt = "[{0}][{1:yyyy-MM-dd}][{1:HH:mm:ss] {2}"
            self.__out_file = open(log_path, mode='a')
        
        def __check_level(self, required):
            if required >= self.trace_level:
                return True
            return False

        def __write_log(self, level, line, *args):
            if not self.__check_level(level):
                return
            to_write = ""
            if len(args) == 0:
                to_write = line
            else:
                to_write = line.format(args)
            self.__out_file.write(self.log_format.format(__trace_names[level], datetime.datetime.now(), to_write) + "\n")
 
        def logd(self, line, *args):
            self.__write_log(DEBUG, line, args)
        
        def log(self, line, *args):
            self.__write_log(INFO, line, args)
        
        def logw(self, line, *args):
            self.__write_log(WARNING, line, args)
        
        def loge(self, exception, msg="An exception occured, please talk to developer"):
            self.__write_log(ERROR, "{1}\n{2}", msg, exception)
        
        def cleanup(self, parameter_list):
            self.__out_file.close()