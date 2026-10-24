# Sample1: named orders reveal intent; most tactical verbs remain unknown

Example battle report from build59638, map `Destruction_2x3_Tohoku_Alt`.
Frames0–19032; four recorded command slots. Frame duration and player/team mapping
unknown. S0–S3 below mean recorded slots, not ownership or named players.

The analyzer recovers a recognizable sequence: named movement and unloading
requests, aircraft and other unit types receiving Shoot requests, repeated tank
Reverse requests, a declared push, and later fire requests. It cannot establish
territory gained, losses, successful attacks or a winner. This is a report of
recorded intent and player statements, with explicit gaps in the battle itself.

## Opening: movement and unloading requests across all four slots

At **frame131**, S2 places the text marker **“leave your cv at base”** [event29].
This records a coordination request; it does not locate or identify a command
vehicle.

Around **frames1050–1106**, all four slots issue explicit Move requests:

- **S1, frame1050:** eight actor references configured as four VAB, VAB VDAA,
  VAB T20/13, AMX-30 ROLAND 3 and AMX-10 RC #reco1 [105].
- **S2, frame1051:** nine references including T-72S, T-72M1 WILK, W-3U
  SALAMANDRA #reco2, SKOT-2AP, BTR-50, TOPAS, 9K33M2 ROMB and two ZIL-157 [107].
- **S0, frame1052:** DAF YA 4440, two MARDER 1A1 references, M113A1G and LVT-4
  receive one Move request [109].
- **S3, frame1064:** OT-64C receives a Move request [111]. At frame1106 another
  Move request names T-72M2 MODERNA, STROP 2, ShM vz.85 PRAM-S,
  BPzV SNĚŽKA #reco1 and OT-64C [127; full audit CSV].

Explicit **UnloadFromTransport** requests follow: S1 VAB at **1078** [117],
S0 AB-204B at **1117** [130], S0 DORNIER 205 at **1153** [139], and S3 Mi-17
at **1235** [153]. These are transport-handling requests, not confirmed passenger
deployments. Initial purchase/deployment composition remains unavailable from
the opaque production payloads. Reference counts above are not physical-unit counts.

## Explicit fire and reversal requests become visible

At **frame1564**, S2 requests **Reverse** for a T-72S reference [286]. At
**1902**, S3 requests **Shoot** for a MIG-29 9-12A reference [383]; at **1980**,
the same slot requests Shoot for ShM vz.85 PRAM-S [412]. At **2112**, S2 requests
**Land** for W-3U SALAMANDRA #reco2 [447].

These establish recognizable requested actions. The MiG request does not prove
an aircraft took off, fired a weapon or hit anything. Reverse does not establish
a retreat under fire. Earlier contextual orders prevent treating frame1902 as
the beginning of combat.

At **3450**, S2 marks **“got thier cv”** [766]. Later S2 asks **“if you could
spare a cv”** at **4164** [938] and **“we need a cv here”** at **5826** [1426].
The apparent command-vehicle story comes from player-written markers. No command
vehicle kill, shortage, transfer or sector capture is verified.

## A declared push: named participants, mostly missing verbs

At **6125**, S3 marks **“leo dead?”** [1501]; S2 marks **“yup”** at **6200**
[1518]. Their sequence suggests a possible exchange, but neither the referent
nor the asserted loss is established. S2 then marks **“smoke”** at **6321**
[1544] and **“gonna push”** at **6360** [1554]. These are map-marker text;
the word smoke is not evidence of a smoke weapon being fired.

In **S2's frames6321–6999**, the analyzer sees **54 standard-order commands**:
**50 contextual39**, **two Move**, **one UnloadFromTransport**, **one Reverse**.
The partial records include references configured as KOMANDOSI, BTR-50,
T-72M1 WILK and JÄÄKÄRI '90. Some commands address the latter two types together
[1556,1570,1699,1733 and full CSV].

The explicit fragments are concrete: **BTR-50 unload at6455** [1573],
**T-72M1 WILK Move at6571 and6792** [1615,1727], and **T-72M1 WILK Reverse
at6985** [1820]. The report cannot tell whether the intended push advanced,
engaged targets, stalled or withdrew. **92.6% of this window's standard-order
verbs remain unresolved.** This is the central narrative gap, despite complete
static-name coverage.

