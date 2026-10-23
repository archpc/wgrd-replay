# Player-action timeline plan

Starting branch decoder/counted-blocks; clean HEAD
5be10ad11cdf1d1c8c4dd31206886100852a0d5a. User authorizes autonomous evidence-backed
investigation, implementation, tests, documentation and incremental commits.

- [x] REA/Rizin: trace 07/08/09 dispatch into execution; establish two gameplay
  interpretations. Bound each unproductive research path to two focused passes.
- [x] Investigate slot/player mapping and frame duration. Keep raw frames and
  unknown mapping/time explicit when not proven. No Windows execution.
- [x] Add --timeline only; keep default parser JSON unchanged. Event per command:
  frame, deterministic frame/slot command order, player slot, opcode, class,
  original parameters/bytes, source offsets and interpretation confidence/evidence.
  Preserve opaque/unresolved commands without inventing boundaries or behavior.
- [x] Focused tests first: ordering/count/provenance, opaque/unknown commands,
  malformed lengths, SHA-224 enforcement. Validate all three authenticated samples;
  deterministic CLI output and default-output compatibility. Tested commits.
- [x] Stop at verified minimum: all samples work, >=2 binary-supported command
  interpretations, complete retention, committed findings and measurable coverage.

No global config, GUI, new dependencies, speculative game events or outcome inference.
New timeline module allowed to avoid unrelated changes to the container parser.

Verified milestone: 41 tests; all 11,565 commands retained; 594/594 multi blocks
split; two CLI runs identical per sample; default JSON byte-identical to starting
commit on all three samples. Single bounded review before final commit.
