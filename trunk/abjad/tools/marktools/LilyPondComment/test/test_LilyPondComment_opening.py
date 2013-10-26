# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_opening_01():
    r'''Opening comments in container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    comment = marktools.LilyPondComment('Voice opening comments here.', 'opening')
    comment.attach(voice)
    comment = marktools.LilyPondComment('More voice opening comments.', 'opening')
    comment.attach(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            % Voice opening comments here.
            % More voice opening comments.
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_LilyPondComment_opening_02():
    r'''Opening comments on leaf.
    '''

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Leaf opening comments here.', 'opening')
    comment.attach(note)
    comment = marktools.LilyPondComment('More leaf opening comments.', 'opening')
    comment.attach(note)

    assert testtools.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        % Leaf opening comments here.
        % More leaf opening comments.
        c'8
        '''
        )

    assert inspect(note).is_well_formed()
