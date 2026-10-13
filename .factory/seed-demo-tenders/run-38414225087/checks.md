---
schema_version: 1
story_slug: seed-demo-tenders
stage: checks
status: findings-open
updated: 2026-10-13T14:38:23Z
fix_cycle: 1
---

## Failing checks

- **static_analysis**: [INFO] Scanning for projects...
[INFO] Loaded 24073 auto-discovered prefixes for remote repository central (prefixes-central.txt)
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
[ERROR] Medium: new com.senacor.freighttenders.tender.DemoDataSeeder(TenderRepository, TenderService, Clock) may expose internal representation by storing an externally mutable object into DemoDataSeeder.tenderService [com.senacor.freighttenders.tender.DemoDataSeeder] At DemoDataSeeder.java:[line 32] EI_EXPOSE_REP2
[INFO] 


To see bug detail using the Spotbugs GUI, use the following command "mvn spotbugs:gui"



[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  8.777 s
[INFO] Finished at: 2026-10-13T14:37:32Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal com.github.spotbugs:spotbugs-maven-plugin:4.10.5.0:check (default-cli) on project freight-tenders-backend: failed with 1 bugs and 0 errors -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
- **test**: [INFO] Scanning for projects...
[INFO] Loaded 24073 auto-discovered prefixes for remote repository central (prefixes-central.txt)
[INFO] 
[INFO] ---------< com.senacor.freighttenders:freight-tenders-backend >---------
[INFO] Building freight-tenders-backend 0.0.1-SNAPSHOT
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- resources:3.5.0:resources (default-resources) @ freight-tenders-backend ---
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] Copying 0 resource from src/main/resources to target/classes
[INFO] 
[INFO] --- compiler:3.15.0:compile (default-compile) @ freight-tenders-backend ---
[INFO] Loaded 74 auto-discovered prefixes for remote repository apache.snapshots (prefixes-apache.snapshots.txt)
[INFO] Nothing to compile - all classes are up to date.
[INFO] 
[INFO] --- resources:3.5.0:testResources (default-testResources) @ freight-tenders-backend ---
[INFO] skip non existing resourceDirectory /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/resources
[INFO] 
[INFO] --- compiler:3.15.0:testCompile (default-testCompile) @ freight-tenders-backend ---
[INFO] Recompiling the module because of changed source code.
[INFO] Compiling 11 source files with javac [debug parameters release 25] to target/test-classes
[INFO] -------------------------------------------------------------
[ERROR] COMPILATION ERROR : 
[INFO] -------------------------------------------------------------
[ERROR] /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:[11,63] package org.springframework.boot.test.autoconfigure.web.servlet does not exist
[ERROR] /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:[21,4] cannot find symbol
  symbol:   class AutoConfigureMockMvc
  location: class com.senacor.freighttenders.tender.DemoProfileGatingTest
[ERROR] /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:[41,4] cannot find symbol
  symbol:   class AutoConfigureMockMvc
  location: class com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] 3 errors 
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  3.691 s
[INFO] Finished at: 2026-10-13T14:37:14Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.15.0:testCompile (default-testCompile) on project freight-tenders-backend: Compilation failure: Compilation failure: 
[ERROR] /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:[11,63] package org.springframework.boot.test.autoconfigure.web.servlet does not exist
[ERROR] /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:[21,4] cannot find symbol
[ERROR]   symbol:   class AutoConfigureMockMvc
[ERROR]   location: class com.senacor.freighttenders.tender.DemoProfileGatingTest
[ERROR] /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:[41,4] cannot find symbol
[ERROR]   symbol:   class AutoConfigureMockMvc
[ERROR]   location: class com.senacor.freighttenders.tender.DemoProfileGatingTest
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
