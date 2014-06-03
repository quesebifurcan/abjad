# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_BuildFileWrangler_repository_status_01():
    r'''Works with distribution file library.
    '''

    input_ = 'u rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents
    assert score_manager._session.proceed_count == 0


def test_BuildFileWrangler_repository_status_02():
    r'''Works with Git-managed score.
    '''

    input_ = 'red~example~score u rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents
    assert score_manager._session.proceed_count == 0


def test_BuildFileWrangler_repository_status_03():
    r'''Works with Subversion-managed score.
    '''

    score_name = score_manager._score_package_wrangler._find_svn_score_name()
    if not score_name:
        return

    input_ = '{} u rst q'.format(score_name)
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_repository_status
    assert score_manager._session.proceed_count == 0