---
schema_version: 1
story_slug: edit-open-tender
stage: checks
status: findings-open
updated: 2026-11-04T08:10:36Z
fix_cycle: 2
---

## Failing checks

- **test**: > frontend@0.0.0 test
> ng test --watch=false

❯ Building...
✔ Building...
Application bundle generation failed. [2.135 seconds] - 2026-11-04T08:10:36.296Z
[31m✘ [41;31m[[41;97mERROR[41;31m][0m [1mTS2345: Argument of type 'TenderDetail | undefined' is not assignable to parameter of type 'string | number | boolean | Object | ArrayBuffer | Blob | (string | number | boolean | Object | null)[] | null'.
  Type 'undefined' is not assignable to type 'string | number | boolean | Object | ArrayBuffer | Blob | (string | number | boolean | Object | null)[] | null'.[0m [1m[35m[plugin angular-compiler][0m

    /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts:33:22:
[37m      33 │         request.flush([32mtender[37m);
         ╵                       [32m~~~~~~[0m
