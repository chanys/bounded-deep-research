# bounded-deep-research

AnswerTrail: a bounded-corpus deep-research agent (a roll-your-own ReAct loop over a fixed library of single-creator YouTube transcripts), live at `answertrail.yeesengchan.com`.
See `CLAUDE.md` for the architecture and conventions; the plans, build logs, and results live in the sibling `../bounded-deep-research-notes` repo.

## Evaluation (Phase 4)

The offline evaluation instrument lives in `eval/`: a calibrated, nugget-based harness that scores the frozen agent over a gold set of factual and longitudinal questions, cross-family (agent on OpenAI, judge + extractors on the Claude family).

- `make eval-runs` — run the frozen agent over the gold questions, 3 runs each, resumable (`eval/run_batch.py`).
- `make eval-score` — score the runs with the frozen judge + extractors and write `eval/artifacts/scoring_report.md` (`eval/score_runs.py`): recall, groundedness, and a retrieval-ceiling / synthesis-conversion / attribution breakdown, plus the shift and no-change longitudinal checks.

The scoring instrument is versioned by prompt hash and calibrated against human labels (Cohen's kappa); every scored run and score file carries its provenance. Method and results are written up per phase in the notes repo (`eval/phase4_phase{A,B,C,D}_*_build_log.md`).
