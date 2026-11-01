# -*- coding: utf-8 -*-
from datetime import datetime

from watchtimer import WatchTimer


def test_counts_active_time_across_episodes_without_pause_seek_or_buffering():
    timer = WatchTimer()
    timer.observe('a', 10, now=0)
    timer.observe('a', 11, now=1)
    timer.observe('a', 12, paused=True, now=2)
    timer.observe('a', 12, now=100)
    timer.observe('a', 200, now=101)
    timer.observe('a', 201, now=120)
    timer.observe('b', 0, now=121)
    timer.observe('b', 1, now=122)
    assert timer.elapsed == 2


def test_optional_timer_and_daily_bedtime():
    timer = WatchTimer()
    timer.elapsed = 3600
    before = datetime(2026, 11, 1, 22, 59)
    at = datetime(2026, 11, 1, 23, 0)
    tomorrow = datetime(2026, 11, 2, 23, 0)
    assert not timer.due(0, False, 23, 0, now=at)
    assert timer.due(60, False, 23, 0, now=before)
    assert not timer.due(0, True, 23, 0, now=before)
    assert timer.due(0, True, 23, 0, now=at)
    timer.reset(acknowledge_bedtime=True, now=at)
    assert timer.elapsed == 0
    assert not timer.due(0, True, 23, 0, now=at)
    assert timer.due(0, True, 23, 0, now=tomorrow)


def test_bedtime_stays_pending_if_episode_ends_after_midnight():
    timer = WatchTimer()
    timer.mark_bedtime(True, 23, 0, now=datetime(2026, 11, 1, 23, 30))
    after_midnight = datetime(2026, 11, 2, 0, 15)
    assert timer.due(0, True, 23, 0, now=after_midnight)
    timer.reset(acknowledge_bedtime=True, now=after_midnight)
    assert not timer.due(0, True, 23, 0, now=after_midnight)
