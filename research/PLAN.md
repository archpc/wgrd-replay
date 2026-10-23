# Counted command decoder implementation plan

Authorization: user accepted count-loop investigation; binary-backed decoder changes,
focused tests, multiple opcodes and incremental commits authorized. Existing checkout;
no global config changes, downloads, target execution or speculative field semantics.

Architecture: one bounded cursor per command block. Per-opcode readers consume only
creator-proven fields. Complete blocks require exactly count commands and EOF.
Unknown/truncated/extra-byte blocks preserve original bytes and explicit unresolved status.
Keep the opcode-08 single-command interface compatible. New fields use object offsets.

- [x] Recover opcode 09 creator and all failure exits; authentic boundary survey.
- [x] Tests first for cursor, 09, 08 concatenation, unknown suffix and malformed lengths.
      Implement, run relevant suite, record coverage, commit.
- [ ] Rank unresolved block frontiers; recover highest-value next creators and helpers.
      For each meaningful batch: evidence -> authentic survey -> failing tests -> code
      -> tests -> coverage -> commit. No repeated unchanged validation.
- [ ] Finish at 594/594 or a substantial verified subset with a concrete evidence blocker.
      Update FORMAT, REA notes, NEXT-STEPS and reproducible sample coverage.

Review focus: shared variable-length cursor; no heuristic resync; count mismatch;
unknown commands after valid prefixes; malformed lengths/counts bounded before loops;
build 59638 evidence is not cross-version runtime equivalence for Sample2.

Ruling: user supplied the complete scope and opted into autonomous implementation;
no per-opcode design approval or recursive review gates. No additional worktree.
