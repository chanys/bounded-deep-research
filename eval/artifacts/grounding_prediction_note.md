# Grounding prediction note (Task 7)

Two pre-registered predictions (cc_07 item 5). A failure is a stop-and-investigate signal.

## factual
input 50; leakage-drop 0 (0.0%); unanswerable-drop 0 (0.0%); errors 0
(a) leakage vs legacy 0.0%: OK (lower)
(b) unanswerable attrition: OK (low)

## comparative
input 40; leakage-drop 0 (0.0%); unanswerable-drop 13 (32.5%); errors 0
(a) leakage vs legacy 0.0%: OK (lower)
(b) unanswerable attrition: TRIPPED -> investigated -> EXPLAINED (not confirmed). Fired at 32.5% unanswerable. Hypothesized cause (extractor hallucination) RULED OUT: the claims are real and chunk-anchored. Actual cause = instrument shape-mismatch - strict per-video grounding cannot evidence a two-sided comparison (only 5/29 pass candidates have BOTH pre-attached sides independently grounded, 6/29 are multi-video by any chunk; the same per-video limitation was verified on longitudinal). The tripwire worked: it fired, forced the investigation, and found a different cause than hypothesized. See build log D69/D70.

## longitudinal
input 38; leakage-drop 0 (0.0%); unanswerable-drop 1 (2.6%); errors 0
(a) leakage vs legacy 0.0%: OK (lower)
(b) unanswerable attrition: OK (low)

