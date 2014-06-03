# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_commit_to_repository_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score m rci q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_commit_to_repository


def test_MaterialPackageWrangler_commit_to_repository_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'm rci q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_commit_to_repository