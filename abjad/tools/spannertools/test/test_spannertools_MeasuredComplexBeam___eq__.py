# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_MeasuredComplexBeam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.MeasuredComplexBeam()
    spanner_2 = spannertools.MeasuredComplexBeam()

    assert not spanner_1 == spanner_2