## Later fire requests continue; the battle result stays unknown

Later explicit Shoot requests name **MARS at9694** [2466], **VPM 120 at9985**
[2514], **ETENDARD IVM at10415** [2599], **ONDAVA at10613** [2670],
**RAKH 91 at11596** [2857], and **M110A2 at12803** [2994].

Across the entire replay, VPM 120 references receive **44 Shoot requests** and
ShM vz.85 PRAM-S references receive **36**. Those80 requests account for58.8%
of the136 explicit Shoot commands. This is concentration within the readable
Shoot subset, not measured damage contribution or total weapon use.

S2's **“killed some shit in here”** marker at **13835** [3136] remains a player
claim. A **“tank”** marker follows at **17087** [3871]. The final two command
records are Shoot requests: S2 RAKH 91 at **19021** [4160], S1 VPM 120 at
**19029** [4161]. Recorded frames end at19032. No winner, final score, confirmed
kill list or surviving army is recoverable from this report.

## How much is meaningful, partial or opaque?

This rubric measures **request-level readability**, not correctness of outcomes
or percentage of the battle understood. Each of all4162 command events belongs
to exactly one tier; commands are unweighted and may contain several actors.

| Tier | Commands | Share | What can be said |
|---|---:|---:|---|
| Meaningful request | 520 | 12.5% | 476 named explicit standard orders +44 marker create/remove requests |
| Partial | 3318 | 79.7% | Contextual39 with named configured references; effective verb/outcome unknown |
| Opaque to narrative | 324 | 7.8% | Gameplay meaning unavailable in the current analyzer |
| Total | 4162 | 100.0% | Entire command population |

The last tier separates into **233 commands with opaque interiors**, **42 with
unsupported layouts**, and **49 with known layouts but uninterpreted gameplay
fields**. All233 opaque-interior records have the RTTI class
TNetworkActionProductionUnite. That name is a lead, not a decoded purchase or
spawn record. Layout decoding covers3887/4162 events (93.4%); this does not imply
comparable narrative coverage.

Considering standard orders alone, **476/3794 =12.5% have an explicit requested
verb;3318/3794 =87.5% remain contextual**. Static names resolve285/285 reference
records across102 configured types. **Zero events have verified execution
outcomes.** That does not mean no actions succeeded; outcome evidence is absent.

Readability also differs sharply by recorded slot:

| Slot | Standard orders | Explicit verbs | Explicit share |
|---|---:|---:|---:|
| S0 | 1574 | 104 | 6.6% |
| S1 | 669 | 152 | 22.7% |
| S2 | 516 | 81 | 15.7% |
| S3 | 1035 | 139 | 13.4% |

This describes analyzer coverage. It cannot establish that S1 played more
actively or S0 issued fewer meaningful tactical actions.

## Selection, evidence and practical value

The narrative deliberately selects readable examples. Its selected source ledger
also includes partial and opaque examples; that selection is not used to estimate
coverage. Of its45 selected anchors,39 (86.7%) are meaningful requests,4 (8.9%)
partial and2 (4.4%) opaque to narrative. These are source-event counts, not a
word-level score for the prose; the example report is intentionally more readable
than the full stream. The full4162-row events.csv is the coverage denominator and includes
every event, tier reason, frame, slot, localized references, source byte offset
and raw coordinate argument. R001-style labels are report-local reference labels,
not physical-unit IDs. reference-labels.json maps them to complete replay-scoped IDs.

Every bracketed number above is a zero-based command_order in the full CSV.
anchors.json provides a convenient selected subset. Coordinates remain uncalibrated
transmitted arguments; no route, frontline or geographical direction asserted.
Dictionary markup and spacing remain verbatim in the audit data; prose occasionally
omits trailing whitespace. Player names/teams remain unlinked to slots.

The analyzer is useful today for **named order search, transport/unload request
history, explicit fire-request summaries and player-marker context**. It does
not yet support a reliable account of engagements, territorial changes, losses
or why a side won. Most of that gap is unresolved effective order/state behavior,
not missing localized names.

Reproduce from the authenticated replay and committed descriptor index:
`python3 -B research/sample1_battle_report.py`. Measurements and CSV are derived
without changing the decoder, game assets or uncertainty fields.
