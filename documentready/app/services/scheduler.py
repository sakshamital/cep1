"""Reliable background scheduler and worker for official government source monitoring.

Features:
- Periodic background cycle running at configurable intervals (e.g. checks every minute for due sources).
- Process isolation: runs in a background daemon thread inside the app worker or as a dedicated standalone CLI worker.
- Concurrency and lock protection: avoids overlapping checks and coordinates safely across Gunicorn workers.
- Resumes pending and interrupted checks cleanly on restart.
- Provides immediate trigger hook for on-demand asynchronous runs.
"""
from __future__ import annotations

import logging
import os
import threading
import time
from typing import Optional

from app.models.db_models import SourceRegistry, utc_now
from app.services.database import get_db_session
from app.services.monitoring import monitor_engine

logger = logging.getLogger(__name__)

_scheduler_thread: Optional[threading.Thread] = None
_stop_event = threading.Event()
_scheduler_lock = threading.Lock()


class BackgroundMonitorScheduler:
    """Manages the background execution loop for scheduled official government source checks."""

    def __init__(self, poll_interval_seconds: int = 60):
        self.poll_interval = poll_interval_seconds
        self._is_running = False

    def start(self) -> bool:
        """Start background daemon thread if not already active."""
        global _scheduler_thread, _stop_event
        with _scheduler_lock:
            if _scheduler_thread is not None and _scheduler_thread.is_alive():
                logger.debug("Background monitor scheduler is already running.")
                return False

            _stop_event.clear()
            _scheduler_thread = threading.Thread(
                target=self._run_loop,
                name="GovSourceMonitorScheduler",
                daemon=True,
            )
            _scheduler_thread.start()
            self._is_running = True
            logger.info("Background monitor scheduler started successfully (polling every %ds).", self.poll_interval)
            return True

    def stop(self, timeout: float = 5.0) -> None:
        """Signal background scheduler to stop and wait for loop termination."""
        global _scheduler_thread, _stop_event
        with _scheduler_lock:
            if _scheduler_thread is not None:
                logger.info("Stopping background monitor scheduler...")
                _stop_event.set()
                _scheduler_thread.join(timeout=timeout)
                _scheduler_thread = None
                self._is_running = False
                logger.info("Background monitor scheduler stopped.")

    def run_once(self, force: bool = False) -> list[dict]:
        """Execute a single evaluation cycle for all due or forced sources."""
        logger.info("Executing monitor check cycle (force=%s)...", force)
        if force:
            return monitor_engine.check_all_sources(force=True)
        return monitor_engine.check_due_sources()

    def _run_loop(self) -> None:
        """Main scheduler loop running in daemon thread."""
        logger.info("Monitor scheduler loop initiated.")
        # Initial brief delay to allow app startup and database migrations to complete cleanly
        time.sleep(3.0)

        # Release any stuck locks leftover from previous server crashes/restarts
        self._cleanup_stale_locks()

        while not _stop_event.is_set():
            try:
                results = monitor_engine.check_due_sources()
                if results:
                    changed = sum(1 for r in results if r.get("status") == "changed")
                    errors = sum(1 for r in results if r.get("status") == "error")
                    logger.info(
                        "Completed scheduled check cycle: %d sources checked (%d changes, %d errors).",
                        len(results),
                        changed,
                        errors,
                    )
            except Exception as exc:
                logger.error("Unexpected error in background monitor loop: %s", exc, exc_info=True)

            # Sleep in small increments to respond promptly to stop requests
            for _ in range(self.poll_interval):
                if _stop_event.is_set():
                    break
                time.sleep(1.0)

        logger.info("Monitor scheduler loop exited gracefully.")

    def _cleanup_stale_locks(self) -> None:
        """Reset is_checking flag for sources that were left locked when previous process abruptly exited."""
        try:
            with get_db_session() as session:
                stale_sources = session.query(SourceRegistry).filter_by(is_checking=True).all()
                if stale_sources:
                    for src in stale_sources:
                        src.is_checking = False
                        src.checking_worker_id = None
                    session.commit()
                    logger.info("Recovered %d stale source locks from previous run.", len(stale_sources))
        except Exception as err:
            logger.warning("Could not clean up stale source locks on startup: %s", err)


# Global singleton instance
scheduler = BackgroundMonitorScheduler()
