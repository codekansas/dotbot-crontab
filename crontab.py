#!/usr/bin/env python

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import dotbot

# Adds submodule to system path.
sys.path.append(Path(__file__).parent / "python-crontab" / "crontab.py")
from crontab import CronSlices, CronTab


class Crontab(dotbot.Plugin):


    def can_handle(self, directive: str) -> bool:
        return directive == "crontab"

    def handle(self, directive: str, data: List[Dict[str, Any]]) -> bool:
        if directive != "crontab":
            self._log.error(f"Can't handle directive {directive}")
            return False

        cron = CronTab(user=True)

        # Only write crontab if we make a change.
        updated = False

        # Remove all existing dotbot crontabs.
        for job in cron.find_comment(re.compile(r"^dotbot")):
            cron.remove(job)
            updated = True

        # Add from config.
        for i, entry in enumerate(data):
            if "time" not in entry:
                self._log.error(f"Skipping entry {i} - missing `time` config")
                continue
            time = entry.pop("time")
            if "command" not in entry:
                self._log.error(f"Skipping entry {i} - missing `command` config")
                continue
            command = entry.pop("command")
            job = cron.new(command=command, comment="dotbot")

            if "comment" in entry:
                comment = entry.pop("comment")
                job.set_comment(f"{job.comment} - {comment}")

            if not CronSlices.is_valid(time):
                self._log.error(f"Skipping entry {i} - invalid time {time}")
                continue
            job.setall(time)

            if "platform" in entry and entry.pop("platform") != sys.platform:
                job.set_comment(f"{job.comment} - disabled on {sys.platform}")
                job.enable(False)

            if entry:
                self._log.error(f"Unused config keys: {list(entry.keys())}")

            updated = True

        if updated:
            cron.write()

        return True
