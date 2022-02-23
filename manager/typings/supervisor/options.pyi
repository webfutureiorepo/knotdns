"""
This type stub file was generated by pyright.
"""

import warnings

from supervisor.compat import ConfigParser

VERSION = ...
def normalize_path(v):
    ...

class Dummy:
    ...


class Options:
    stderr = ...
    stdout = ...
    exit = ...
    warnings = warnings
    uid = ...
    progname = ...
    configfile = ...
    schemadir = ...
    configroot = ...
    here = ...
    positional_args_allowed = ...
    def __init__(self, require_configfile=...) -> None:
        """Constructor.

        Params:
        require_configfile -- whether we should fail on no config file.
        """
        ...
    
    def default_configfile(self): # -> str | None:
        """Return the name of the found config file or print usage/exit."""
        ...
    
    def help(self, dummy): # -> None:
        """Print a long help message to stdout and exit(0).

        Occurrences of "%s" in are replaced by self.progname.
        """
        ...
    
    def usage(self, msg): # -> None:
        """Print a brief error message to stderr and exit(2)."""
        ...
    
    def add(self, name=..., confname=..., short=..., long=..., handler=..., default=..., required=..., flag=..., env=...): # -> None:
        """Add information about a configuration option.

        This can take several forms:

        add(name, confname)
            Configuration option 'confname' maps to attribute 'name'
        add(name, None, short, long)
            Command line option '-short' or '--long' maps to 'name'
        add(None, None, short, long, handler)
            Command line option calls handler
        add(name, None, short, long, handler)
            Assign handler return value to attribute 'name'

        In addition, one of the following keyword arguments may be given:

        default=...  -- if not None, the default value
        required=... -- if nonempty, an error message if no value provided
        flag=...     -- if not None, flag value for command line option
        env=...      -- if not None, name of environment variable that
                        overrides the configuration file or default
        """
        ...
    
    def realize(self, args=..., doc=..., progname=...): # -> None:
        """Realize a configuration.

        Optional arguments:

        args     -- the command line arguments, less the program name
                    (default is sys.argv[1:])

        doc      -- usage message (default is __main__.__doc__)
        """
        ...
    
    def process_config(self, do_usage=...): # -> None:
        """Process configuration data structure.

        This includes reading config file if necessary, setting defaults etc.
        """
        ...
    
    def process_config_file(self, do_usage): # -> None:
        ...
    
    def exists(self, path): # -> bool:
        ...
    
    def open(self, fn, mode=...): # -> TextIOWrapper:
        ...
    
    def get_plugins(self, parser, factory_key, section_prefix): # -> list[Unknown]:
        ...
    
    def import_spec(self, spec): # -> Any:
        ...
    


