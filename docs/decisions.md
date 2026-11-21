# Decisions

One line per decision: date, what, why. Newest last. Change a decision by
adding a new line, not by editing the old one.

| Date | Decision | Why |
|---|---|---|
| 2026-11-20 | Standard library only up to milestone 2 | Fewer moving parts while the core takes shape |
| 2026-11-20 | The plan lives in `docs/PLAN.md` | One place we both follow |
| 2026-11-20 | Experiment output goes in `runs/`, ignored by git | Checkpoints and videos grow to gigabytes |
| 2026-11-21 | A snapshot of the robot's control logic is copied into `firmware/vendor/`, with its commit hash | The course repository is private on LiU's GitLab; both of us must be able to build without it. Use of the code is approved |
| 2026-11-21 | Python 3.12 managed with `uv`; `uv.lock` is committed | Both Macs and CI get exactly the same versions |
| 2026-11-21 | Sensors simulated as raw readings, run through Sensormodul's own code | The lag comes from the real filtering instead of a fitted number; both boards' firmware in the loop |
| 2026-11-21 | A wall touch is +5 s and the run goes on; stuck 5 s ends it | Competition rule 5.4; the score must match how the track is judged |
| 2026-11-21 | Runs are headless and deterministic; `experiments/view.py` replays any run with graphics | Batches as fast as possible, and anything trained can still be watched |
| 2026-11-21 | `firmware/update.sh` wraps the firmware's settings in `#ifndef` when copying, so they can be set with `-D` | Tuning without touching the course repository; same code, same defaults |
| 2026-11-21 | The RL policy replaces only the corridor steering (the PID); the state machine still navigates | A fair comparison with the PID, and far more likely to train |
