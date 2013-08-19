# -*- encoding: utf-8 -*-
import abc
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class PitchClassSegment(TypedTuple):
    '''Pitch-class segment base class:

    ::

        >>> numbered_segment = pitchtools.PitchClassSegment(
        ...     tokens=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitchClass,
        ...     )
        >>> numbered_segment
        PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

    ::

        >>> named_segment = pitchtools.PitchClassSegment(
        ...     tokens=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=pitchtools.NamedPitchClass,
        ...     )
        >>> named_segment
        PitchClassSegment(['c', 'ef', 'bqs', 'd'])

    Return pitch-class segment.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [-2, -1.5, 6, 7, -1.5, 7],
        )

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        assert item_class in (
            None,
            pitchtools.NamedPitchClass,
            pitchtools.NumberedPitchClass,
            )
        if item_class is None:
            item_class = pitchtools.NumberedPitchClass
        TypedTuple.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._repr_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        from abjad.tools import pitchtools
        parts = []
        if self.item_class is pitchtools.NamedPitchClass:
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        return ', '.join(parts)

    @property
    def _repr_string(self):
        return self._format_string

    ### PUBLIC METHODS ###

    def alpha(self):
        r'''Morris alpha transform of pitch-class segment:

        ::

            >>> numbered_segment.alpha()
            PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

        Return pitch-class segment.
        '''
        from abjad.tools import mathtools
        numbers = []
        for pc in self:
            pc = abs(float(pc))
            is_integer = True
            if not mathtools.is_integer_equivalent_number(pc):
                is_integer = False
                fraction_part = pc - int(pc)
                pc = int(pc)
            if abs(pc) % 2 == 0:
                number = (abs(pc) + 1) % 12
            else:
                number = abs(pc) - 1
            if not is_integer:
                number += fraction_part
            else:
                number = int(number)
            numbers.append(number)
        return self.new(tokens=numbers)

    def invert(self):
        r'''Invert pitch-class segment:

        ::

            >>> numbered_segment.invert()
            PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

        Return pitch-class segment.
        '''
        tokens = (pc.invert() for pc in self)
        return self.new(tokens=tokens)

    def is_equivalent_under_transposition(self, expr):
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.namedpitch(self[0], 4))
        new_npcs = [x + difference for x in self]
        new_npc_seg = self.new(tokens=new_npcs)
        return arg == new_npc_seg

    def multiply(self, n):
        r'''Multiply pitch-class segment by `n`:

        ::

            >>> numbered_segment.multiply(5)
            PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

        Return pitch-class segment.
        '''
        from abjad.tools import pitchtools
        tokens = (pitchtools.NumberedPitchClass(pc).multiply(n)
            for pc in self)
        return self.new(tokens=tokens)

    def retrograde(self):
        r'''Retrograde of pitch-class segment:

        ::

            >>> numbered_segment.retrograde()
            PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

        Return pitch-class segment.
        '''
        return self.new(tokens=reversed(self))

    def rotate(self, n):
        r'''Rotate pitch-class segment:

        ::

            >>> numbered_segment.rotate(1)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

        Return numbered chromatic pitch-class segment.
        '''
        from abjad.tools import sequencetools
        tokens = sequencetools.rotate_sequence(self[:], n)
        return self.new(tokens=tokens)

    def transpose(self, n):
        r'''Transpose pitch-class segment:

        ::

            >>> numbered_segment.transpose(10)
            PitchClassSegment([8, 8.5, 4, 5, 8.5, 5])

        Return pitch-class segment.
        '''
        tokens = (pc.transpose(n) for pc in self)
        return self.new(tokens=tokens)

