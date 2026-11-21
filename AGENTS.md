# Instructions for AI coding agents

Both of us work in this repository with AI coding agents. This file is what
every agent follows; `CLAUDE.md` points Claude Code here. Keep it short and
current: an agent that follows a stale line does the wrong thing with
confidence.

## Read first

- `README.md`: what the project is.
- `docs/PLAN.md`: the tasks. Work only on a task listed there.
- `docs/DESIGN.md`: how the parts fit together.
- `docs/decisions.md`: what is already decided. Do not reopen a decision
  without asking the person you work with.
- `data/README.md`: what has been measured, and where each value comes from.

## Commands

```
uv sync                                          # set up .venv from uv.lock
uv run python -m unittest discover -s tests -t . # tests
uv run ruff check . --fix                        # lint
```

Never run `ruff format`: the aligned comments are on purpose. Add a
dependency with `uv add <package>` (`uv add --dev` for tools), never with
pip, and commit `pyproject.toml` and `uv.lock` together.

## Rules

- **Never push to `main`.** It is protected: every change goes through a
  pull request from a branch, needs green CI and the other person's
  approval. One branch and one pull request per task in `docs/PLAN.md`.
- **Run the tests and ruff before saying a change works**, and say which you
  ran.
- **Update the docs in the same change:** tick the task in `docs/PLAN.md`,
  add a line to `docs/decisions.md` for a choice someone would otherwise ask
  about, and keep `data/README.md` in step with `mazesim/params.py`.
- **Every value in `mazesim/params.py` says where it came from:** measured
  (with date), derived, or guess (with the measurement that would replace
  it). Never invent a measurement.
- **The robot's firmware is not in this repository yet,** and nothing that
  needs it is built until the course project's firmware is finished
  (`docs/decisions.md`). Do not copy it in or write code that depends on it.
- **Standard library only** in `mazesim/` until milestone 2; the simulator
  core never imports matplotlib (`docs/DESIGN.md`, fast without graphics).
- **Commit messages:** one short line saying what changed. No AI
  attribution or co-author lines.
- Code, comments, docs and commit messages in English.
