# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# ok to have is_test=True to test view rename
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_rename_view_01():

    input_ = 'g vnew _test_100 rm all'
    input_ += ' add segment~01~(Red~Example~Score) done default q' 
    score_manager._run(pending_user_input=input_)
        
    input_ = 'g vls q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' in contents
    assert '_test_101' not in contents

    input_ = 'g vren _test_100 _test_101 default q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    input_ = 'g vls q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' not in contents
    assert '_test_101' in contents

    input_ = 'g vrm _test_101 default q'
    score_manager._run(pending_user_input=input_)

    input_ = 'g vls q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_101' not in contents