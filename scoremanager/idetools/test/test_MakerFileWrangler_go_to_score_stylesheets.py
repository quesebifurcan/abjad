# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_score_stylesheets_01():
    r'''Goes from score maker files to score stylesheets.
    '''

    input_ = 'red~example~score k y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Red Example Score (2013) - stylesheets',
        ]
    assert ide._transcript.titles == titles