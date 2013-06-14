import os
import subprocess
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.core.ScoreManagerObject.ScoreManagerObject import \
    ScoreManagerObject
from experimental.tools.scoremanagertools import predicates


class MenuObject(ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, session=None, where=None, title=None):
        ScoreManagerObject.__init__(self, session=session)
        self.indent_level = 0
        self.title = title
        self.where = where

    ### PRIVATE METHODS ###

    def _make_tab(self, n):
        return 4 * n * ' '

    ### PUBLIC PROPERTIES ###

    @apply
    def title():
        def fget(self):
            return self._title
        def fset(self, title):
            assert isinstance(title, (str, list, type(None)))
            self._title = title
        return property(**locals())

    ### PUBLIC METHODS ###

    def make_title_lines(self):
        menu_lines = []
        if isinstance(self.title, str):
            title_lines = [stringtools.capitalize_string_start(self.title)]
        elif isinstance(self.title, list):
            title_lines = self.title
        else:
            title_lines = []
        for title_line in title_lines:
            if self.indent_level:
                line = '{} {}'.format(
                    self._make_tab(self.indent_level), title_line)
                menu_lines.append(line)
            else:
                menu_lines.append(title_line)
        if menu_lines:
            menu_lines.append('')
        return menu_lines
