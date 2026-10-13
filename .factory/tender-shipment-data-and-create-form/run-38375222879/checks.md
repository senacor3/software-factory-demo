---
schema_version: 1
story_slug: tender-shipment-data-and-create-form
stage: checks
status: findings-open
updated: 2026-10-13T09:32:41Z
fix_cycle: 1
---

## Failing checks

- **build**: > frontend@0.0.0 build
> ng build

❯ Building...
✔ Building...
Application bundle generation failed. [1.647 seconds] - 2026-10-13T09:31:58.230Z
[31m✘ [41;31m[[41;97mERROR[41;31m][0m [1mTS2322: Type 'Currency | null' is not assignable to type 'Currency'.
  Type 'null' is not assignable to type 'Currency'.[0m [1m[35m[plugin angular-compiler][0m

    /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-create/tender-create.ts:248:6:
[37m      248 │       [32mcurrency[37m: value.currency,
          ╵       [32m~~~~~~~~[0m

  The expected type comes from property 'currency' which is declared here on type 'CreateTenderRequest'

    /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-api.ts:81:2:
[37m      81 │   [32mcurrency[37m: Currency;
         ╵   [32m~~~~~~~~[0m
- **test**: > frontend@0.0.0 test
> ng test --watch=false

❯ Building...
✔ Building...
Application bundle generation failed. [1.433 seconds] - 2026-10-13T09:32:10.690Z
[31m✘ [41;31m[[41;97mERROR[41;31m][0m [1mTS2322: Type 'Currency | null' is not assignable to type 'Currency'.
  Type 'null' is not assignable to type 'Currency'.[0m [1m[35m[plugin angular-compiler][0m

    /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-create/tender-create.ts:248:6:
[37m      248 │       [32mcurrency[37m: value.currency,
          ╵       [32m~~~~~~~~[0m

  The expected type comes from property 'currency' which is declared here on type 'CreateTenderRequest'

    /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-api.ts:81:2:
[37m      81 │   [32mcurrency[37m: Currency;
         ╵   [32m~~~~~~~~[0m
