---
schema_version: 1
story_slug: edit-open-tender
stage: checks
status: unresolved-after-cap
updated: 2026-11-04T08:11:12Z
fix_cycle: 2
---

## Failing checks

- **test**: > frontend@0.0.0 test
> ng test --watch=false

❯ Building...
✔ Building...
Initial chunk files                                | Names                                           |  Raw size
chunk-7M6BHYHJ.js                                  | -                                               |  76.47 kB | 
chunk-GX5JOUP7.js                                  | -                                               |  51.27 kB | 
spec-app-tender-detail-tender-detail.js            | spec-app-tender-detail-tender-detail            |  42.20 kB | 
chunk-ZBVADLRZ.js                                  | -                                               |  25.54 kB | 
spec-app-tender-overview-tender-overview.js        | spec-app-tender-overview-tender-overview        |  19.63 kB | 
styles.css                                         | styles                                          |  16.68 kB | 
chunk-SOGWMKOD.js                                  | -                                               |  15.38 kB | 
spec-app-tender-create-tender-create.js            | spec-app-tender-create-tender-create            |  13.98 kB | 
spec-app-tender-edit-tender-edit.js                | spec-app-tender-edit-tender-edit                |   8.54 kB | 
spec-app-tender-api.js                             | spec-app-tender-api                             |   5.57 kB | 
chunk-RSTWSNOR.js                                  | -                                               |   4.80 kB | 
spec-app-table-sort.js                             | spec-app-table-sort                             |   4.18 kB | 
spec-app-tender-format.js                          | spec-app-tender-format                          |   3.03 kB | 
spec-app-app.js                                    | spec-app-app                                    |   3.02 kB | 
chunk-Q3MJPO3J.js                                  | -                                               |   2.68 kB | 
chunk-X2VYMMG2.js                                  | -                                               |   2.45 kB | 
init-testbed.js                                    | init-testbed                                    |   2.27 kB | 
chunk-FXV4AZXE.js                                  | -                                               |   2.10 kB | 
chunk-4IO5JKOM.js                                  | -                                               |   1.60 kB | 
spec-app-tender-create-tender-create-validators.js | spec-app-tender-create-tender-create-validators |   1.58 kB | 
chunk-BLMD3KD4.js                                  | -                                               |   1.31 kB | 
vitest-mock-patch.js                               | vitest-mock-patch                               | 988 bytes | 
init-compiler.js                                   | init-compiler                                   | 166 bytes | 

                                                   | Initial total                                   | 305.44 kB

Application bundle generation complete. [2.043 seconds] - 2026-11-04T08:11:09.595Z


