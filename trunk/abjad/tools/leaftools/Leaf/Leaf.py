# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.selectiontools import more
from abjad.tools.componenttools.Component import Component


class Leaf(Component):
    '''A note, rest, chord or skip.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    # TODO: see if _grace and _after_grace can be removed
    __slots__ = (
        '_after_grace', 
        '_grace', 
        '_leaf_index',
        '_lilypond_duration_multiplier', 
        '_written_duration',
        '_written_pitch_indication_is_nonsemantic',
        '_written_pitch_indication_is_at_sounding_pitch',
        'after_grace', 
        'grace',
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    def __init__(self, written_duration, lilypond_duration_multiplier=None):
        Component.__init__(self)
        self._lilypond_duration_multiplier = lilypond_duration_multiplier
        self._leaf_index = None
        self.written_duration = durationtools.Duration(written_duration)
        self.written_pitch_indication_is_nonsemantic = False
        self.written_pitch_indication_is_at_sounding_pitch = True

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments.

        Returns tuple.
        '''
        result = []
        result.append(self.written_duration)
        if self.lilypond_duration_multiplier is not None:
            result.append(self.lilypond_duration_multiplier)
        return tuple(result)

    def __repr__(self):
        '''Interpreter representation of leaf.

        Returns string.
        '''
        return '{}({!r})'.format(
            self._class_name, self._compact_representation)

    def __str__(self):
        '''String representation of leaf.

        Returns string.
        '''
        return self._compact_representation

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '({})'.format(self._formatted_duration)

    @property
    def _duration_in_seconds(self):
        from abjad.tools import contexttools
        tempo = self._get_effective_context_mark(contexttools.TempoMark)
        if tempo is not None and not tempo.is_imprecise:
            result = self._get_duration() / tempo.duration / tempo.units_per_minute * 60
            return durationtools.Duration(result)
        raise MissingTempoError

    @property
    def _format_pieces(self):
        return self.lilypond_format.split('\n')

    @property
    def _formatted_duration(self):
        duration_string = self.written_duration.lilypond_duration_string
        if self.lilypond_duration_multiplier is not None:
            return '{} * {}'.format(
                duration_string, self.lilypond_duration_multiplier)
        else:
            return duration_string

    @property
    def _multiplied_duration(self):
        if self.written_duration:
            if self.lilypond_duration_multiplier is not None:
                multiplied_duration = self.written_duration
                multiplied_duration *= self.lilypond_duration_multiplier
                return multiplied_duration
            else:
                return durationtools.Duration(self.written_duration)
        else:
            return None

    @property
    def _preprolated_duration(self):
        return self._multiplied_duration

    ### PRIVATE METHODS ###

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, '_override', None) is not None:
            self._override = copy.copy(leaf.override)
        if getattr(leaf, '_set', None) is not None:
            self._set = copy.copy(leaf.set)

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Component._copy_with_marks_but_without_children_or_spanners(self)
        for grace_container in self._get_grace_containers():
            new_grace_container = \
                grace_container._copy_with_children_and_marks_but_without_spanners()
            new_grace_container(new)
        return new

    def _format_after_slot(leaf, format_contributions):
        result = []
        result.append(('spanners', 
            format_contributions.get('after', {}).get('spanners', [])))
        result.append(('context marks', 
            format_contributions.get('after', {}).get('context marks', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'after', {}).get('lilypond command marks', [])))
        result.append(('comments', 
            format_contributions.get('after', {}).get('comments', [])))
        return result

    def _format_agrace_body(leaf):
        result = []
        if hasattr(leaf, '_after_grace'):
            after_grace = leaf.after_grace
            if len(after_grace):
                result.append(after_grace.lilypond_format)
        return ['agrace body', result]

    def _format_agrace_opening(leaf):
        result = []
        if hasattr(leaf, '_after_grace'):
            if len(leaf.after_grace):
                result.append(r'\afterGrace')
        return ['agrace opening', result]

    def _format_before_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_grace_body())
        result.append(('comments', 
            format_contributions.get('before', {}).get('comments', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'before', {}).get('lilypond command marks', [])))
        result.append(('context marks', 
            format_contributions.get('before', {}).get('context marks', [])))
        result.append(('grob overrides', 
            format_contributions.get('grob overrides', [])))
        result.append(('context settings', 
            format_contributions.get('context settings', [])))
        result.append(('spanners', 
            format_contributions.get('before', {}).get('spanners', [])))
        return result

    def _format_close_brackets_slot(leaf, format_contributions):
        return []

    def _format_closing_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_agrace_body())
        result.append(('spanners', 
            format_contributions.get('closing', {}).get('spanners', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'closing', {}).get('lilypond command marks', [])))
        result.append(('context marks', 
            format_contributions.get('closing', {}).get('context marks', [])))
        result.append(('comments', 
            format_contributions.get('closing', {}).get('comments', [])))
        return result

    def _format_contents_slot(leaf, format_contributions):
        result = []
        result.append(leaf._format_leaf_body(format_contributions))
        return result

    def _format_grace_body(leaf):
        result = []
        if hasattr(leaf, '_grace'):
            grace = leaf.grace
            if len(grace):
                result.append(grace.lilypond_format)
        return ['grace body', result]

    def _format_leaf_body(leaf, format_contributions):
        result = leaf._format_leaf_nucleus()[1]
        right = format_contributions.get('right', {})
        if right:
            result.extend(right.get('stem tremolos', []))
            result.extend(right.get('articulations', []))
            result.extend(right.get('lilypond command marks', []))
            result.extend(right.get('context marks', []))
            result.extend(right.get('spanners', []))
            result.extend(right.get('comments', []))
        result = [' '.join(result)]
        markup = right.get('markup')
        if markup:
            if len(markup) == 1:
                result[0] += ' {}'.format(markup[0])
            else:
                result.extend('\t{}'.format(x) for x in markup)
        return ['leaf body', result]

    # TODO: subclass this properly for chord
    def _format_leaf_nucleus(leaf):
        from abjad.tools.chordtools.Chord import Chord
        if not isinstance(leaf, Chord):
            return ['nucleus', leaf._body]
        result =  []
        chord = leaf
        note_heads = chord.note_heads
        if any('\n' in x.lilypond_format for x in note_heads):
            for note_head in note_heads:
                format = note_head.lilypond_format
                format_list = format.split('\n')
                format_list = ['\t' + x for x in format_list]
                result.extend(format_list)
            result.insert(0, '<')
            result.append('>')
            result = '\n'.join(result)
            result += str(chord._formatted_duration)
        else:
            result.extend([x.lilypond_format for x in note_heads])
            result = '<%s>%s' % (' '.join(result), chord._formatted_duration)
        # single string, but wrapped in list bc contribution
        return ['nucleus', [result]]

    def _format_open_brackets_slot(leaf, format_contributions):
        return []

    def _format_opening_slot(leaf, format_contributions):
        result = []
        result.append(('comments', 
            format_contributions.get('opening', {}).get('comments', [])))
        result.append(('context marks', 
            format_contributions.get('opening', {}).get('context marks', [])))
        result.append(('lilypond command marks',
            format_contributions.get(
                'opening', {}).get('lilypond command marks', [])))
        result.append(('spanners', 
            format_contributions.get('opening', {}).get('spanners', [])))
        result.append(leaf._format_agrace_opening())
        return result

    def _get_leaf_index(self):
        self._update_now(offsets=True)
        return self._leaf_index

    def _process_contribution_packet(self, contribution_packet):
        result = ''
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = '\t' + contributor[0] + ':\n'
                else:
                    contributor = '\t' + contributor + ':\n'
                result += contributor
                for contribution in contributions:
                    contribution = '\t\t' + contribution + '\n'
                    result += contribution
        return result

    def _select_tie_chain(self):
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        spanner_classes = (spannertools.TieSpanner,)
        for component in self._select_parentage():
            tie_spanners = component._get_spanners(spanner_classes)
            if len(tie_spanners) == 1:
                tie_spanner = tie_spanners.pop()
                return selectiontools.TieChain(music=tie_spanner.leaves)
            elif 1 < len(tie_spanners):
                raise ExtraSpannerError
        else:
            return selectiontools.TieChain(music=self)

    def _report_format_contributors(self):
        format_contributions = formattools.get_all_format_contributions(self)
        report = ''
        report += 'slot 1:\n'
        report += self._process_contribution_packet(
            self._format_before_slot(format_contributions))
        report += 'slot 3:\n'
        report += self._process_contribution_packet(
            self._format_opening_slot(format_contributions))
        report += 'slot 4:\n'
        report += '\tleaf body:\n'
        report += '\t\t' + self._format_contents_slot(
            format_contributions)[0][1][0] + '\n'
        report += 'slot 5:\n'
        report += self._process_contribution_packet(
            self._format_closing_slot(format_contributions))
        report += 'slot 7:\n'
        report += self._process_contribution_packet(
            self._format_after_slot(format_contributions))
        return report

    def _shorten(self, duration):
        from abjad.tools import leaftools
        duration = self._get_duration() - duration
        prolation = self._select_parentage().prolation
        preprolated_duration = duration / prolation
        leaftools.set_leaf_duration(self, preprolated_duration)

    # TODO: This should be replaced in favor of self._split_at_offsets().
    #       The precondition is that self._split_at_offsets() must be
    #       extended to handle graces.
    #       Also important to migrate over the (large-ish) set of tests for 
    #       this method.
    def _split_at_offset(
        self, 
        offset, 
        fracture_spanners=False,
        tie_split_notes=True, 
        tie_split_rests=False,
        ):
        from abjad.tools import contexttools
        from abjad.tools import leaftools
        from abjad.tools import marktools
        from abjad.tools import pitchtools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        # check input
        offset = durationtools.Offset(offset)
        # calculate durations
        leaf_multiplied_duration = self._multiplied_duration
        prolation = self._select_parentage(include_self=False).prolation
        preprolated_duration = offset / prolation
        # handle boundary cases
        if preprolated_duration <= 0:
            return ([], [self])
        if leaf_multiplied_duration <= preprolated_duration:
            return ([self], [])
        # create new leaf
        new_leaf = copy.copy(self)
        self._splice([new_leaf], grow_spanners=True)
        # adjust leaf
        self._detach_grace_containers(kind='after')
        # adjust new leaf
        new_leaf._detach_grace_containers(kind='grace')
        new_leaf.select().detach_marks()
        new_leaf.select().detach_marks(contexttools.ContextMark)
        left_leaf_list = \
            leaftools.set_leaf_duration(self, preprolated_duration)
        right_preprolated_duration = \
            leaf_multiplied_duration - preprolated_duration
        right_leaf_list = leaftools.set_leaf_duration(
            new_leaf, right_preprolated_duration)
        leaf_left_of_split = left_leaf_list[-1]
        leaf_right_of_split = right_leaf_list[0]
        leaves_around_split = (leaf_left_of_split, leaf_right_of_split)
        if fracture_spanners:
            spannertools.fracture_spanners_attached_to_component(
                leaf_left_of_split,
                direction=Right,
                )
        # tie split notes, rests and chords as specified
        if  (pitchtools.is_pitch_carrier(self) and tie_split_notes) or \
            (not pitchtools.is_pitch_carrier(self) and tie_split_rests):
            selection = selectiontools.ContiguousLeafSelection(
                leaves_around_split)
            selection._attach_tie_spanner_to_leaf_pair()
        return left_leaf_list, right_leaf_list
        # TODO: make this substitution work
        #return self._split_leaf_at_offsets(
        #    leaf, 
        #    [offset], 
        #    cyclic=False,
        #    fracture_spanners=fracture_spanners, 
        #    tie_split_notes=tie_split_notes,
        #    tie_split_rests=tie_split_rests,
        #    )

    def _split_at_offsets(
        self,
        offsets,
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=True,
        tie_split_rests=False,
        ):
        from abjad.tools import componenttools
        from abjad.tools import contexttools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import marktools
        from abjad.tools import pitchtools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        offsets = [durationtools.Offset(offset) for offset in offsets]
        if cyclic:
            offsets = sequencetools.repeat_sequence_to_weight_exactly(
                offsets, self._get_duration())
        durations = [durationtools.Duration(offset) for offset in offsets]
        if sum(durations) < self._get_duration():
            last_duration = self._get_duration() - sum(durations)
            durations.append(last_duration)
        sequencetools.truncate_sequence_to_weight(
            durations, self._get_duration())
        result = []
        leaf_prolation = self._select_parentage(include_self=False).prolation
        leaf_copy = copy.copy(self)
        for duration in durations:
            new_leaf = copy.copy(self)
            preprolated_duration = duration / leaf_prolation
            shard = leaftools.set_leaf_duration(
                new_leaf, preprolated_duration)
            shard = [x._select_parentage().root for x in shard]
            result.append(shard)
        flattened_result = sequencetools.flatten_sequence(result)
        flattened_result = selectiontools.SliceSelection(flattened_result)
        spanner_classes = (spannertools.TieSpanner,)
        if spannertools.get_spanners_attached_to_any_improper_parent_of_component(
            self, spanner_classes=spanner_classes):
            selection = selectiontools.select(flattened_result)
            selection.detach_spanners(spanner_classes=spanner_classes)
        componenttools.move_parentage_and_spanners_from_components_to_components(
            [self], flattened_result)
        if fracture_spanners:
            first_shard = result[0]
            spannertools.fracture_spanners_attached_to_component(
                first_shard[-1], direction=Right)
            last_shard = result[-1]
            spannertools.fracture_spanners_attached_to_component(
                last_shard[0], direction=Left)
            for middle_shard in result[1:-1]:
                spannertools.fracture_spanners_attached_to_component(
                    middle_shard[0], direction=Left)
                spannertools.fracture_spanners_attached_to_component(
                    middle_shard[-1], direction=Right)
        # adjust first leaf
        first_leaf = flattened_result[0]
        self._detach_grace_containers(kind='after')
        # adjust any middle leaves
        for middle_leaf in flattened_result[1:-1]:
            middle_leaf._detach_grace_containers(kind='grace')
            self._detach_grace_containers(kind='after')
            middle_leaf.select().detach_marks()
            middle_leaf.select().detach_marks(contexttools.ContextMark)
        # adjust last leaf
        last_leaf = flattened_result[-1]
        last_leaf._detach_grace_containers(kind='grace')
        last_leaf.select().detach_marks()
        last_leaf.select().detach_marks(contexttools.ContextMark)
        # tie split notes, rests and chords as specified
        if  (pitchtools.is_pitch_carrier(self) and tie_split_notes) or \
            (not pitchtools.is_pitch_carrier(self) and tie_split_rests):
            flattened_result_leaves = iterationtools.iterate_leaves_in_expr(
                flattened_result)
            # TODO: implement SliceSelection._attach_tie_spanner_to_leaves()
            for leaf_pair in sequencetools.iterate_sequence_pairwise_strict(
                flattened_result_leaves):
                selection = selectiontools.ContiguousLeafSelection(leaf_pair)
                selection._attach_tie_spanner_to_leaf_pair()
        # return result
        return result

    def _split_in_halves(self, n=2):
        from abjad.tools import leaftools
        from abjad.tools import componenttools
        assert mathtools.is_nonnegative_integer_power_of_two(n)
        assert 0 < n
        new_leaves = (n - 1) * self
        self._splice(new_leaves, grow_spanners=True)
        adjustment_multiplier = durationtools.Duration(1, n)
        self.written_duration *= adjustment_multiplier
        for new_leaf in new_leaves:
            new_leaf.written_duration *= adjustment_multiplier
            
    def _to_tuplet_with_ratio(self, proportions, is_diminution=True):
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        from abjad.tools import notetools
        from abjad.tools import selectiontools
        from abjad.tools import tuplettools
        # check input
        proportions = mathtools.Ratio(proportions)
        # find target duration of fixed-duration tuplet
        target_duration = self.written_duration
        # find basic prolated duration of note in tuplet
        basic_prolated_duration = target_duration / sum(proportions)
        # find basic written duration of note in tuplet
        basic_written_duration = \
            basic_prolated_duration.equal_or_greater_assignable
        # find written duration of each note in tuplet
        written_durations = [x * basic_written_duration for x in proportions]
        # make tuplet notes
        try:
            notes = [notetools.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [durationtools.Duration(x, denominator) 
                for x in proportions]
            notes = notetools.make_notes(0, note_durations)
        # make tuplet
        tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)
        # fix tuplet contents if necessary
        tuplet._fix()
        # change prolation if necessary
        if not tuplet.multiplier == 1:
            if is_diminution:
                if not tuplet.is_diminution:
                    tuplet._diminished_to_augmented()
            else:
                if tuplet.is_diminution:
                    tuplet._diminished_to_augmented()
        # give leaf position in score structure to tuplet
        componenttools.move_parentage_and_spanners_from_components_to_components(
            [self], [tuplet])
        # return tuplet
        return tuplet

    ### PUBLIC PROPERTIES ###

    @apply
    def lilypond_duration_multiplier():
        def fget(self):
            '''LilyPond duration multiplier.

            Set to positive multiplier or none.

            ..  note:: Attribute will migrate to ``Duration`` in Abjad 2.14.

            Returns positive multiplier or none.
            '''
            return self._lilypond_duration_multiplier
        def fset(self, expr):
            if expr is None:
                self._lilypond_duration_multiplier = None
            else:
                lilypond_duration_multiplier = durationtools.Multiplier(expr)
                assert 0 <= lilypond_duration_multiplier
                self._lilypond_duration_multiplier = lilypond_duration_multiplier
        return property(**locals())

    @apply
    def written_duration():
        def fget(self):
            '''Written duration of leaf.

            Set to duration.

            Returns duration.
            '''
            return self._written_duration
        def fset(self, expr):
            rational = durationtools.Duration(expr)
            if not rational.is_assignable:
                message = 'not assignable duration: {!r}.'
                raise AssignabilityError(message.format(rational))
            self._written_duration = rational
        return property(**locals())

    @apply
    def written_pitch_indication_is_at_sounding_pitch():
        def fget(self):
            r'''Returns true when written pitch is at sounding pitch.
            Returns false when written pitch is transposed.
            '''
            return self._written_pitch_indication_is_at_sounding_pitch
        def fset(self, expr):
            if not isinstance(expr, bool):
                raise TypeError
            self._written_pitch_indication_is_at_sounding_pitch = expr
        return property(**locals())

    @apply
    def written_pitch_indication_is_nonsemantic():
        def fget(self):
            r'''Returns true when pitch is nonsemantic.
            Returns false otherwise.

            Set to true when using leaves only graphically.

            Setting this value to true sets sounding pitch indicator to false.
            '''
            return self._written_pitch_indication_is_nonsemantic
        def fset(self, expr):
            if not isinstance(expr, bool):
                raise TypeError
            self._written_pitch_indication_is_nonsemantic = expr
            if expr == True:
                self.written_pitch_indication_is_at_sounding_pitch = False
        return property(**locals())
