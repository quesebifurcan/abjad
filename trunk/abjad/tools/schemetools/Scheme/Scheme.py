from abjad.tools.abctools import AbjadObject


class Scheme(AbjadObject):
    r'''Abjad model of Scheme code:

    ::

        >>> scheme = schemetools.Scheme(True)
        >>> scheme.lilypond_format
        '##t'

    schemetools.Scheme can represent nested structures:

    ::

        >>> scheme = schemetools.Scheme(
        ...     ('left', (1, 2, False)), ('right', (1, 2, 3.3)))
        >>> scheme.lilypond_format
        '#((left (1 2 #f)) (right (1 2 3.3)))'

    schemetools.Scheme wraps variable-length arguments into a tuple:

    ::

        >>> scheme_1 = schemetools.Scheme(1, 2, 3)
        >>> scheme_2 = schemetools.Scheme((1, 2, 3))
        >>> scheme_1.lilypond_format == scheme_2.lilypond_format
        True

    schemetools.Scheme also takes an optional `quoting` keyword, 
    by which Scheme's various quote, unquote, unquote-splicing characters 
    can be prepended to the formatted result:

    ::

        >>> scheme = schemetools.Scheme((1, 2, 3), quoting="'#")
        >>> scheme.lilypond_format
        "#'#(1 2 3)"

    Scheme can also force quotes around strings which contain no whitespace:

    ::

        >>> scheme = schemetools.Scheme('nospaces', force_quotes=True)
        >>> f(scheme)
        #"nospaces"

    The above is useful in certain \override situations, 
    as LilyPond's Scheme interpreter
    will treat unquoted strings as symbols rather than strings.

    Scheme is immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_force_quotes', 
        '_quoting', 
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        if 1 == len(args):
            if isinstance(args[0], type(self)):
                args = args[0]._value
            else:
                args = args[0]
        quoting = kwargs.get('quoting')
        force_quotes = bool(kwargs.get('force_quotes'))
        assert isinstance(quoting, (str, type(None)))
        if quoting is not None:
            assert all(x in ("'", ',', '@', '`', '#') for x in quoting)
        self._force_quotes = force_quotes
        self._quoting = quoting
        self._value = args

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self._value == expr._value:
                return True
        return False

    def __getnewargs__(self):
        return (self._value,)

    def __repr__(self):
        return "%s(%r)" % (self._class_name, self._value)

    def __str__(self):
        if self._quoting is not None:
            return self._quoting + self._formatted_value
        return self._formatted_value

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        from abjad.tools import schemetools
        return schemetools.format_scheme_value(
            self._value, force_quotes=self.force_quotes)

    ### PUBLIC PROPERTIES ###

    @property
    def force_quotes(self):
        return self._force_quotes

    @property
    def lilypond_format(self):
        '''Hash-mark-prepended format of Scheme:

        ::

            >>> scheme = schemetools.Scheme(True)
            >>> scheme.lilypond_format
            '##t'

        Returns string.
        '''
        if self._quoting is not None:
            return '#' + self._quoting + self._formatted_value
        return '#%s' % self._formatted_value
