# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_library_01():
    r'''From score stylesheets to library.
    '''

    input_ = 'red~example~score y ** q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Abjad IDE',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_library_02():
    r'''From all stylesheets to library.
    '''

    input_ = 'Y ** q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE',
        ]
    assert score_manager._transcript.titles == titles