[1m[30m[46m RUN [49m[39m[22m [36mv5.0.3 [39m[90m/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend[39m

 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-overview/tender-overview.spec.ts [2m([22m[2m33 tests[22m[2m)[22m[33m 586[2mms[22m[39m
 [31m❯[39m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts [2m([22m[2m12 tests[22m[2m | [22m[31m11 failed[39m[2m)[22m[32m 121[2mms[22m[39m
   [31m❯[39m TenderEdit [2m(12)[22m
[31m     [31m×[31m shows a German loading message before the response arrives[39m[32m 22[2mms[22m[39m
[31m     [31m×[31m shows the detail page error for a load failure and keeps the back link[39m[32m 5[2mms[22m[39m
     [32m✓[39m shows the detail page error for a non-numeric id without a request[32m 37[2mms[22m[39m
[31m     [31m×[31m shows not-editable and no form for a tender that is not open[39m[32m 5[2mms[22m[39m
[31m     [31m×[31m prefills the form including the ADR class and the temperature range[39m[32m 6[2mms[22m[39m
[31m     [31m×[31m disables Speichern while nothing changed and enables it after a valid change[39m[32m 7[2mms[22m[39m
[31m     [31m×[31m accepts a stored past bid deadline but rejects a changed past date[39m[32m 7[2mms[22m[39m
[31m     [31m×[31m sends the complete data via PUT and navigates to the detail page on success[39m[32m 5[2mms[22m[39m
[31m     [31m×[31m points Abbrechen and the back link at the detail page without a request[39m[32m 10[2mms[22m[39m
[31m     [31m×[31m locks every field but delivery date and bid deadline when offers exist[39m[32m 7[2mms[22m[39m
[31m     [31m×[31m shows the conflict message for a 409 and keeps the entered values[39m[32m 5[2mms[22m[39m
[31m     [31m×[31m shows the generic message for another failure and keeps the entered values[39m[32m 4[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-api.spec.ts [2m([22m[2m11 tests[22m[2m)[22m[32m 33[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/table-sort.spec.ts [2m([22m[2m11 tests[22m[2m)[22m[32m 3[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-format.spec.ts [2m([22m[2m11 tests[22m[2m)[22m[32m 4[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/app.spec.ts [2m([22m[2m3 tests[22m[2m)[22m[32m 22[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-create/tender-create-validators.spec.ts [2m([22m[2m4 tests[22m[2m)[22m[32m 1[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-create/tender-create.spec.ts [2m([22m[2m26 tests[22m[2m)[22m[33m 1122[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts [2m([22m[2m56 tests[22m[2m)[22m[33m 1535[2mms[22m[39m

[2m Test Files [22m [1m[31m1 failed[39m[22m[2m | [22m[1m[32m8 passed[39m[22m[90m (9)[39m
[2m      Tests [22m [1m[31m11 failed[39m[22m[2m | [22m[1m[32m156 passed[39m[22m[90m (167)[39m
[2m   Start at [22m 08:11:09
[2m   Duration [22m 2.83s[2m (environment 52%, tests 32%, setup 7%, import 5%, transform 4%)[22m


::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > shows a German loading message before the response arrives,line=44,column=17::TypeError: Cannot read properties of null (reading 'querySelector')%0A ❯ element src/app/tender-edit/tender-edit.spec.ts:44:17%0A ❯ src/app/tender-edit/tender-edit.spec.ts:68:12%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > shows the detail page error for a load failure and keeps the back link,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:76:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > shows not-editable and no form for a tender that is not open,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:90:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > prefills the form including the ADR class and the temperature range,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:97:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > disables Speichern while nothing changed and enables it after a valid change,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:117:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > accepts a stored past bid deadline but rejects a changed past date,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:131:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > sends the complete data via PUT and navigates to the detail page on success,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:141:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > points Abbrechen and the back link at the detail page without a request,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:171:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > locks every field but delivery date and bid deadline when offers exist,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:178:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > shows the conflict message for a 409 and keeps the entered values,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:204:5%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-edit/tender-edit.spec.ts,title=[frontend] src/app/tender-edit/tender-edit.spec.ts > TenderEdit > shows the generic message for another failure and keeps the entered values,line=31,column=32::Error: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ open src/app/tender-edit/tender-edit.spec.ts:31:32%0A ❯ src/app/tender-edit/tender-edit.spec.ts:218:5%0A%0A
[90mstderr[2m | src/app/tender-detail/tender-detail.spec.ts[2m > [22m[2mTenderDetail[2m > [22m[2mshows remarks/offers for an open tender with enabled add-forms, and appends a new remark/offer without reloading
[22m[39mNG0406: This instance of the `ApplicationRef` has already been destroyed.
NG0406: This instance of the `ApplicationRef` has already been destroyed.
NG0406: This instance of the `ApplicationRef` has already been destroyed.


[31m⎯⎯⎯⎯⎯⎯[39m[1m[41m Failed Tests 11 [49m[22m[31m⎯⎯⎯⎯⎯⎯⎯[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mshows a German loading message before the response arrives
[31m[1mTypeError[22m: Cannot read properties of null (reading 'querySelector')[39m
[36m [2m❯[22m element src/app/tender-edit/tender-edit.spec.ts:[2m44:17[22m[39m
    [90m 42|[39m
    [90m 43|[39m   function element<T extends HTMLElement>(testId: string): T | null {
    [90m 44|[39m     return root.querySelector<T>(`[data-testid="${testId}"]`);
    [90m   |[39m                 [31m^[39m
    [90m 45|[39m   }
    [90m 46|[39m
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m68:12[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mshows the detail page error for a load failure and keeps the back link
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m76:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mshows not-editable and no form for a tender that is not open
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m90:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mprefills the form including the ADR class and the temperature range
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m97:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mdisables Speichern while nothing changed and enables it after a valid change
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m117:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22maccepts a stored past bid deadline but rejects a changed past date
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m131:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[6/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22msends the complete data via PUT and navigates to the detail page on success
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m141:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[7/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mpoints Abbrechen and the back link at the detail page without a request
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m171:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[8/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mlocks every field but delivery date and bid deadline when offers exist
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m178:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[9/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mshows the conflict message for a 409 and keeps the entered values
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m204:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[10/11]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-edit/tender-edit.spec.ts[2m > [22mTenderEdit[2m > [22mshows the generic message for another failure and keeps the entered values
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1", found none.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m open src/app/tender-edit/tender-edit.spec.ts:[2m31:32[22m[39m
    [90m 29|[39m     await Promise.resolve();
    [90m 30|[39m     if (tender !== undefined || status !== 200) {
    [90m 31|[39m       const request = httpMock.expectOne('/api/tenders/1');
    [90m   |[39m                                [31m^[39m
    [90m 32|[39m       if (status === 200) {
    [90m 33|[39m         request.flush(tender!);
[90m [2m❯[22m src/app/tender-edit/tender-edit.spec.ts:[2m218:5[22m[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[11/11]⎯[22m[39m
