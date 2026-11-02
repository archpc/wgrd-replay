# Agent instructions

Follow [CONTRIBUTING.md](CONTRIBUTING.md). It is the single rule set for humans
and agents. The hard stops:

- Never touch the ASCII cow in `wgrd_orders.py`.
- No game launch, VM operation or runtime instrumentation without explicit
  authorization in the current request.
- No force-push, history rewrite, `git add -A` or unauthorized merge.
- No secrets, replay bytes, game binaries or private player data in Git.
