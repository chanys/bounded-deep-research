# bounded-deep-research

AnswerTrail: a bounded-corpus deep-research agent (a roll-your-own ReAct loop over a fixed library of single-creator YouTube transcripts), live at `answertrail.yeesengchan.com`.
See `CLAUDE.md` for the architecture and conventions; the plans, build logs, and results live in the sibling `../bounded-deep-research-notes` repo.

## Evaluation (Phase 4)

The offline evaluation instrument lives in `eval/`: a calibrated, nugget-based harness that scores the frozen agent over a gold set of factual and longitudinal questions, cross-family (agent on OpenAI, judge + extractors on the Claude family).

- `make eval-runs` — run the frozen agent over the gold questions, 3 runs each, resumable (`eval/run_batch.py`).
- `make eval-score` — score the runs with the frozen judge + extractors and write `eval/artifacts/scoring_report.md` (`eval/score_runs.py`): recall, groundedness, and a retrieval-ceiling / synthesis-conversion / attribution breakdown, plus the shift and no-change longitudinal checks.
- `python -m eval.make_read_bundle --read-sets` — assemble self-contained per-question read files (`eval/artifacts/read/<qid>.md`: question, gold nuggets, answer, verdicts + reasons, retrieved chunk text) for the human audit of results.

The scoring instrument is versioned by prompt hash and calibrated against human labels (Cohen's kappa 0.879); every scored run and score file carries its provenance. The full set has been scored (`eval/artifacts/scoring_report.md`); method and results are written up per phase in the notes repo (`eval/phase4_phase{A,B,C,D}_*_build_log.md`, plus `eval/session_handoff_2026-07-27.md` for the session-level summary).

For a self-contained narrative of the evaluation (readable without the code), see the two reference docs in the notes repo: `eval/gold_construction_reference.md` (how the gold is built) and `eval/experiments_reference.md` (the experiments, metrics, ablations, and judge calibration).
