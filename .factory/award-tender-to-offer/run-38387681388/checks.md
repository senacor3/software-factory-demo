---
schema_version: 1
story_slug: award-tender-to-offer
stage: checks
status: findings-open
updated: 2026-10-13T11:14:33Z
fix_cycle: 2
---

## Failing checks

- **static_analysis**: > frontend@0.0.0 static-analysis
> eslint -c eslint.static-analysis.config.js .
sh: 1: eslint: not found
- **test**: > frontend@0.0.0 test
> ng test --watch=false
sh: 1: ng: not found
