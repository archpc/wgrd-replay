# Recovered REA evidence records (2026-10-26)

Eight evidence IDs cited by `REA-NOTES-59638.md` Sessions 1-3 had no record file in
`research/evidence/`. Time Machine was not readable from this session (Full Disk
Access not granted; APFS local-snapshot mount refused without privileges). The
complete records were found verbatim inside Hermes session request dumps from
2026-10-23 (`~/.hermes/sessions/request_dump_local-91d17880…_20261023_093231_540090.json`),
as `mcp__rea__procedure_pseudo_code` tool results. Each was parsed from the dump's
JSON (two levels of JSON string nesting), checked for the same top-level schema as
the tracked records, and written unmodified with the tracked 2-space formatting.
Subject digest in every record: WarGame3.exe build 59638 SHA-256 1c7533eb…; provider Ghidra 12.1.4.

| Evidence ID | Operation | Procedure | SHA-256 of written file | Source dump (basename) | Dump mtime (UTC) |
|---|---|---|---|---|---|
| `ev_060180193041fc41b30acda6e056d4a626b31faedecc2398dd12cc0d99e42df5` | procedure_pseudo_code | 0x8fb4a0 | `f54d0f480bc160febaf7599cba3d50883444cf153af1fccb3b57082d6e1fca0e` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_0ea526f5556ac2eefb743529ca85e4e31968e9006cc543a1680ab41a54e76e96` | procedure_pseudo_code | 0xb2fbc0 | `9122e7a2c344d70139a6d4f042d92b93deaea3d1fc5ed92c6679baf7f6fa87a7` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_1e924a6e3778ddd804dfd468166067bb2a2bdd836e842ccfe21d79d0a986f0ef` | procedure_pseudo_code | 0xb3ea20 | `3f8d6529df3a736fe531bce7bdfe4de98ed44da22241a8952020d92a2b9425fd` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_37b97e85707a6d1e153be4c1a65fb7fad1cd590022c87473fc6c27558d94c677` | procedure_pseudo_code | 0xb29440 | `79acc067428945f4bc65a122b3ab7cb02bc0def5bc96c8849b352f7aa12aa60f` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_4ea358ce6a87a813127e7bfd582a4263ca5a20e59125ae9cea602ab3c62250de` | procedure_pseudo_code | 0xb3db10 | `7da3dc0a45dac53e9f60b9d9fae01b46d651163062763ab6ed5232c0b34df1d2` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_7841a093d8125d111c2b474600c7995ab5e58a9a93f130fef47f1ed9a762e67a` | procedure_pseudo_code | 0xb3c5d0 | `fc3124e7149b5afeb7d825264356e94a269b984a7da5f91671aa7eeaac1c7945` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_b44efd7d15a9f1813f52e3a9c2859e04ce38fe493f11a4a5155dc2eaf976c2d2` | procedure_pseudo_code | 0x10b9300 | `6acea246049bcc1d0c0ad70ac8d81dff2fd65dc04b258f2e046d4df88c4b6308` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |
| `ev_d3d3f96676e00401abf72bee0657895c67afb4162d43c5e2b1c5608b8e357e31` | procedure_pseudo_code | 0xb2c170 | `d885c82c8250ecf1271f0c3223f247dcbb95161da292aba277d8d5d9c07fb6d7` | `request_dump_local-91d17880d8c44363c1b54ae760cb9b5973082b1c91952b4665d66b7c4326ac4e_20261023_093231_540090.json` | 2026-10-23T13:32:31.864252+00:00 |

Limitations: the dump is a transcript capture, not the REA evidence store; byte
identity with the original store files cannot be proven, only schema and content
consistency with the notes (procedure addresses match REA-NOTES Findings 1, 3 and
Session 3 items 11-14, 17, 18). Backups were not modified.
