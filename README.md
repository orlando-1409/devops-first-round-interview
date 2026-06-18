# Sr. DevOps Engineer Interview — Round 1

Welcome! This is a ~60 minute exercise. Don't worry about finishing everything
— we're more interested in how you think than in a perfect solution.

## The environment

This repo is designed to be opened as a **GitHub Codespace**. When you open it,
the devcontainer will:
- Boot a Python 3.11 environment
- Install runtime and dev dependencies (`pip install -r requirements-dev.txt`)
- Forward port 8000 for the API
- Disable Copilot and other AI panes for the duration of the interview

You should not need to install anything yourself. If `pytest` or `ruff` aren't
on your path when the Codespace finishes building, run:

```bash
pip install -r requirements-dev.txt
```

## The problem

You've been handed a small FastAPI service called **Audience Builder**. Our
engineers use it to define audiences by filtering a `people` table on age.
The application code works — you do **not** need to add product features.

What *doesn't* work is the CI/CD pipeline. Your job has two parts: get the
**CI** pipeline ship-ready, then design how **CD** should work for a service
like this.

### What's in the repo

- `app/` — the FastAPI service (`main.py`, `data.py`, `models.py`).
- `data/people.csv` — 100 rows of mock data backing the API
  (`person_id, age, state, first_name, last_name`).
- `tests/` — pytest suite for the API and data layer.
- `data/people.csv` is treated as a "table" — read-only, no DB.
- `.github/workflows/ci.yml` — the CI workflow. **This is broken.**
- `requirements.txt` — runtime dependencies.
- `requirements-dev.txt` — dev/test dependencies (linting, testing, the
  FastAPI test client).
- `pyproject.toml` — pytest and ruff configuration.

This is a **two-part exercise**. Part 2 is revealed by your interviewer once
Part 1 is wrapped up, so focus on what's in front of you rather than designing
for what might come later.

# Part 1 — Fix the CI pipeline (first ~20 min)

The CI pipeline at `.github/workflows/ci.yml` is broken and slower than it
should be. We want you to:

1. **Reproduce the failure** and walk us through how you'd diagnose it from
   the workflow run output (or from running the same commands locally).
2. **Figure out what's wrong** — there is more than one issue, and they aren't
   all in the workflow file. Some live in the application code that the
   pipeline is meant to be checking. Treat us as teammates pairing with you:
   tell us what you suspect, what you're checking, and what each piece of
   evidence rules in or out.
3. **Fix everything the pipeline surfaces** so it goes green on a PR against
   this repo. That includes any code-quality issues the linter flags — talk
   us through how you'd fix each one and why.
4. **Make it faster.** Once it's green, look for ways to cut wall-clock time
   and explain the trade-offs of each change you make.
5. **Open a PR** with your changes and walk us through it.

We are deliberately not giving you a checklist of what to fix — debugging the
pipeline (and the things it catches) *is* the exercise.

**Time check:** at the 20-minute mark we'll move to Part 2 even if the pipeline
isn't fully polished. Get the must-haves landed first, optimize second.

# Part 2 — Design discussion

Your interviewer will reveal Part 2 once Part 1 is wrapped up. It's a
whiteboarding / discussion session — no coding required. You can sketch in any
tool you're comfortable with. A few free options that work in-browser with no
account:

- [draw.io](https://draw.io) (a.k.a. `app.diagrams.net`)
- [Excalidraw](https://excalidraw.com)
- [tldraw](https://www.tldraw.com)
- [Lucidchart](https://lucid.app) (free tier)

Pick whichever you're fastest in — we care about the design, not the polish.

## How we'll evaluate this

We're looking at **both your CI fix and your CD design**. Specifically:

- **Diagnosis** — can you read a failing pipeline and map each error to a
  cause, instead of guessing and re-running?
- **Correctness of fix** — pipeline goes green, lint issues are actually
  addressed (not suppressed), tests pass.
- **Optimization** — at least a general idea of how to speed a CI job up.
- **CD design judgment** — environment decoupling, immutable artifacts,
  per-environment secrets, a zero-downtime deploy strategy with fast
  rollback, and how you'd *see* a bad deploy in production.
- **Communication** — talking through decisions, asking clarifying questions,
  and reasoning out loud are all encouraged.

## Ground rules

- **No AI assistants.** Copilot is disabled in this devcontainer. Please
  don't use ChatGPT, Claude, Cursor, Gemini, or any other LLM tool in
  another tab — we want to see *your* thinking, not a model's.
- Docs, GitHub issues, Stack Overflow, GitHub Actions / pytest / ruff /
  cloud-provider documentation are all fair game — same as a normal day at
  work.
- Talk us through your reasoning. Silent debugging and silent design are
  hard to evaluate.
- Ask us anything! Clarifying questions are encouraged and aren't held
  against you.

Good luck!

## Running the app and tests

From the repo root:

```bash
# Start the API locally
uvicorn app.main:app --reload

# Run the fast test suite (excludes anything tagged @pytest.mark.slow)
pytest -m "not slow"

# Run every test, including the slow ones
pytest

# Run the linter
ruff check .
```

Try a request once the server is up:

```bash
curl -X POST http://localhost:8000/audiences \
  -H 'content-type: application/json' \
  -d '{"name":"young adults","filters":{"min_age":18,"max_age":30}}'
```


# test