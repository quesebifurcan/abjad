# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_open_every_metadata_py_01():

    input_ = 'mdo* y q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file