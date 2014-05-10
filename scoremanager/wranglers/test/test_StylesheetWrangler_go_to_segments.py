# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_go_to_segments_01():
    r'''Goes from score stylesheets to score segments.
    '''

    input_ = 'red~example~score y g q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_segments_02():
    r'''Goes from stylesheets library to segments library.
    '''

    input_ = 'y g q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - stylesheets',
        'Score manager - segments',
        ]
    assert score_manager._transcript.titles == titles