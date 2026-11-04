---
schema_version: 1
story_slug: edit-open-tender
stage: checks
status: findings-open
updated: 2026-11-04T08:09:21Z
fix_cycle: 1
---

## Failing checks

- **lint**: [INFO] Scanning for projects...
[INFO] Loaded 24360 auto-discovered prefixes for remote repository central (prefixes-central.txt)
[INFO] 
[INFO] ---------< com.senacor.freighttenders:freight-tenders-backend >---------
[INFO] Building freight-tenders-backend 0.0.1-SNAPSHOT
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- spotless:3.10.4:check (default-cli) @ freight-tenders-backend ---
[INFO] Index file does not exist. Fallback to an empty index
[INFO] Spotless.Java is keeping 47 files clean - 5 needs changes to be clean, 42 were already clean, 0 were skipped because caching determined they were already clean
[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.978 s
[INFO] Finished at: 2026-11-04T08:08:32Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal com.diffplug.spotless:spotless-maven-plugin:3.10.4:check (default-cli) on project freight-tenders-backend: The following files had format violations:
[ERROR]     src/main/java/com/senacor/freighttenders/tender/TenderService.java
[ERROR]         @@ -120,8 +120,7 @@
[ERROR]          ····}
[ERROR]          ····addIfDifferent(changed,·"palletCount",·tender.getPalletCount(),·request.palletCount());
[ERROR]          ····addIfDifferent(changed,·"equipmentType",·tender.getEquipmentType(),·request.equipmentType());
[ERROR]         -····addIfDifferent(
[ERROR]         -········changed,·"dangerousGoods",·tender.isDangerousGoods(),·request.dangerousGoods());
[ERROR]         +····addIfDifferent(changed,·"dangerousGoods",·tender.isDangerousGoods(),·request.dangerousGoods());
[ERROR]          ····addIfDifferent(changed,·"adrClass",·tender.getAdrClass(),·request.adrClass());
[ERROR]          ····addIfDifferent(
[ERROR]          ········changed,
[ERROR]     src/main/java/com/senacor/freighttenders/tender/CreateTenderRequestValidator.java
[ERROR]         @@ -84,16 +84,13 @@
[ERROR]          
[ERROR]          ····if·(Boolean.TRUE.equals(request.temperatureControlled()))·{
[ERROR]          ······if·(request.equipmentType()·!=·null·&&·request.equipmentType()·!=·EquipmentType.REEFER)·{
[ERROR]         -········violations.add(
[ERROR]         -············new·Violation("equipmentType",·"must·be·REEFER·when·temperatureControlled"));
[ERROR]         +········violations.add(new·Violation("equipmentType",·"must·be·REEFER·when·temperatureControlled"));
[ERROR]          ······}
[ERROR]          ······if·(request.temperatureMinC()·==·null)·{
[ERROR]         -········violations.add(
[ERROR]         -············new·Violation("temperatureMinC",·"is·required·when·temperatureControlled"));
[ERROR]         +········violations.add(new·Violation("temperatureMinC",·"is·required·when·temperatureControlled"));
[ERROR]          ······}
[ERROR]          ······if·(request.temperatureMaxC()·==·null)·{
[ERROR]         -········violations.add(
[ERROR]         -············new·Violation("temperatureMaxC",·"is·required·when·temperatureControlled"));
[ERROR]         +········violations.add(new·Violation("temperatureMaxC",·"is·required·when·temperatureControlled"));
[ERROR]          ······}
[ERROR]          ······if·(request.temperatureMinC()·!=·null
[ERROR]          ··········&&·request.temperatureMaxC()·!=·null
[ERROR]     src/test/java/com/senacor/freighttenders/tender/TenderControllerTest.java
[ERROR]         @@ -98,7 +98,9 @@
[ERROR]          ····given(tenderService.updateTender(eq(1L),·any(CreateTenderRequest.class)))
[ERROR]          ········.willThrow(
[ERROR]          ············new·InvalidTenderException(
[ERROR]         -················List.of(new·TenderExceptionHandler.Violation("bidDeadline",·"must·not·be·in·the·past"))));
[ERROR]         +················List.of(
[ERROR]         +····················new·TenderExceptionHandler.Violation(
[ERROR]         +························"bidDeadline",·"must·not·be·in·the·past"))));
[ERROR]          ····given(tenderService.updateTender(eq(2L),·any(CreateTenderRequest.class)))
[ERROR]          ········.willThrow(new·TenderLockedFieldsException(2L,·List.of("commodity")));
[ERROR]          ····given(tenderService.updateTender(eq(3L),·any(CreateTenderRequest.class)))
[ERROR]     src/test/java/com/senacor/freighttenders/tender/TenderServiceTest.java
[ERROR]         @@ -167,7 +167,8 @@
[ERROR]          ········.willAnswer(invocation·->·invocation.getArgument(0));
[ERROR]          ····Clock·deadlineDay·=
[ERROR]          ········Clock.fixed(Instant.parse("2026-10-16T08:00:00Z"),·ZoneId.of("Europe/Berlin"));
[ERROR]         -····TenderService·service·=·new·TenderService(tenderRepository,·deadlineDay,·TenderFixtures.validator(deadlineDay));
[ERROR]     ... (5 more lines that didn't fit)
[ERROR] Violations also present in:
[ERROR]     src/test/java/com/senacor/freighttenders/tender/ValidatorTestConfiguration.java
[ERROR] Run 'mvn spotless:apply' to fix these violations.
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
WARNING: sun.misc.Unsafe::staticFieldBase has been called by com.diffplug.spotless.java.ModuleHelper (file:/home/runner/.m2/repository/com/diffplug/spotless/spotless-lib/4.10.4/spotless-lib-4.10.4.jar)
WARNING: Please consider reporting this to the maintainers of class com.diffplug.spotless.java.ModuleHelper
WARNING: sun.misc.Unsafe::staticFieldBase will be removed in a future release
- **test**: [INFO] Scanning for projects...
[INFO] Loaded 24360 auto-discovered prefixes for remote repository central (prefixes-central.txt)
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
[INFO] Loaded 64 auto-discovered prefixes for remote repository apache.snapshots (prefixes-apache.snapshots.txt)
[INFO] Nothing to compile - all classes are up to date.
[INFO] 
[INFO] --- resources:3.5.0:testResources (default-testResources) @ freight-tenders-backend ---
[INFO] skip non existing resourceDirectory /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/resources
[INFO] 
[INFO] --- compiler:3.15.0:testCompile (default-testCompile) @ freight-tenders-backend ---
[INFO] Recompiling the module because of changed source code.
[INFO] Compiling 12 source files with javac [debug parameters release 25] to target/test-classes
[INFO] 
[INFO] --- surefire:3.5.6:test (default-test) @ freight-tenders-backend ---
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.senacor.freighttenders.tender.TenderServiceTest
Mockito is currently self-attaching to enable the inline-mock-maker. This will no longer work in future releases of the JDK. Please add Mockito as an agent to your build as described in Mockito's documentation: https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html#0.3
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
WARNING: A Java agent has been loaded dynamically (/home/runner/.m2/repository/net/bytebuddy/byte-buddy-agent/1.18.11/byte-buddy-agent-1.18.11.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
08:08:21.889 [main] INFO org.hibernate.validator.internal.util.Version -- HV000001: Hibernate Validator 9.1.3.Final
[ERROR] Tests run: 27, Failures: 0, Errors: 1, Skipped: 0, Time elapsed: 1.622 s <<< FAILURE! -- in com.senacor.freighttenders.tender.TenderServiceTest
[ERROR] com.senacor.freighttenders.tender.TenderServiceTest.updateTenderWithOffersAllowsDeliveryDateAndBidDeadlineAndIgnoresDecimalScale -- Time elapsed: 0.041 s <<< ERROR!
com.senacor.freighttenders.tender.InvalidTenderException: Request validation failed
	at com.senacor.freighttenders.tender.TenderService.validateUpdate(TenderService.java:106)
	at com.senacor.freighttenders.tender.TenderService.updateTender(TenderService.java:63)
	at com.senacor.freighttenders.tender.TenderServiceTest.updateTenderWithOffersAllowsDeliveryDateAndBidDeadlineAndIgnoresDecimalScale(TenderServiceTest.java:490)

[INFO] Running com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Running com.senacor.freighttenders.tender.TenderServicePersistenceTest
08:08:22.528 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
08:08:22.709 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest
08:08:22.710 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
08:08:22.724 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:23.075Z  INFO 2596 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Starting TenderServicePersistenceTest using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:23.077Z  INFO 2596 --- [           main] c.s.f.t.TenderServicePersistenceTest     : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:08:23.379Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:08:23.422Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 37 ms. Found 1 JPA repository interface.
2026-11-04T08:08:23.462Z  INFO 2596 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-11-04T08:08:23.562Z  INFO 2596 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:7294c7a3-c1ca-4447-8a8e-c91bdba9c017;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-11-04T08:08:23.791Z  INFO 2596 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:08:23.834Z  INFO 2596 --- [           main] org.hibernate.orm.core                   : HHH000001: Hibernate ORM core version 7.4.5.Final
2026-11-04T08:08:24.029Z  INFO 2596 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:08:24.092Z  INFO 2596 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:7294c7a3-c1ca-4447-8a8e-c91bdba9c017]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 7294C7A3-C1CA-4447-8A8E-C91BDBA9C017/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:08:24.635Z  INFO 2596 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-11-04T08:08:24.683Z  INFO 2596 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:08:24.741Z  INFO 2596 --- [           main] o.s.d.j.r.query.QueryEnhancerFactories   : Hibernate is in classpath; If applicable, HQL parser will be used.
2026-11-04T08:08:24.901Z  INFO 2596 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Started TenderServicePersistenceTest in 2.133 seconds (process running for 4.789)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
Hibernate: select o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until from offer o1_0 where o1_0.tender_id=?
Hibernate: update tender set adr_class=?,awarded_offer_id=?,bid_deadline=?,commodity=?,currency=?,dangerous_goods=?,delivery_date=?,destination_country=?,destination_postal_code=?,destination_city=?,equipment_type=?,loading_meters=?,origin_country=?,origin_postal_code=?,origin_city=?,pallet_count=?,pickup_date=?,status=?,temperature_controlled=?,temperature_maxc=?,temperature_minc=?,weight_kg=? where id=?
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
Hibernate: select o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until from offer o1_0 where o1_0.tender_id=?
Hibernate: update tender set adr_class=?,awarded_offer_id=?,bid_deadline=?,commodity=?,currency=?,dangerous_goods=?,delivery_date=?,destination_country=?,destination_postal_code=?,destination_city=?,equipment_type=?,loading_meters=?,origin_country=?,origin_postal_code=?,origin_city=?,pallet_count=?,pickup_date=?,status=?,temperature_controlled=?,temperature_maxc=?,temperature_minc=?,weight_kg=? where id=?
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until from offer o1_0 where o1_0.tender_id=?
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.701 s -- in com.senacor.freighttenders.tender.TenderServicePersistenceTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-11-04T08:08:25.184Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:25.186Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-11-04T08:08:25.189Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:25.189Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:25.191Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:25.239Z  INFO 2596 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Starting DemoProfileGatingTest.WithDemoProfile using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:25.239Z  INFO 2596 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : The following 1 profile is active: "demo"
2026-11-04T08:08:25.433Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:08:25.441Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 6 ms. Found 1 JPA repository interface.
2026-11-04T08:08:25.544Z  INFO 2596 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:08:25.557Z  INFO 2596 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:08:25.558Z  INFO 2596 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2026-11-04T08:08:25.566Z  INFO 2596 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection conn8: url=jdbc:h2:mem:gating-with-demo user=SA
2026-11-04T08:08:25.567Z  INFO 2596 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2026-11-04T08:08:25.575Z  INFO 2596 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:gating-with-demo]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: GATING-WITH-DEMO/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:08:25.622Z  INFO 2596 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-11-04T08:08:25.633Z  INFO 2596 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:08:25.720Z  WARN 2596 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-11-04T08:08:26.027Z  INFO 2596 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:08:26.027Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:08:26.029Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-11-04T08:08:26.042Z  INFO 2596 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Started DemoProfileGatingTest.WithDemoProfile in 0.841 seconds (process running for 5.931)
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.190 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-11-04T08:08:26.374Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:26.376Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-11-04T08:08:26.377Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:26.377Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:26.378Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:26.397Z  INFO 2596 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Starting DemoProfileGatingTest.WithoutDemoProfile using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:26.397Z  INFO 2596 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:08:26.488Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:08:26.494Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 4 ms. Found 1 JPA repository interface.
2026-11-04T08:08:26.546Z  INFO 2596 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:08:26.558Z  INFO 2596 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:08:26.559Z  INFO 2596 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Starting...
2026-11-04T08:08:26.561Z  INFO 2596 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-2 - Added connection conn18: url=jdbc:h2:mem:gating-without-demo user=SA
2026-11-04T08:08:26.561Z  INFO 2596 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Start completed.
2026-11-04T08:08:26.562Z  INFO 2596 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:gating-without-demo]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: GATING-WITHOUT-DEMO/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:08:26.605Z  INFO 2596 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-11-04T08:08:26.613Z  INFO 2596 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:08:26.646Z  WARN 2596 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-11-04T08:08:26.697Z  INFO 2596 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:08:26.697Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:08:26.698Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-11-04T08:08:26.703Z  INFO 2596 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Started DemoProfileGatingTest.WithoutDemoProfile in 0.322 seconds (process running for 6.592)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.349 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.542 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.TenderRepositoryTest
2026-11-04T08:08:26.725Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:26.738Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest
2026-11-04T08:08:26.738Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:26.745Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:26.760Z  INFO 2596 --- [           main] c.s.f.tender.TenderRepositoryTest        : Starting TenderRepositoryTest using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:26.760Z  INFO 2596 --- [           main] c.s.f.tender.TenderRepositoryTest        : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:08:26.834Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:08:26.858Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 19 ms. Found 1 JPA repository interface.
2026-11-04T08:08:26.871Z  INFO 2596 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-11-04T08:08:26.879Z  INFO 2596 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:f66cadf5-8842-472b-b4db-6133a4518a83;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-11-04T08:08:26.891Z  INFO 2596 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:08:26.906Z  INFO 2596 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:08:26.907Z  INFO 2596 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:f66cadf5-8842-472b-b4db-6133a4518a83]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: F66CADF5-8842-472B-B4DB-6133A4518A83/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:08:26.958Z  INFO 2596 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-11-04T08:08:26.966Z  INFO 2596 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:08:26.994Z  INFO 2596 --- [           main] c.s.f.tender.TenderRepositoryTest        : Started TenderRepositoryTest in 0.246 seconds (process running for 6.882)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id where t1_0.status=?
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until from offer o1_0 where o1_0.tender_id=?
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until from offer o1_0 where o1_0.tender_id=?
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: select t1_0.id,t1_0.adr_class,ao1_0.id,ao1_0.amount,ao1_0.delivery_date,ao1_0.note,ao1_0.supplier_name,t2_0.id,t2_0.adr_class,t2_0.awarded_offer_id,t2_0.bid_deadline,t2_0.commodity,t2_0.currency,t2_0.dangerous_goods,t2_0.delivery_date,t2_0.destination_country,t2_0.destination_postal_code,t2_0.destination_city,t2_0.equipment_type,t2_0.loading_meters,t2_0.origin_country,t2_0.origin_postal_code,t2_0.origin_city,t2_0.pallet_count,t2_0.pickup_date,t2_0.status,t2_0.temperature_controlled,t2_0.temperature_maxc,t2_0.temperature_minc,t2_0.weight_kg,ao1_0.valid_until,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer ao1_0 on ao1_0.id=t1_0.awarded_offer_id left join tender t2_0 on t2_0.id=ao1_0.tender_id where t1_0.id=?
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.370 s -- in com.senacor.freighttenders.tender.TenderRepositoryTest
[INFO] Running com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-11-04T08:08:27.098Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:27.107Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-11-04T08:08:27.107Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:27.110Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:27.160Z  INFO 2596 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Starting TenderCreateValidationTest using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:27.161Z  INFO 2596 --- [           main] c.s.f.tender.TenderCreateValidationTest  : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:08:27.424Z  INFO 2596 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:08:27.425Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:08:27.426Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-11-04T08:08:27.434Z  INFO 2596 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Started TenderCreateValidationTest in 0.296 seconds (process running for 7.323)
[INFO] Tests run: 58, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.851 s -- in com.senacor.freighttenders.tender.TenderCreateValidationTest
[INFO] Running com.senacor.freighttenders.tender.TenderControllerTest
2026-11-04T08:08:27.951Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:27.956Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
2026-11-04T08:08:27.957Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:27.960Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Tests run: 32, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.300 s -- in com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Running com.senacor.freighttenders.tender.DemoDataSeederTest
2026-11-04T08:08:28.253Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:28.260Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest
2026-11-04T08:08:28.261Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:28.267Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:28.292Z  INFO 2596 --- [           main] c.s.f.tender.DemoDataSeederTest          : Starting DemoDataSeederTest using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:28.292Z  INFO 2596 --- [           main] c.s.f.tender.DemoDataSeederTest          : The following 1 profile is active: "demo"
2026-11-04T08:08:28.380Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:08:28.388Z  INFO 2596 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 6 ms. Found 1 JPA repository interface.
2026-11-04T08:08:28.399Z  INFO 2596 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-11-04T08:08:28.410Z  INFO 2596 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:d21d998d-52d3-4cff-8fd1-f557295a1caf;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-11-04T08:08:28.454Z  INFO 2596 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:08:28.480Z  INFO 2596 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:08:28.485Z  INFO 2596 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:d21d998d-52d3-4cff-8fd1-f557295a1caf]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: D21D998D-52D3-4CFF-8FD1-F557295A1CAF/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:08:28.551Z  INFO 2596 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-11-04T08:08:28.559Z  INFO 2596 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:08:28.609Z  INFO 2596 --- [           main] c.s.f.tender.DemoDataSeederTest          : Started DemoDataSeederTest in 0.339 seconds (process running for 8.497)
Hibernate: select count(*) from tender t1_0
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: insert into tender (adr_class,awarded_offer_id,bid_deadline,commodity,currency,dangerous_goods,delivery_date,destination_country,destination_postal_code,destination_city,equipment_type,loading_meters,origin_country,origin_postal_code,origin_city,pallet_count,pickup_date,status,temperature_controlled,temperature_maxc,temperature_minc,weight_kg,id) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,default)
Hibernate: insert into offer (amount,delivery_date,note,supplier_name,tender_id,valid_until,id) values (?,?,?,?,?,?,default)
Hibernate: insert into remark (tender_id,text,id) values (?,?,default)
Hibernate: update tender set adr_class=?,awarded_offer_id=?,bid_deadline=?,commodity=?,currency=?,dangerous_goods=?,delivery_date=?,destination_country=?,destination_postal_code=?,destination_city=?,equipment_type=?,loading_meters=?,origin_country=?,origin_postal_code=?,origin_city=?,pallet_count=?,pickup_date=?,status=?,temperature_controlled=?,temperature_maxc=?,temperature_minc=?,weight_kg=? where id=?
Hibernate: update tender set adr_class=?,awarded_offer_id=?,bid_deadline=?,commodity=?,currency=?,dangerous_goods=?,delivery_date=?,destination_country=?,destination_postal_code=?,destination_city=?,equipment_type=?,loading_meters=?,origin_country=?,origin_postal_code=?,origin_city=?,pallet_count=?,pickup_date=?,status=?,temperature_controlled=?,temperature_maxc=?,temperature_minc=?,weight_kg=? where id=?
Hibernate: select count(*) from tender t1_0
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select count(*) from tender t1_0
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
Hibernate: select count(*) from tender t1_0
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
Hibernate: select count(*) from tender t1_0
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
Hibernate: select count(*) from tender t1_0
Hibernate: select count(*) from tender t1_0
Hibernate: select count(*) from tender t1_0
Hibernate: select count(*) from tender t1_0
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select r1_0.tender_id,r1_0.id,r1_0.text from remark r1_0 where r1_0.tender_id=?
Hibernate: select count(*) from tender t1_0
Hibernate: select t1_0.id,t1_0.adr_class,t1_0.awarded_offer_id,t1_0.bid_deadline,t1_0.commodity,t1_0.currency,t1_0.dangerous_goods,t1_0.delivery_date,t1_0.destination_country,t1_0.destination_postal_code,t1_0.destination_city,t1_0.equipment_type,t1_0.loading_meters,o1_0.tender_id,o1_0.id,o1_0.amount,o1_0.delivery_date,o1_0.note,o1_0.supplier_name,o1_0.valid_until,t1_0.origin_country,t1_0.origin_postal_code,t1_0.origin_city,t1_0.pallet_count,t1_0.pickup_date,t1_0.status,t1_0.temperature_controlled,t1_0.temperature_maxc,t1_0.temperature_minc,t1_0.weight_kg from tender t1_0 left join offer o1_0 on t1_0.id=o1_0.tender_id
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.493 s -- in com.senacor.freighttenders.tender.DemoDataSeederTest
[INFO] Running com.senacor.freighttenders.health.HealthControllerTest
2026-11-04T08:08:28.747Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:28.756Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest
2026-11-04T08:08:28.757Z  INFO 2596 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:08:28.760Z  INFO 2596 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:08:28.776Z  INFO 2596 --- [           main] c.s.f.health.HealthControllerTest        : Starting HealthControllerTest using Java 25.0.5 with PID 2596 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:08:28.777Z  INFO 2596 --- [           main] c.s.f.health.HealthControllerTest        : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:08:28.902Z  INFO 2596 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:08:28.903Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:08:28.903Z  INFO 2596 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 0 ms
2026-11-04T08:08:28.908Z  INFO 2596 --- [           main] c.s.f.health.HealthControllerTest        : Started HealthControllerTest in 0.145 seconds (process running for 8.796)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.177 s -- in com.senacor.freighttenders.health.HealthControllerTest
[INFO] 
[INFO] Results:
[INFO] 
[ERROR] Errors: 
[ERROR]   TenderServiceTest.updateTenderWithOffersAllowsDeliveryDateAndBidDeadlineAndIgnoresDecimalScale:490 » InvalidTender Request validation failed
[INFO] 
[ERROR] Tests run: 138, Failures: 0, Errors: 1, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  12.125 s
[INFO] Finished at: 2026-11-04T08:08:28Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:3.5.6:test (default-test) on project freight-tenders-backend: 
[ERROR] 
[ERROR] See /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/target/surefire-reports for the individual test results.
[ERROR] See dump files (if any exist) [date].dump, [date]-jvmRun[N].dump and [date].dumpstream.
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
