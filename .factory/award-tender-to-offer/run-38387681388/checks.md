---
schema_version: 1
story_slug: award-tender-to-offer
stage: checks
status: findings-open
updated: 2026-10-13T11:13:35Z
fix_cycle: 1
---

## Failing checks

- **static_analysis**: [INFO] Scanning for projects...
[INFO] Loaded 24072 auto-discovered prefixes for remote repository central (prefixes-central.txt)
[INFO] 
[INFO] ---------< com.senacor.freighttenders:freight-tenders-backend >---------
[INFO] Building freight-tenders-backend 0.0.1-SNAPSHOT
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] >>> spotbugs:4.10.5.0:check (default-cli) > :spotbugs @ freight-tenders-backend >>>
[INFO] 
[INFO] --- spotbugs:4.10.5.0:spotbugs (spotbugs) @ freight-tenders-backend ---
[INFO] Loaded 74 auto-discovered prefixes for remote repository apache.snapshots (prefixes-apache.snapshots.txt)
[INFO] Done SpotBugs Analysis....
[INFO] Skipping com.github.spotbugs:spotbugs-maven-plugin:4.10.5.0:spotbugs report goal
[INFO] 
[INFO] <<< spotbugs:4.10.5.0:check (default-cli) < :spotbugs @ freight-tenders-backend <<<
[INFO] 
[INFO] 
[INFO] --- spotbugs:4.10.5.0:check (default-cli) @ freight-tenders-backend ---
[INFO] BugInstance size is 1
[INFO] Error size is 0
[INFO] Total bugs: 1
[ERROR] Medium: com.senacor.freighttenders.tender.Tender.award(Offer) may expose internal representation by storing an externally mutable object into Tender.awardedOffer [com.senacor.freighttenders.tender.Tender] At Tender.java:[line 235] EI_EXPOSE_REP2
[INFO] 


To see bug detail using the Spotbugs GUI, use the following command "mvn spotbugs:gui"



