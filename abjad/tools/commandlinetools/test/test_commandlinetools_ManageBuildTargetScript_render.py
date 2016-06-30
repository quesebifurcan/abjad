# -*- coding: utf-8 -*-
from __future__ import print_function
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    def test_success_all(self):
        expected_files = [
            'test_score/test_score/build/.gitignore',
            'test_score/test_score/build/assets/.gitignore',
            'test_score/test_score/build/assets/instrumentation.tex',
            'test_score/test_score/build/assets/performance-notes.tex',
            'test_score/test_score/build/letter-portrait/back-cover.pdf',
            'test_score/test_score/build/letter-portrait/back-cover.tex',
            'test_score/test_score/build/letter-portrait/front-cover.pdf',
            'test_score/test_score/build/letter-portrait/front-cover.tex',
            'test_score/test_score/build/letter-portrait/music.ly',
            'test_score/test_score/build/letter-portrait/music.pdf',
            'test_score/test_score/build/letter-portrait/parts.ly',
            'test_score/test_score/build/letter-portrait/preface.pdf',
            'test_score/test_score/build/letter-portrait/preface.tex',
            'test_score/test_score/build/letter-portrait/score.pdf',
            'test_score/test_score/build/letter-portrait/score.tex',
            'test_score/test_score/build/parts.ily',
            'test_score/test_score/build/segments.ily',
            'test_score/test_score/build/segments/.gitignore',
            'test_score/test_score/build/segments/test-segment.ily',
            ]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--render', 'letter-portrait']
        #with systemtools.RedirectedStreams(stdout=self.string_io):
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(self.build_path, expected_files)

    def test_success_back_cover(self):
        expected_files = [
            'test_score/test_score/build/letter-portrait/back-cover.pdf',
            'test_score/test_score/build/letter-portrait/back-cover.tex',
            'test_score/test_score/build/letter-portrait/front-cover.tex',
            'test_score/test_score/build/letter-portrait/music.ly',
            'test_score/test_score/build/letter-portrait/parts.ly',
            'test_score/test_score/build/letter-portrait/preface.tex',
            'test_score/test_score/build/letter-portrait/score.tex',
            ]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--back-cover',
            ]
        #with systemtools.RedirectedStreams(stdout=self.string_io):
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)

    def test_success_front_cover(self):
        expected_files = [
            'test_score/test_score/build/letter-portrait/back-cover.tex',
            'test_score/test_score/build/letter-portrait/front-cover.pdf',
            'test_score/test_score/build/letter-portrait/front-cover.tex',
            'test_score/test_score/build/letter-portrait/music.ly',
            'test_score/test_score/build/letter-portrait/parts.ly',
            'test_score/test_score/build/letter-portrait/preface.tex',
            'test_score/test_score/build/letter-portrait/score.tex',
            ]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--front-cover',
            ]
        #with systemtools.RedirectedStreams(stdout=self.string_io):
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)

    def test_success_preface(self):
        expected_files = [
            'test_score/test_score/build/letter-portrait/back-cover.tex',
            'test_score/test_score/build/letter-portrait/front-cover.tex',
            'test_score/test_score/build/letter-portrait/music.ly',
            'test_score/test_score/build/letter-portrait/parts.ly',
            'test_score/test_score/build/letter-portrait/preface.pdf',
            'test_score/test_score/build/letter-portrait/preface.tex',
            'test_score/test_score/build/letter-portrait/score.tex',
            ]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--preface',
            ]
        #with systemtools.RedirectedStreams(stdout=self.string_io):
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)

    def test_success_music(self):
        expected_files = [
            'test_score/test_score/build/letter-portrait/back-cover.tex',
            'test_score/test_score/build/letter-portrait/front-cover.tex',
            'test_score/test_score/build/letter-portrait/music.ly',
            'test_score/test_score/build/letter-portrait/music.pdf',
            'test_score/test_score/build/letter-portrait/parts.ly',
            'test_score/test_score/build/letter-portrait/preface.tex',
            'test_score/test_score/build/letter-portrait/score.tex',
            ]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--music',
            ]
        #with systemtools.RedirectedStreams(stdout=self.string_io):
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)

    def test_success_parts(self):
        expected_files = [
            'test_score/test_score/build/letter-portrait/back-cover.tex',
            'test_score/test_score/build/letter-portrait/front-cover.tex',
            'test_score/test_score/build/letter-portrait/music.ly',
            'test_score/test_score/build/letter-portrait/parts-cello.pdf',
            'test_score/test_score/build/letter-portrait/parts-viola.pdf',
            'test_score/test_score/build/letter-portrait/parts-violin-i.pdf',
            'test_score/test_score/build/letter-portrait/parts-violin-ii.pdf',
            'test_score/test_score/build/letter-portrait/parts.ly',
            'test_score/test_score/build/letter-portrait/preface.tex',
            'test_score/test_score/build/letter-portrait/score.tex',
            ]
        self.create_score()
        self.install_fancy_segment_maker()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--parts',
            ]
        #with systemtools.RedirectedStreams(stdout=self.string_io):
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)