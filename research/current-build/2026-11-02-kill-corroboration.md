# Revision 131544: repeated damage sequence and original kill-table evidence

Status: exact repeated observations and visible table labels verified. Replay-file
association remains an inference; per-unit kill credit and source roles are provisional.
No new VM execution was performed for this comparison.

## Pinned inputs

| Input | SHA-256 |
|---|---|
| Original engine | `5eaa6d6168c9570ff9789bffb3b2cc16fd908be61263b12fcc1e8b2f09efc75d` |
| Retained replay `replay_2026-11-01_19-10-26.wargamerpl2` | `abf6a5e909ec976a30d16e043f25220bfb7d7a149cfbf828de992be8e69da121` |
| Older trace `damage-state-combat-02.jsonl` | `95f3592493a3c55da52150e64eb773b68f652f4530dca586458847e1f95a7bd6` |
| New trace `wgrd-aar-combat-20261102-01.jsonl` | `607ee419a674b554051cec998ca8ba619de5c11c8e9de277f071fd7d62f2ba74` |
| Original kill-table image `wgrd-terra-skirmish-21.png` | `62334686777fe120b8a15c47b2fa084b404f588362ad4f2631bdde8504159f1d` |

The traces have different process IDs, creation identities, timestamps and object
addresses. Both pin the same engine. They are not joined by heap address.

## Raw comparison

For every paired impact, align by ordinal and compare nine values:

1. mode;
2. local handle decoded as little-endian u32;
3. raw float32 input-argument bits;
4. suppression +`0x190` before and after;
5. physical damage +`0x19c` before and after;
6. raw +`0x1a0` before and after.

This enumerates nine scalar values per event, not six. All 252 comparisons across
28 events match exactly. There are zero mismatches. Physical transitions occur at
ordinals 3, 7 and 21 in both captures; the other 25 are suppression transitions.

This supports the hypothesis of deterministic re-execution of the same input. It
is not a proof that the complete engine states or loaded files were identical.
Neither capture has a retained native replay-open record. The original narrative
names the retained replay and screenshot. No independent capture/action-manifest
binding was found in the reviewed retained files; session history was not
exhaustively audited. A static replay GUID join is not a playback log.

A prior delegate overstatement is rejected: the older trace did not read +`0x194`
or +`0x198`. Those fields cannot be compared across the captures. The original
little-endian handle bytes must also not be interpreted as a big-endian integer.

## Fresh visual check

The original PNG hash was checked before inspection. Local Apple Vision OCR was
used only to locate public unit-label words and construct privacy-filtered crops;
profile and chat pixels were excluded before external visual inspection. The OCR
missed one victim label. A separate unit-type-column crop showed three fully legible
rows, each reading `VTT-323`. That establishes three visible rows, not a complete list.

Two visible attacker-type labels read exactly `MERKAVA IIID BAZ`. The runtime
native descriptor debug name is `Unit_Merkava_IIIB_Baz`. The display and internal
strings are preserved literally; localization/alias equivalence is not assumed.
No callsign, player identity or native handle was recovered from this check.

## Bounded conclusion

The [live owner/type bridge](2026-11-02-live-unit-attribution.md) independently
resolves the new capture's six damaged handles to `Unit_VTT_323_NK`. Three distinct
handles (33, 31, 39) reach the observed native physical-damage threshold and each
parents an owner-destruction call. Three further cleanup calls remain excluded.

The three visible `VTT-323` kill-table entries agree with that count and type.
This is corroboration at the cohort/type-count level only. It does not establish:

- which table row corresponds to which runtime handle;
- whether the visible table includes every kill;
- whether each observed destruction invocation produced a scored kill;
- shooter, weapon, projectile or player attribution;
- an assignment of the two UI labels to owners 74 and 75;
- score arithmetic from the displayed value 30;
- ownership/side or battle-time/replay-frame mapping.

The structured [runtime AAR](2026-11-02-runtime-aar.md) therefore retains unknown
per-event kill outcomes. Its source-role fields are not upgraded by this agreement.

## Reproduction and retained evidence

Private artifacts under `aar-20261102T050816Z/`:

- `same-replay-corroboration.json` and `.md`: independent comparison report; its
  stronger same-input/maxima wording is superseded by the qualifications above.
- `same-sequence-lead-verification.json`: independently repeated raw-bit comparison,
  complete per-ordinal values and explicit corrections.
- `kill-table-visual-observation.json`: visible-label transcription and limits.
- `kill-table-local-ocr.swift`, `kill-table-local-word-boxes.json`: local extraction
  recipe and allowlisted word rectangles, not a complete OCR transcript.
- `kill-table-privacy-mask.json` and `kill-table-victim-type-column-provenance.json`:
  original/derived hashes, crop coordinates and scaling.
- `existing-evidence-aar-v1/kill-corroboration.json`: structured sidecar containing
  the agreement level and unresolved row/credit mappings; core event files are unchanged.

The original replay, PNG, traces and older derived outputs remain unchanged.
A future live capture must observe the actual replay-open path and preserve the
read-only engine evidence before any stronger file/row attribution is published.
