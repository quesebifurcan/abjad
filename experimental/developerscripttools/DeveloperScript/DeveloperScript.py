from abjad.tools import abctools
from abjad.tools import stringtools
from abc import abstractmethod, abstractproperty
import argparse
import os


class DeveloperScript(abctools.AbjadObject):
    '''Abjad object-oriented model of a developer script:

    ::

        >>> from experimental.abjadbooktools import DeveloperScript

    ::

        >>> script = DeveloperScript()
        >>> script.program_name
        'developer'

    It can be used from the command line:

    ::

        $ ./DeveloperScript.py --help
        usage: developer [-h] [--version]

        A short description.

        optional arguments:
          -h, --help  show this help message and exit
          --version   show program's version number and exit

        A long description.

    ::

        $ ./DeveloperScript.py --version
        developer 1.0

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_argument_parser',)

    ### CLASS INITIALIZER ###

    def __init__(self):
        parser = self._argument_parser = argparse.ArgumentParser(
            description=self.short_description,
            epilog=self.long_description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=self.program_name,
            )
        parser.add_argument('--version', action='version',
            version='%(prog)s {}'.format(self.version))
        self._argument_parser = parser
        self.setup_argument_parser(parser)

    ### SPECIAL METHODS ###

    def __call__(self, args=None):
        if args is None:
            args = self.argument_parser.parse_args()
        else:
            if isinstance(args, str):
                args = args.split()
            elif not isinstance(args, (list, tuple)):
                raise ValueError
            args = self.argument_parser.parse_args(args)
        self.process_args(args)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def alias(self):
        '''The alias to use for the script, useful only if the script defines
        an abj-dev scripting group as well.
        '''
        return None

    @property
    def argument_parser(self):
        '''The script's instance of argparse.ArgumentParser.'''
        return self._argument_parser

    @property
    def formatted_help(self):
        return self._argument_parser.format_help()

    @property
    def formatted_usage(self):
        return self._argument_parser.format_usage()

    @property
    def formatted_version(self):
        return self._argument_parser.format_version()

    @abstractproperty
    def long_description(self):
        '''The long description, printed after arguments explanations.'''
        raise NotImplemented

    @property
    def program_name(self):
        '''The name of the script, callable from the command line.'''
        name = self._class_name[:self._class_name.rfind('Script')]
        return stringtools.uppercamelcase_to_space_delimited_lowercase(
            name).replace(' ', '-')

    @property
    def scripting_group(self):
        '''The script's scripting subcommand group.'''
        return None

    @abstractproperty
    def short_description(self):
        '''The short description of the script, printed before arguments explanations.

        Also used as a summary in other contexts.
        '''
        raise NotImplemented

    @abstractproperty
    def version(self):
        '''The version number of the script.'''
        raise NotImplemented

    ### PUBLIC METHODS ###

    @abstractmethod
    def process_args(self, args):
        pass

    @abstractmethod
    def setup_argument_parser(self):
        pass

