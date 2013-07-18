from abjad import *


def test_TonalAnalysisSelection_are_stepwise_notes_01():
    '''Notes with the same pitch name are stepwise so long
    as pitch numbers differ.
    '''

    notes = [Note('c', (1, 4)), Note('cs', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_notes()


def test_TonalAnalysisSelection_are_stepwise_notes_02():
    '''Notes with the different pitch name are stepwise so long
    as they differ by exactly one staff space.
    '''

    notes = [Note('c', (1, 4)), Note('d', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_notes()

    notes = [Note('c', (1, 4)), Note('ds', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_notes()

    notes = [Note('c', (1, 4)), Note('b,', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_notes()

    notes = [Note('c', (1, 4)), Note('bf,', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_notes()


def test_TonalAnalysisSelection_are_stepwise_notes_03():
    '''Notes with the same pitch are not stepwise.
    '''

    notes = [Note('c', (1, 4)), Note('c', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert not selection.are_stepwise_notes()


def test_TonalAnalysisSelection_are_stepwise_notes_04():
    '''Notes separated by more than 1 staff space are not stepwise.
    '''

    notes = [Note('c', (1, 4)), Note('e', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert not selection.are_stepwise_notes()


def test_TonalAnalysisSelection_are_stepwise_notes_05():
    '''Contour changes in note sequence qualifies as tepwise.
    '''

    notes = notetools.make_notes([0, 2, 4, 5, 4, 2, 0], [(1, 4)])
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_notes()