class ServerOptions(Options):
    user = ...
    sockchown = ...
    sockchmod = ...
    logfile = ...
    loglevel = ...
    pidfile = ...
    passwdfile = ...
    nodaemon = ...
    silent = ...
    httpservers = ...
    unlink_pidfile = ...
    unlink_socketfiles = ...
    mood = ...
    def __init__(self) -> None:
        ...
    
    def version(self, dummy): # -> None:
        """Print version to stdout and exit(0).
        """
        ...
    
    def getLogger(self, *args, **kwargs): # -> Logger:
        ...
    
    def default_configfile(self): # -> str | None:
        ...
    
    def realize(self, *arg, **kw): # -> None:
        ...
    
    def process_config(self, do_usage=...): # -> None:
        ...
    
    def read_config(self, fp):
        ...
    
    def process_groups_from_parser(self, parser): # -> list[Unknown]:
        ...
    
    def parse_fcgi_socket(self, sock, proc_uid, socket_owner, socket_mode, socket_backlog): # -> UnixStreamSocketConfig | InetStreamSocketConfig:
        ...
    
    def processes_from_section(self, parser, section, group_name, klass=...): # -> list[Unknown]:
        ...
    
    def server_configs_from_parser(self, parser): # -> list[Unknown]:
        ...
    
    def daemonize(self): # -> None:
        ...
    
    def write_pidfile(self): # -> None:
        ...
    
    def cleanup(self): # -> None:
        ...
    
    def close_httpservers(self): # -> None:
        ...
    
    def close_logger(self): # -> None:
        ...
    
    def setsignals(self): # -> None:
        ...
    
    def get_signal(self): # -> None:
        ...
    
    def openhttpservers(self, supervisord): # -> None:
        ...
    
    def get_autochildlog_name(self, name, identifier, channel):
        ...
    
    def clear_autochildlogdir(self): # -> None:
        ...
    
    def get_socket_map(self): # -> dict[Unknown, Unknown]:
        ...
    
    def cleanup_fds(self): # -> None:
        ...
    
    def kill(self, pid, signal): # -> None:
        ...
    
    def waitpid(self): # -> tuple[int | None, int | None]:
        ...
    
    def drop_privileges(self, user): # -> str | None:
        """Drop privileges to become the specified user, which may be a
        username or uid.  Called for supervisord startup and when spawning
        subprocesses.  Returns None on success or a string error message if
        privileges could not be dropped."""
        ...
    
    def set_uid_or_exit(self): # -> None:
        """Set the uid of the supervisord process.  Called during supervisord
        startup only.  No return value.  Exits the process via usage() if
        privileges could not be dropped."""
        ...
    
    def set_rlimits_or_exit(self): # -> None:
        """Set the rlimits of the supervisord process.  Called during
        supervisord startup only.  No return value.  Exits the process via
        usage() if any rlimits could not be set."""
        ...
    
    def make_logger(self): # -> None:
        ...
    
    def make_http_servers(self, supervisord): # -> list[Unknown]:
        ...
    
    def close_fd(self, fd): # -> None:
        ...
    
    def fork(self): # -> int:
        ...
    
    def dup2(self, frm, to): # -> None:
        ...
    
    def setpgrp(self): # -> None:
        ...
    
    def stat(self, filename): # -> stat_result:
        ...
    
    def write(self, fd, data): # -> int:
        ...
    
    def execve(self, filename, argv, env): # -> NoReturn:
        ...
    
    def mktempfile(self, suffix, prefix, dir):
        ...
    
    def remove(self, path): # -> None:
        ...
    
    def setumask(self, mask): # -> None:
        ...
    
    def get_path(self): # -> List[str]:
        """Return a list corresponding to $PATH, or a default."""
        ...
    
    def get_pid(self): # -> int:
        ...
    
    def check_execv_args(self, filename, argv, st): # -> None:
        ...
    
    def reopenlogs(self): # -> None:
        ...
    
    def readfd(self, fd): # -> bytes:
        ...
    
    def chdir(self, dir): # -> None:
        ...
    
    def make_pipes(self, stderr=...): # -> dict[str, None]:
        """ Create pipes for parent to child stdin/stdout/stderr
        communications.  Open fd in non-blocking mode so we can read them
        in the mainloop without blocking.  If stderr is False, don't
        create a pipe for stderr. """
        ...
    
    def close_parent_pipes(self, pipes): # -> None:
        ...
    
    def close_child_pipes(self, pipes): # -> None:
        ...
    


class ClientOptions(Options):
    positional_args_allowed = ...
    interactive = ...
    prompt = ...
    serverurl = ...
    username = ...
    password = ...
    history_file = ...
    def __init__(self) -> None:
        ...
    
    def realize(self, *arg, **kw): # -> None:
        ...
    
    def read_config(self, fp):
        ...
    
    def getServerProxy(self):
        ...
    


_marker = ...
class UnhosedConfigParser(ConfigParser.RawConfigParser):
    mysection = ...
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def read_string(self, string, source=...): # -> None:
        '''Parse configuration data from a string.  This is intended
        to be used in tests only.  We add this method for Py 2/3 compat.'''
        ...
    
    def read(self, filenames, **kwargs): # -> list[Unknown]:
        '''Attempt to read and parse a list of filenames, returning a list
        of filenames which were successfully parsed.  This is a method of
        RawConfigParser that is overridden to build self.section_to_file,
        which is a mapping of section names to the files they came from.
        '''
        ...
    
    def saneget(self, section, option, default=..., do_expand=..., expansions=...): # -> str:
        ...
    
    def getdefault(self, option, default=..., expansions=..., **kwargs): # -> str:
        ...
    
    def expand_here(self, here): # -> None:
        ...
    


