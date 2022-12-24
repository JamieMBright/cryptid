"""
Logging decorator.

The logging decorator is a way to inoffensively log all function calls and
general information on the info level without having lots of code.
"""
from datetime import datetime
from functools import wraps
import logging
import os
import socket
import sys
from types import ModuleType
from typing import List
from operator import attrgetter
import __main__

# Don't be tempted to import from tools. Tools uses log, so a circular import
# will occur. Instead, may need to have duplicate code if wish to use check_type
# from ukpnutils.tools import check_type


def check_type(var, varname: str, vartype) -> None:
    """
    Check the type of a variable against it's intended type.

    This variable takes var and checks it against var type using the isinstance
    technique, it then produces a standardised error message in the outcome
    that the variable is not the correct variable.

    Parameters
    ----------
    var : any type
        An instance of the variable you wish to check
    varname : str
        A string that is the __name__ of the variable.
    vartype : any type
        An instance of the type of variable you expect var to be.

    Returns
    -------
    None

    Example
    -------
    import numpy as np
    a = "not a numpy array"
    check_type(a, "a", str) --> nothing happens
    check_type(a, "a", np.ndarray) --> raises Type Error
    """
    # check inputs
    if not isinstance(varname, str):
        raise TypeError(
            f"Input variable '{varname}' should be of type str is in fact of type: {type(varname)}")

    # perform the check on the requested variable and vartype
    if not isinstance(var, vartype):
        raise TypeError(
            f"Input variable '{varname}' should be of type {vartype} is in fact of type: {type(var)}")
    return None


def build_logger(logging_level: int = logging.DEBUG,
                 config: ModuleType = None,
                 config_params: List[str] = []):
    """
    Build the logger for any 'python run_*.py' script.

    A logger should be made per run_*.py file in the following tree:

        /logs/
          L run_*/ a.k.a parent name
                  L yyyymmdd/
                        L   runtime-yyyymmdd-HHMM.log


    Parameters
    ----------
        logging_level : int,
            The logging level for the logger. Note the best practise way of
            setting this is to use the logger.<LEVEL> properties for accuracy.
            The options are: logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, logging.CRITICAL.

        config : ModuleType,
            This is a config module that contains properties. The config is
            used purely to add configuration information at the beginning of
            the log. E.g. ,if config.KEY_PROPERTY=1, then at the start of the
            log, it would print this information.

        config_params : List[str],
            The keys to query the config. the config file will be queried like:
                for key in config_params:
                    logger.info(getattr(config, key))

    Returns
    -------
        logger : logging.Logger,
            The logger that has been created using this method. Note that the
            logger can be accessed with the logging.getlogger(__name__) method
            also. This should point to the outcome of this funciton should the
            __name__ property by a run_*.py script.

    Raises
    ------
        TypeError,
            If the input parameters are not adhering to the typehints.

        ValueError,
            For unrecognised logging levels.

        NameError,
            Should a key inside config_params not be a property inside of the
            config module.

    Example
    -------
    from ukpnutils.loggingdecorator import build_logger
    from my_package import my_configuration_module as config
    import logging

    build_logger(
        logging_level=logging.ERROR,
        config=config,
        config_params=['MODE', 'INTERVALS', 'HORIZON', 'LEAD_TIME', 'UPDATE_FREQ', 'REPROCESS_EXISTING_FORECASTS', 'MULTIPROCESS_MODE', 'MAX_WORKERS', 'PLOTTING'])
    logger = logging.getLogger(__name__)

    """
    # checks
    check_type(logging_level, "logging_level", int)
    permissible_log_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    if logging_level not in permissible_log_levels:
        raise ValueError(f"Unrecognised logging_level. Received {logging_level} but the permissible options are {permissible_log_levels}.")
    if config is not None:
        check_type(config, "config", ModuleType)
    check_type(config_params, "config_params", list)
    for elem in config_params:
        check_type(elem, "elem", str)
        if not hasattr(config, elem):
            raise NameError(f"The module 'config' has no property {elem}. config has properties {dir(config)}.")

    # get the parent name of the file. E.g., run_realtime. If this is being run
    # in an interactive console, there will be no __main__ object, and so this
    # will revert to 'console_run'.
    try:
        parent_name = __main__.__file__.rsplit(os.sep, 1)[1].split(".")[0]
    except BaseException:
        parent_name = 'console_run'

    # get the times of the current run.
    runtime = datetime.strftime(datetime.now(), "%Y%m%d-%H%M")
    date = datetime.strftime(datetime.now(), "%Y%m%d")
    # build the
    dir_path = os.path.join(os.getcwd(), "logs", parent_name, date)
    # check that it exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # specify the name of the file.
    log_name = f"runtime-{runtime}.log"
    # build the fullpath
    full_path = os.path.join(dir_path, log_name)

    # initialize the logger, but use debug to start. We use user spec later.
    logging.basicConfig(filename=full_path,
                        filemode="w",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging_level)

    logger = logging.getLogger(__name__)
    # add a formatter handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # write some opening text into the logger that details the core information.
    # note that it is not straight forward to write directly into the log file
    # without passing in that info as an error format. However, if we write in
    # the file with the logger.INFO level, but the user requests a higher level
    # then we would not see this below information. To get aronud this, we
    # always add this information at the logging_level requested. The downside
    # is that, if in logging.ERROR level, then the opening text will appear as
    # an error.
    logger.log(logging_level, "---------------------------------------------------------------------------------------------------------")
    logger.log(logging_level, f"FILE: {parent_name.upper()} HAS BEEN TRIGGERED on hostname: {socket.gethostname()}.")
    logger.log(logging_level, f"LOG LOCATION: {full_path}")
    if config:
        f = attrgetter(*tuple(config_params))
        vals = f(config)
        msg_elems = [config_params[i].lower() + "=" + str(vals[i]) for i in range(len(config_params))]
        # msg = ",\n".join(msg_elems)
        for elem in msg_elems:
            logger.log(logging_level, elem)
    logger.log(logging_level, "---------------------------------------------------------------------------------------------------------")

    return logger


def log(func):
    """
    Decorate a function with The Log Decorator.

    This is the logging decorator, used simply by putting @log in the line
    before any function definition.

    The logging decorator takes all the inputs of a function, records this
    information using the logging module, and keeps rich detail about the in
    and out of each decorated function call.

    The logger will then execute the function inside a try except block, which
    will then log any exceptions as unexpected. This encourages the user to
    manage their own exceptions inside the decorated function. The working
    principle is that any leaked exceptions are unexpected errors and will be
    re-raised once the result is stored.

    Parameters
    ----------
        func : function object
            The function being decorated.

    Returns
    -------
        _ : _
            The output of the decorated function.

    Example
    -------
    import logging
    from ukpnutils.loggingdecorator import log
    logger = logging.getLogger(__name__)

    @log
    def my_decorataed_function():
        print("This function is executed inside the logging decorator.")
    """
    logger = logging.getLogger(__name__)

    def decorator_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(f"function {func.__name__} called with args: {args} and kwargs: {kwargs}")
            except BaseException:
                logger.exception(f"failed to report on function inputs: {func.__name__} called with arg: {args}, and kwargs: {kwargs} ")

            try:
                # call the function inside the safety of the try except
                result = func(*args, **kwargs)
                # perform any analysis on the outputs from the function call
                logger.debug(f"function {func.__name__} exited with result: {result}")
                return result

            except BaseException:
                logger.exception(f"function {func.__name__} called with args: {args} and kwargs: {kwargs}")
                print(f"Fuck. Something went wrong inside {func.__name__}.")
                raise
                return None
        return wrapper
    return decorator_log(func)
