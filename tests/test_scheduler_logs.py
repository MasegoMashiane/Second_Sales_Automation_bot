# python
import pytest
from unittest.mock import patch
import run_scheduler
from run_scheduler import main

def test_main_schedules_and_logs():
    scheduled_jobs = []

    class MockJob:
        def __init__(self, interval=None):
            self.interval = interval
            self.at_called_with = None
            self.do_called_with = None
            # allow chaining: schedule().day.at(...).do(...) and schedule(interval).minutes.do(...)
            self.day = self
            self.minutes = self

        def at(self, time_str):
            self.at_called_with = time_str
            return self

        def do(self, func):
            self.do_called_with = func
            scheduled_jobs.append(self)
            return self

    def fake_every(interval=None):
        return MockJob(interval=interval)

    class BreakLoop(Exception):
        pass

    def raise_breakloop():
        # when schedule.run_pending is called, raise to break out of the infinite loop in main()
        raise BreakLoop

    # Patch the schedule/time/logging objects used inside run_scheduler module
    with patch('run_scheduler.schedule.every', side_effect=fake_every) as mock_every, \
         patch('run_scheduler.schedule.run_pending', side_effect=raise_breakloop) as mock_run_pending, \
         patch('run_scheduler.time.sleep') as mock_sleep, \
         patch('run_scheduler.logger.info') as mock_log:

        # Call main and allow BreakLoop to stop the loop
        try:
            main()
        except BreakLoop:
            pass

    # Verify three jobs were scheduled
    assert len(scheduled_jobs) == 3

    # First scheduled job: daily at 09:00 -> run_sales
    first = scheduled_jobs[0]
    assert first.at_called_with == "09:00"
    assert first.do_called_with == run_scheduler.run_sales

    # Second scheduled job: every 30 minutes -> run_social
    second = scheduled_jobs[1]
    assert second.interval == 30
    assert second.do_called_with == run_scheduler.run_social

    # Third scheduled job: daily at 18:00 -> collect_metrics
    third = scheduled_jobs[2]
    assert third.at_called_with == "18:00"
    assert third.do_called_with == run_scheduler.collect_metrics

    # Verify logging.info was called with expected messages
    logged_messages = [call.args[0] for call in mock_log.call_args_list]
    assert any("Automation Scheduler Started" == msg for msg in logged_messages)
    assert any("=" * 50 == msg for msg in logged_messages)
    assert any("Sales campaigns: Daily at 09:00" == msg for msg in logged_messages)
    assert any("Social posts: Every 30 minutes" == msg for msg in logged_messages)
    assert any("Metrics collection: Daily at 18:00" == msg for msg in logged_messages)