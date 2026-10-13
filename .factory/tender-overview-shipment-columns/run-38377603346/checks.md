---
schema_version: 1
story_slug: tender-overview-shipment-columns
stage: checks
status: findings-open
updated: 2026-10-13T09:44:16Z
fix_cycle: 1
---

## Failing checks

- **lint**: > frontend@0.0.0 lint
> ng lint


Linting "frontend"...

/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-test-data.ts
  31:23  error  '_count' is assigned a value but never used   @typescript-eslint/no-unused-vars
  31:50  error  '_lowest' is assigned a value but never used  @typescript-eslint/no-unused-vars

✖ 2 problems (2 errors, 0 warnings)
Lint errors found in the listed files.
- **static_analysis**: > frontend@0.0.0 static-analysis
> eslint -c eslint.static-analysis.config.js .


/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-test-data.ts
  31:23  error  '_count' is assigned a value but never used              @typescript-eslint/no-unused-vars
  31:23  error  Remove the declaration of the unused '_count' variable   sonarjs/no-unused-vars
  31:50  error  '_lowest' is assigned a value but never used             @typescript-eslint/no-unused-vars
  31:50  error  Remove the declaration of the unused '_lowest' variable  sonarjs/no-unused-vars

✖ 4 problems (4 errors, 0 warnings)
