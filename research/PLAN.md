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
- [x] Rank unresolved block frontiers; recover highest-value next creators and helpers.
      For each meaningful batch: evidence -> authentic survey -> failing tests -> code
      -> tests -> coverage -> commit. No repeated unchanged validation.
- [x] Finish at 594/594 or a substantial verified subset with a concrete evidence blocker.
      Update FORMAT, REA notes, NEXT-STEPS and reproducible sample coverage.

Review focus: shared variable-length cursor; no heuristic resync; count mismatch;
unknown commands after valid prefixes; malformed lengths/counts bounded before loops;
build 59638 evidence is not cross-version runtime equivalence for Sample2.

Ruling: user supplied the complete scope and opted into autonomous implementation;
no per-opcode design approval or recursive review gates. No additional worktree.

Completion: all 594 multi blocks split (571 complete, 23 explicitly opaque-framed).
31 tests passed; coverage census checks authenticated bytes and exact reassembly.
No opcode scanner, global configuration edits, target execution, or recursive reviews.

Final verification: independent census completed; CLI summary smoke on authenticated
Sample2 reports 4/4 split and 2/4 complete layouts. All 19 retained REA records have
successful exit status and unchanged target hashes. One bounded read-only final
review found no material issues; no test rerun or recursive delegation during review.
