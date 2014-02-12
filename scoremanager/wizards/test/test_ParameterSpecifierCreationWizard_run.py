# -*- encoding: utf-8 -*-
from experimental import *


def test_ParameterSpecifierCreationWizard_run_01():

    wizard = scoremanager.wizards.ParameterSpecifierCreationWizard()
    wizard._run(pending_user_input='instrument instrument violin done')

    assert wizard.target == scoremanager.specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())
