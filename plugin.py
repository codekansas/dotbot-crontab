#!/usr/bin/env python

import sys
from pathlib import Path
from typing import Any, Dict, List

import dotbot

sys.path.append(str(Path(__file__).parent.resolve()))
from crontab import CronSlices, CronTab


class Crontab(dotbot.Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "crontab"

    def handle(self, directive: str, data: List[Dict[str, Any]]) -> bool:
        if directive != "crontab":
            self._log.error(f"Can't handle directive {directive}")
            return False

        any_changes_requested = False

        for entry in data:
            platform = entry.get("platform")
            if platform is None or platform == sys.platform:
                any_changes_requested = True
        if not any_changes_requested:
            self._log.lowinfo(
                "No actions in crontab task match current platform, exiting"
            )
            return True

        cron = CronTab(user=True)

        # Remove all existing dotbot crontabs.
        removed = cron.remove_all(comment="dotbot")
        updated = removed > 0
        self._log.lowinfo(f"Removing {removed} old dotbot entries from users's crontab")

        # Add from config.
        for i, entry in enumerate(data):
            if "key" in entry and "value" in entry:
                if "platform" in entry and entry.pop("platform") != sys.platform:
                    continue
                cron.env[entry.pop("key")] = entry.pop("value")
                continue

            if "time" not in entry:
                self._log.error(f"Skipping entry {i} - missing `time` config")
                continue
            time = entry.pop("time")
            if "command" not in entry:
                self._log.error(f"Skipping entry {i} - missing `command` config")
                continue
            command = entry.pop("command")
            job = cron.new(command=command, comment="dotbot")

            if not CronSlices.is_valid(time):
                self._log.error(f"Skipping entry {i} - invalid time {time}")
                continue
            job.setall(time)

            if "platform" in entry and entry.pop("platform") != sys.platform:
                job.enable(False)

            if entry:
                self._log.error(f"Unused config keys: {list(entry.keys())}")

            self._log.lowinfo(
                f"Adding command {command} at time {time} to users's crontab"
            )

            updated = True

        if updated:
            cron.write()

        return True