class Config:
    def __ne__(self, other) -> bool:
        ...
    
    def __lt__(self, other) -> bool:
        ...
    
    def __le__(self, other) -> bool:
        ...
    
    def __gt__(self, other) -> bool:
        ...
    
    def __ge__(self, other) -> bool:
        ...
    
    def __repr__(self): # -> str:
        ...
    


class ProcessConfig(Config):
    req_param_names = ...
    optional_param_names = ...
    def __init__(self, options, **params) -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def get_path(self):
        '''Return a list corresponding to $PATH that is configured to be set
        in the process environment, or the system default.'''
        ...
    
    def create_autochildlogs(self): # -> None:
        ...
    
    def make_process(self, group=...): # -> Subprocess:
        ...
    
    def make_dispatchers(self, proc): # -> tuple[dict[Unknown, Unknown], Unknown]:
        ...
    


class EventListenerConfig(ProcessConfig):
    def make_dispatchers(self, proc): # -> tuple[dict[Unknown, Unknown], Unknown]:
        ...
    


class FastCGIProcessConfig(ProcessConfig):
    def make_process(self, group=...): # -> FastCGISubprocess:
        ...
    
    def make_dispatchers(self, proc): # -> tuple[dict[Unknown, Unknown], Unknown]:
        ...
    


class ProcessGroupConfig(Config):
    def __init__(self, options, name, priority, process_configs) -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def after_setuid(self): # -> None:
        ...
    
    def make_group(self): # -> ProcessGroup:
        ...
    


class EventListenerPoolConfig(Config):
    def __init__(self, options, name, priority, process_configs, buffer_size, pool_events, result_handler) -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def after_setuid(self): # -> None:
        ...
    
    def make_group(self): # -> EventListenerPool:
        ...
    


class FastCGIGroupConfig(ProcessGroupConfig):
    def __init__(self, options, name, priority, process_configs, socket_config) -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def make_group(self): # -> FastCGIProcessGroup:
        ...
    


def readFile(filename, offset, length): # -> bytes:
    """ Read length bytes from the file named by filename starting at
    offset """
    ...

def tailFile(filename, offset, length): # -> list[str | int | bool] | list[str | Unknown | bool]:
    """
    Read length bytes from the file named by filename starting at
    offset, automatically increasing offset and setting overflow
    flag if log size has grown beyond (offset + length).  If length
    bytes are not available, as many bytes as are available are returned.
    """
    ...

def decode_wait_status(sts): # -> tuple[int, str] | tuple[Literal[-1], Unknown | str] | tuple[Literal[-1], Unknown]:
    """Decode the status returned by wait() or waitpid().

    Return a tuple (exitstatus, message) where exitstatus is the exit
    status, or -1 if the process was killed by a signal; and message
    is a message telling what happened.  It is the caller's
    responsibility to display the message.
    """
    ...

_signames = ...
def signame(sig):
    """Return a symbolic name for a signal.

    Return "signal NNN" if there is no corresponding SIG name in the
    signal module.
    """
    ...

class SignalReceiver:
    def __init__(self) -> None:
        ...
    
    def receive(self, sig, frame): # -> None:
        ...
    
    def get_signal(self): # -> None:
        ...
    


def expand(s, expansions, name):
    ...

def make_namespec(group_name, process_name): # -> str:
    ...

def split_namespec(namespec): # -> tuple[Unknown, Unknown | None]:
    ...

class ProcessException(Exception):
    """ Specialized exceptions used when attempting to start a process """
    ...


class BadCommand(ProcessException):
    """ Indicates the command could not be parsed properly. """
    ...


class NotExecutable(ProcessException):
    """ Indicates that the filespec cannot be executed because its path
    resolves to a file which is not executable, or which is a directory. """
    ...


class NotFound(ProcessException):
    """ Indicates that the filespec cannot be executed because it could not
    be found """
    ...


class NoPermission(ProcessException):
    """ Indicates that the file cannot be executed because the supervisor
    process does not possess the appropriate UNIX filesystem permission
    to execute the file. """
    ...