[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  9.015 s
[INFO] Finished at: 2026-10-13T11:13:15Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal com.github.spotbugs:spotbugs-maven-plugin:4.10.5.0:check (default-cli) on project freight-tenders-backend: failed with 1 bugs and 0 errors -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
- **test**: > frontend@0.0.0 test
> ng test --watch=false

❯ Building...
✔ Building...
Initial chunk files                         | Names                                    |  Raw size
chunk-GWIEIW76.js                           | -                                        |  75.38 kB | 
chunk-IX2QXSUW.js                           | -                                        |  51.84 kB | 
spec-app-tender-detail-tender-detail.js     | spec-app-tender-detail-tender-detail     |  41.38 kB | 
chunk-OAYIRKBM.js                           | -                                        |  25.54 kB | 
spec-app-tender-overview-tender-overview.js | spec-app-tender-overview-tender-overview |  19.57 kB | 
styles.css                                  | styles                                   |  16.68 kB | 
spec-app-tender-create-tender-create.js     | spec-app-tender-create-tender-create     |  13.94 kB | 
chunk-RSTWSNOR.js                           | -                                        |   4.80 kB | 
spec-app-tender-api.js                      | spec-app-tender-api                      |   4.78 kB | 
spec-app-table-sort.js                      | spec-app-table-sort                      |   4.18 kB | 
spec-app-app.js                             | spec-app-app                             |   3.20 kB | 
spec-app-tender-format.js                   | spec-app-tender-format                   |   3.03 kB | 
init-testbed.js                             | init-testbed                             |   2.27 kB | 
chunk-LGUICGS3.js                           | -                                        |   2.27 kB | 
chunk-FXV4AZXE.js                           | -                                        |   2.10 kB | 
chunk-4IO5JKOM.js                           | -                                        |   1.60 kB | 
chunk-BLMD3KD4.js                           | -                                        |   1.31 kB | 
vitest-mock-patch.js                        | vitest-mock-patch                        | 988 bytes | 
init-compiler.js                            | init-compiler                            | 166 bytes | 

                                            | Initial total                            | 275.04 kB

Application bundle generation complete. [2.455 seconds] - 2026-10-13T11:12:54.262Z


[1m[30m[46m RUN [49m[39m[22m [36mv5.0.3 [39m[90m/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend[39m

 [31m❯[39m [30m[43m frontend [49m[39m src/app/tender-overview/tender-overview.spec.ts [2m([22m[2m33 tests[22m[2m | [22m[31m1 failed[39m[2m)[22m[33m 853[2mms[22m[39m
   [31m❯[39m TenderOverview [2m(33)[22m
     [32m✓[39m should create[32m 88[2mms[22m[39m
     [32m✓[39m shows a German loading message before the response arrives, not an empty-state[32m 18[2mms[22m[39m
     [32m✓[39m lists open and closed tenders under their German headings when the backend returns a mix[32m 54[2mms[22m[39m
     [32m✓[39m shows a German empty-state message for the section with no tenders[32m 29[2mms[22m[39m
     [32m✓[39m links to the create-tender page and to each tender's detail page[32m 26[2mms[22m[39m
     [32m✓[39m shows the city of the origin and destination address in the Von and Nach columns[32m 33[2mms[22m[39m
[31m     [31m×[31m renders the seven column headers in order, in both tables, with no status header or pill[39m[32m 54[2mms[22m[39m
     [32m✓[39m shows pickup date, load line, German vehicle label, deadline and offer count in a row[32m 39[2mms[22m[39m
     [32m✓[39m shows ADR class and temperature range as hints in the Ladung cell, and nothing for a plain tender[32m 17[2mms[22m[39m
     [32m✓[39m shows the temperature range for a reefer tender[32m 16[2mms[22m[39m
     [32m✓[39m shows no second line in the Ladung cell for a plain tender[32m 14[2mms[22m[39m
     [32m✓[39m shows no lowest offer and a count of 0 for a tender without offers[32m 13[2mms[22m[39m
     [32m✓[39m deadline hints [2m(3)[22m
       [32m✓[39m shows "heute" for an open tender whose deadline is today[32m 15[2mms[22m[39m
       [32m✓[39m shows "abgelaufen" for an open tender whose deadline has passed[32m 11[2mms[22m[39m
       [32m✓[39m shows no hint for a closed tender with a deadline today or in the past[32m 16[2mms[22m[39m
     [32m✓[39m sorting by the other columns [2m(5)[22m
       [32m✓[39m sorts by pickupDate ascending and then descending[32m 33[2mms[22m[39m
       [32m✓[39m sorts by weightKg ascending and then descending[32m 24[2mms[22m[39m
       [32m✓[39m sorts by bidDeadline ascending and then descending[32m 18[2mms[22m[39m
       [32m✓[39m sorts by offerCount ascending and then descending[32m 18[2mms[22m[39m
       [32m✓[39m has no sort button on the Fahrzeug header[32m 18[2mms[22m[39m
     [32m✓[39m shows a German error message when the backend is unreachable[32m 6[2mms[22m[39m
     [32m✓[39m shows the page heading and never the raw status enum[32m 29[2mms[22m[39m
     [32m✓[39m orders both tables newest-first with no sort indicator until a column is selected[32m 18[2mms[22m[39m
     [32m✓[39m sorts ascending when a column header is selected and shows the indicator on that column only[32m 22[2mms[22m[39m
     [32m✓[39m reverses to descending when the active column header is selected again[32m 29[2mms[22m[39m
     [32m✓[39m switches to the newly selected column ascending and clears the previous header[32m 30[2mms[22m[39m
     [32m✓[39m sorts each table independently of the other[32m 23[2mms[22m[39m
     [32m✓[39m makes every sort header a real button, so Tab + Enter/Space trigger it like a click[32m 25[2mms[22m[39m
     [32m✓[39m still renders the sortable header row when a table is empty, with the empty message in its body[32m 14[2mms[22m[39m
     [32m✓[39m lists awarded and closed tenders together with a Status column and Zuschlag line[32m 27[2mms[22m[39m
     [32m✓[39m navigates to the tender's detail page when its row is selected anywhere[32m 24[2mms[22m[39m
     [32m✓[39m does not navigate in place when a row is selected with a modifier key held[32m 30[2mms[22m[39m
     [32m✓[39m leaves a click on the row's own link to that link, without navigating a second time[32m 20[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-api.spec.ts [2m([22m[2m10 tests[22m[2m)[22m[32m 46[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/table-sort.spec.ts [2m([22m[2m11 tests[22m[2m)[22m[32m 7[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-format.spec.ts [2m([22m[2m11 tests[22m[2m)[22m[32m 4[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/app.spec.ts [2m([22m[2m3 tests[22m[2m)[22m[32m 40[2mms[22m[39m
 [32m✓[39m [30m[43m frontend [49m[39m src/app/tender-create/tender-create.spec.ts [2m([22m[2m26 tests[22m[2m)[22m[33m 1281[2mms[22m[39m
 [31m❯[39m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts [2m([22m[2m53 tests[22m[2m | [22m[31m12 failed[39m[2m)[22m[33m 1616[2mms[22m[39m
   [31m❯[39m TenderDetail [2m(53)[22m
     [32m✓[39m shows the back link while loading, before the response arrives[32m 150[2mms[22m[39m
     [32m✓[39m shows the back link when the tender cannot be loaded[32m 25[2mms[22m[39m
     [32m✓[39m shows the back link when the route id is not a number[32m 16[2mms[22m[39m
     [32m✓[39m shows the back link as the first element in main for an open tender[32m 81[2mms[22m[39m
     [32m✓[39m shows the back link as the first element in main for a closed tender[32m 62[2mms[22m[39m
     [32m✓[39m navigates to the overview when the back link is clicked[32m 89[2mms[22m[39m
     [32m✓[39m shows a German loading message before the response arrives[32m 14[2mms[22m[39m
     [32m✓[39m shows remarks/offers for an open tender with enabled add-forms, and appends a new remark/offer without reloading[32m 80[2mms[22m[39m
     [32m✓[39m disables the add-forms and shows a German explanation for a closed tender[32m 44[2mms[22m[39m
     [32m✓[39m shows a German not-found/error message when the tender cannot be loaded[32m 11[2mms[22m[39m
     [32m✓[39m shows the route as the page heading and the status as a German pill, never the raw enum[32m 46[2mms[22m[39m
     [32m✓[39m orders remarks and offers newest-first with no sort indicator until a column is selected[32m 47[2mms[22m[39m
     [32m✓[39m sorts remarks ascending when the header is selected, and descending when selected again[32m 57[2mms[22m[39m
     [32m✓[39m sorts offers by amount numerically, not as strings, showing German euro amounts[32m 43[2mms[22m[39m
     [32m✓[39m switches the offers sort to a newly selected column ascending and clears the previous header[32m 54[2mms[22m[39m
     [32m✓[39m sorts the remarks and offers tables independently of each other[32m 55[2mms[22m[39m
     [32m✓[39m makes every sort header a real button, so Tab + Enter/Space trigger it like a click[32m 65[2mms[22m[39m
     [32m✓[39m still renders the sortable header rows when a tender has no remarks or offers, with the empty messages in the table bodies[32m 36[2mms[22m[39m
     [32m✓[39m puts a newly added remark and offer at the top while no column is sorted[32m 55[2mms[22m[39m
     [32m✓[39m puts a newly added remark and offer at their sorted position while a column is sorted[32m 58[2mms[22m[39m
     [32m✓[39m shows the remark error below the field and above the submit button, keeping the typed text[32m 38[2mms[22m[39m
     [32m✓[39m shows the offer error below the fields and above the submit button, keeping the entered values[32m 37[2mms[22m[39m
     [32m✓[39m disables each submit button while its request is in flight and ignores a second submit[32m 43[2mms[22m[39m
     [32m✓[39m places the single closed explanation before both add-forms in DOM order[32m 18[2mms[22m[39m
     [32m✓[39m shows a secondary German close button for an open tender[32m 20[2mms[22m[39m
     [32m✓[39m never shows the close button for a tender that loads closed[32m 17[2mms[22m[39m
     [32m✓[39m closes the tender in place, keeping remarks and offers and disabling the add-forms[32m 110[2mms[22m[39m
     [32m✓[39m disables the close button while the request is in flight and ignores a second click[32m 15[2mms[22m[39m
     [32m✓[39m shows a German error and keeps the tender open when closing fails[32m 24[2mms[22m[39m
     [32m✓[39m shows the summary line with pickup, delivery, vehicle and weight[32m 15[2mms[22m[39m
     [32m✓[39m renders the four shipment data cards in order with every row[32m 15[2mms[22m[39m
     [32m✓[39m shows fallback values for missing pallets, dangerous goods and temperature control[32m 12[2mms[22m[39m
     [32m✓[39m marks an open tender with a past bid deadline as abgelaufen[32m 12[2mms[22m[39m
     [32m✓[39m marks an open tender whose bid deadline is today as heute[32m 12[2mms[22m[39m
     [32m✓[39m shows no deadline hint for a closed tender with a past bid deadline[32m 13[2mms[22m[39m
     [32m✓[39m places the offers section before the remarks section[32m 13[2mms[22m[39m
     [32m✓[39m formats offer amounts and names the amount label in the tender currency[32m 20[2mms[22m[39m
     [32m✓[39m renders six offer columns with a trailing Vergeben column, Hinweis not sortable[32m 16[2mms[22m[39m
     [31m❯[39m awarding an offer [2m(6)[22m
       [32m✓[39m offers Vergeben only for non-expired offers of an open tender[32m 16[2mms[22m[39m
       [32m✓[39m offers no award actions on closed tenders[32m 14[2mms[22m[39m
       [32m✓[39m confirms in place for one row only and cancels without a request[32m 20[2mms[22m[39m
[31m       [31m×[31m disables the buttons while the request is in flight[39m[32m 21[2mms[22m[39m
[31m       [31m×[31m shows a German alert and keeps the tender open when awarding fails[39m[32m 1[2mms[22m[39m
[31m       [31m×[31m updates the page in place after a successful award[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m sorts offers by delivery date and validity date in both directions[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m shows the late-delivery and expired hints only where they apply[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m shows the note of an offer[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m shows German errors under invalid touched offer fields[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m disables the offer form with a notice when the bid deadline has passed, keeping remarks enabled[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m shows only the closed explanation for a closed tender past its deadline[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m keeps the entered values and shows the offer error when saving fails with 409[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m shows no summary line or data cards while loading[39m[32m 0[2mms[22m[39m
[31m     [31m×[31m shows no summary line or data cards when the tender cannot be loaded[39m[32m 0[2mms[22m[39m

[2m Test Files [22m [1m[31m2 failed[39m[22m[2m | [22m[1m[32m5 passed[39m[22m[90m (7)[39m
[2m      Tests [22m [1m[31m13 failed[39m[22m[2m | [22m[1m[32m134 passed[39m[22m[90m (147)[39m
[2m   Start at [22m 11:12:54
[2m   Duration [22m 3.35s[2m (environment 48%, tests 34%, setup 8%, import 6%, transform 5%)[22m


::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > awarding an offer > disables the buttons while the request is in flight,line=852,column=28::Error: Expected one matching request for criteria "Match URL: /api/tenders/1/offers/20/award", found none. Requests received are: POST /api/tenders/1/offers/21/award.%0A ❯ HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:112:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:852:28%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > awarding an offer > disables the buttons while the request is in flight,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > awarding an offer > shows a German alert and keeps the tender open when awarding fails,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > awarding an offer > shows a German alert and keeps the tender open when awarding fails,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > awarding an offer > updates the page in place after a successful award,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > awarding an offer > updates the page in place after a successful award,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > sorts offers by delivery date and validity date in both directions,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > sorts offers by delivery date and validity date in both directions,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows the late-delivery and expired hints only where they apply,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows the late-delivery and expired hints only where they apply,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows the note of an offer,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows the note of an offer,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows German errors under invalid touched offer fields,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows German errors under invalid touched offer fields,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > disables the offer form with a notice when the bid deadline has passed%2C keeping remarks enabled,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > disables the offer form with a notice when the bid deadline has passed%2C keeping remarks enabled,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows only the closed explanation for a closed tender past its deadline,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows only the closed explanation for a closed tender past its deadline,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > keeps the entered values and shows the offer error when saving fails with 409,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > keeps the entered values and shows the offer error when saving fails with 409,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows no summary line or data cards while loading,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows no summary line or data cards while loading,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows no summary line or data cards when the tender cannot be loaded,line=105,column=19::Error: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.%0A ❯ TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:839:13%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:596:10%0A ❯ TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:343:33%0A ❯ src/app/tender-detail/tender-detail.spec.ts:105:19%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts,title=[frontend] src/app/tender-detail/tender-detail.spec.ts > TenderDetail > shows no summary line or data cards when the tender cannot be loaded,line=120,column=14::Error: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award%0A ❯ HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:147:13%0A ❯ src/app/tender-detail/tender-detail.spec.ts:120:14%0A%0A

::error file=/home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/frontend/src/app/tender-overview/tender-overview.spec.ts,title=[frontend] src/app/tender-overview/tender-overview.spec.ts > TenderOverview > renders the seven column headers in order%2C in both tables%2C with no status header or pill,line=186,column=23::AssertionError: expected [ 'Von', 'Nach', 'Abholung', …(5) ] to deeply equal [ 'Von', 'Nach', 'Abholung', …(4) ]%0A%0A- Expected%0A+ Received%0A%0A@@ -4,6 +4,7 @@%0A    "Abholung",%0A    "Ladung",%0A    "Fahrzeug",%0A    "Angebotsfrist",%0A    "Angebote",%0A+   "Status",%0A  ]%0A%0A ❯ src/app/tender-overview/tender-overview.spec.ts:186:23%0A%0A
[90mstderr[2m | src/app/tender-detail/tender-detail.spec.ts[2m > [22m[2mTenderDetail[2m > [22m[2mshows remarks/offers for an open tender with enabled add-forms, and appends a new remark/offer without reloading
[22m[39mNG0406: This instance of the `ApplicationRef` has already been destroyed.
NG0406: This instance of the `ApplicationRef` has already been destroyed.
NG0406: This instance of the `ApplicationRef` has already been destroyed.


[31m⎯⎯⎯⎯⎯⎯[39m[1m[41m Failed Tests 13 [49m[22m[31m⎯⎯⎯⎯⎯⎯⎯[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mawarding an offer[2m > [22mdisables the buttons while the request is in flight
[31m[1mError[22m: Expected one matching request for criteria "Match URL: /api/tenders/1/offers/20/award", found none. Requests received are: POST /api/tenders/1/offers/21/award.[39m
[90m [2m❯[22m HttpClientTestingBackend.expectOne ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m112:13[22m[39m
[36m [2m❯[22m src/app/tender-detail/tender-detail.spec.ts:[2m852:28[22m[39m
    [90m850|[39m       click(element, 'award-confirm');
    [90m851|[39m
    [90m852|[39m       const req = httpMock.expectOne('/api/tenders/1/offers/20/award');
    [90m   |[39m                            [31m^[39m
    [90m853|[39m       expect(
    [90m854|[39m         element.querySelector<HTMLButtonElement>('[data-testid="award-…

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/25]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mawarding an offer[2m > [22mdisables the buttons while the request is in flight
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mawarding an offer[2m > [22mshows a German alert and keeps the tender open when awarding fails
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mawarding an offer[2m > [22mupdates the page in place after a successful award
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22msorts offers by delivery date and validity date in both directions
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows the late-delivery and expired hints only where they apply
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows the note of an offer
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows German errors under invalid touched offer fields
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mdisables the offer form with a notice when the bid deadline has passed, keeping remarks enabled
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows only the closed explanation for a closed tender past its deadline
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mkeeps the entered values and shows the offer error when saving fails with 409
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows no summary line or data cards while loading
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows no summary line or data cards when the tender cannot be loaded
[31m[1mError[22m: Expected no open requests, found 1: POST /api/tenders/1/offers/21/award[39m
[90m [2m❯[22m HttpClientTestingBackend.verify ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/common/http/testing/src/backend.ts:[2m147:13[22m[39m
[36m [2m❯[22m src/app/tender-detail/tender-detail.spec.ts:[2m120:14[22m[39m
    [90m118|[39m
    [90m119|[39m   afterEach(() => {
    [90m120|[39m     httpMock.verify();
    [90m   |[39m              [31m^[39m
    [90m121|[39m   });
    [90m122|[39m

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/25]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mawarding an offer[2m > [22mshows a German alert and keeps the tender open when awarding fails
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mawarding an offer[2m > [22mupdates the page in place after a successful award
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22msorts offers by delivery date and validity date in both directions
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows the late-delivery and expired hints only where they apply
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows the note of an offer
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows German errors under invalid touched offer fields
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mdisables the offer form with a notice when the bid deadline has passed, keeping remarks enabled
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows only the closed explanation for a closed tender past its deadline
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mkeeps the entered values and shows the offer error when saving fails with 409
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows no summary line or data cards while loading
[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-detail/tender-detail.spec.ts[2m > [22mTenderDetail[2m > [22mshows no summary line or data cards when the tender cannot be loaded
[31m[1mError[22m: Cannot configure the test module when the test module has already been instantiated. Make sure you are not using `inject` before `TestBed.configureTestingModule`.[39m
[90m [2m❯[22m TestBedImpl.assertNotInstantiated ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:[2m839:13[22m[39m
[90m [2m❯[22m TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:[2m596:10[22m[39m
[90m [2m❯[22m TestBedImpl.configureTestingModule ../k8-fastbuild-ST-fdfa778d11ba/bin/packages/core/testing/src/test_bed.ts:[2m343:33[22m[39m
[36m [2m❯[22m src/app/tender-detail/tender-detail.spec.ts:[2m105:19[22m[39m
    [90m103|[39m
    [90m104|[39m   beforeEach(async () => {
    [90m105|[39m     await TestBed.configureTestingModule({
    [90m   |[39m                   [31m^[39m
    [90m106|[39m       providers: [
    [90m107|[39m         provideHttpClient(),

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/25]⎯[22m[39m

[41m[1m FAIL [22m[49m [30m[43m frontend [49m[39m src/app/tender-overview/tender-overview.spec.ts[2m > [22mTenderOverview[2m > [22mrenders the seven column headers in order, in both tables, with no status header or pill
[31m[1mAssertionError[22m: expected [ 'Von', 'Nach', 'Abholung', …(5) ] to deeply equal [ 'Von', 'Nach', 'Abholung', …(4) ][39m

[32m- Expected[39m
[31m+ Received[39m

[33m@@ -4,6 +4,7 @@[39m
[2m    "Abholung",[22m
[2m    "Ladung",[22m
[2m    "Fahrzeug",[22m
[2m    "Angebotsfrist",[22m
[2m    "Angebote",[22m
[31m+   "Status",[39m
[2m  ][22m

[36m [2m❯[22m src/app/tender-overview/tender-overview.spec.ts:[2m186:23[22m[39m
    [90m184|[39m         compiled.querySelectorAll(`[data-testid="${table}"] thead th`),
    [90m185|[39m       ).map((th) => th.textContent?.trim());
    [90m186|[39m       expect(headers).toEqual([
    [90m   |[39m                       [31m^[39m
    [90m187|[39m         'Von',
    [90m188|[39m         'Nach',

[31m[2m⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/25]⎯[22m[39m
