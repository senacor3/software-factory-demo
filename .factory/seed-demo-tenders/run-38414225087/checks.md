---
schema_version: 1
story_slug: seed-demo-tenders
stage: checks
status: unresolved-after-cap
updated: 2026-10-13T14:40:14Z
fix_cycle: 2
---

## Failing checks

- **test**: [INFO] Scanning for projects...
[INFO] Loaded 24074 auto-discovered prefixes for remote repository central (prefixes-central.txt)
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
[INFO] 
[INFO] --- surefire:3.5.6:test (default-test) @ freight-tenders-backend ---
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.senacor.freighttenders.tender.DemoDataSeederTest
14:40:04.887 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
14:40:05.151 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest
14:40:05.153 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
14:40:05.174 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:05.562Z  INFO 3588 --- [           main] c.s.f.tender.DemoDataSeederTest          : Starting DemoDataSeederTest using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:05.564Z  INFO 3588 --- [           main] c.s.f.tender.DemoDataSeederTest          : The following 1 profile is active: "demo"
2026-10-13T14:40:05.973Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:40:06.040Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 50 ms. Found 1 JPA repository interface.
2026-10-13T14:40:06.091Z  INFO 3588 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-10-13T14:40:06.244Z  INFO 3588 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:33575e24-af0f-432b-8539-157858d8f4d9;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-10-13T14:40:06.519Z  INFO 3588 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:40:06.570Z  INFO 3588 --- [           main] org.hibernate.orm.core                   : HHH000001: Hibernate ORM core version 7.4.5.Final
2026-10-13T14:40:06.943Z  INFO 3588 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:40:07.011Z  INFO 3588 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:33575e24-af0f-432b-8539-157858d8f4d9]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 33575E24-AF0F-432B-8539-157858D8F4D9/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:40:07.819Z  INFO 3588 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-10-13T14:40:07.875Z  INFO 3588 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:40:07.966Z  INFO 3588 --- [           main] o.s.d.j.r.query.QueryEnhancerFactories   : Hibernate is in classpath; If applicable, HQL parser will be used.
2026-10-13T14:40:08.225Z  INFO 3588 --- [           main] c.s.f.tender.DemoDataSeederTest          : Started DemoDataSeederTest in 2.998 seconds (process running for 4.317)
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
Mockito is currently self-attaching to enable the inline-mock-maker. This will no longer work in future releases of the JDK. Please add Mockito as an agent to your build as described in Mockito's documentation: https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html#0.3
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
WARNING: A Java agent has been loaded dynamically (/home/runner/.m2/repository/net/bytebuddy/byte-buddy-agent/1.18.11/byte-buddy-agent-1.18.11.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
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
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 4.595 s -- in com.senacor.freighttenders.tender.DemoDataSeederTest
[INFO] Running com.senacor.freighttenders.tender.TenderServicePersistenceTest
2026-10-13T14:40:09.299Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:09.310Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest
2026-10-13T14:40:09.311Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:09.321Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:09.354Z  INFO 3588 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Starting TenderServicePersistenceTest using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:09.355Z  INFO 3588 --- [           main] c.s.f.t.TenderServicePersistenceTest     : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:40:09.445Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:40:09.455Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 8 ms. Found 1 JPA repository interface.
2026-10-13T14:40:09.470Z  INFO 3588 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-10-13T14:40:09.481Z  INFO 3588 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:6aa7f321-18c2-4116-aa82-755db6816582;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-10-13T14:40:09.504Z  INFO 3588 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:40:09.524Z  INFO 3588 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:40:09.526Z  INFO 3588 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:6aa7f321-18c2-4116-aa82-755db6816582]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 6AA7F321-18C2-4116-AA82-755DB6816582/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:40:09.598Z  INFO 3588 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-10-13T14:40:09.609Z  INFO 3588 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:40:09.664Z  INFO 3588 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Started TenderServicePersistenceTest in 0.337 seconds (process running for 5.756)
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
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.470 s -- in com.senacor.freighttenders.tender.TenderServicePersistenceTest
[INFO] Running com.senacor.freighttenders.tender.TenderRepositoryTest
2026-10-13T14:40:09.773Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:09.790Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest
2026-10-13T14:40:09.791Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:09.806Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:09.861Z  INFO 3588 --- [           main] c.s.f.tender.TenderRepositoryTest        : Starting TenderRepositoryTest using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:09.861Z  INFO 3588 --- [           main] c.s.f.tender.TenderRepositoryTest        : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:40:09.948Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:40:09.957Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 7 ms. Found 1 JPA repository interface.
2026-10-13T14:40:09.969Z  INFO 3588 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-10-13T14:40:09.978Z  INFO 3588 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:44858ee8-313d-460a-8d93-152ea7e8d17f;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-10-13T14:40:09.998Z  INFO 3588 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:40:10.018Z  INFO 3588 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:40:10.020Z  INFO 3588 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:44858ee8-313d-460a-8d93-152ea7e8d17f]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 44858EE8-313D-460A-8D93-152EA7E8D17F/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:40:10.088Z  INFO 3588 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-10-13T14:40:10.100Z  INFO 3588 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:40:10.149Z  INFO 3588 --- [           main] c.s.f.tender.TenderRepositoryTest        : Started TenderRepositoryTest in 0.338 seconds (process running for 6.242)
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
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.522 s -- in com.senacor.freighttenders.tender.TenderRepositoryTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-10-13T14:40:10.298Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:10.301Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-10-13T14:40:10.304Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:10.305Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:10.307Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:10.342Z  INFO 3588 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Starting DemoProfileGatingTest.WithDemoProfile using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:10.343Z  INFO 3588 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : The following 1 profile is active: "demo"
2026-10-13T14:40:10.637Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:40:10.646Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 7 ms. Found 1 JPA repository interface.
2026-10-13T14:40:10.800Z  INFO 3588 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:40:10.820Z  INFO 3588 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:40:10.821Z  INFO 3588 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2026-10-13T14:40:10.831Z  INFO 3588 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection conn25: url=jdbc:h2:mem:freighttenders user=SA
2026-10-13T14:40:10.833Z  INFO 3588 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2026-10-13T14:40:10.843Z  INFO 3588 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:freighttenders]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: FREIGHTTENDERS/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:40:10.913Z  INFO 3588 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-10-13T14:40:10.927Z  INFO 3588 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:40:11.033Z  WARN 3588 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-10-13T14:40:11.371Z  INFO 3588 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:40:11.371Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:40:11.373Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 2 ms
2026-10-13T14:40:11.389Z  INFO 3588 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Started DemoProfileGatingTest.WithDemoProfile in 1.074 seconds (process running for 7.481)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.267 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-10-13T14:40:11.565Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:11.568Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-10-13T14:40:11.569Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:11.569Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:11.570Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:11.593Z  INFO 3588 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Starting DemoProfileGatingTest.WithoutDemoProfile using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:11.614Z  INFO 3588 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:40:11.729Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:40:11.736Z  INFO 3588 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 5 ms. Found 1 JPA repository interface.
2026-10-13T14:40:11.785Z  INFO 3588 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:40:11.799Z  INFO 3588 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:40:11.799Z  INFO 3588 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Starting...
2026-10-13T14:40:11.800Z  INFO 3588 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-2 - Added connection conn35: url=jdbc:h2:mem:freighttenders user=SA
2026-10-13T14:40:11.801Z  INFO 3588 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Start completed.
2026-10-13T14:40:11.801Z  INFO 3588 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:freighttenders]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: FREIGHTTENDERS/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:40:11.868Z  INFO 3588 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-10-13T14:40:11.876Z  INFO 3588 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:40:11.917Z  WARN 3588 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-10-13T14:40:11.999Z  INFO 3588 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:40:11.999Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:40:12.000Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-10-13T14:40:12.007Z  INFO 3588 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Started DemoProfileGatingTest.WithoutDemoProfile in 0.434 seconds (process running for 8.1)

MockHttpServletRequest:
      HTTP Method = GET
      Request URI = /api/tenders
       Parameters = {}
          Headers = []
             Body = null
    Session Attrs = {}

Handler:
             Type = com.senacor.freighttenders.tender.TenderController
           Method = com.senacor.freighttenders.tender.TenderController#listTenders(TenderStatus)

Async:
    Async started = false
     Async result = null

Resolved Exception:
             Type = null

ModelAndView:
        View name = null
             View = null
            Model = null

FlashMap:
       Attributes = null

MockHttpServletResponse:
           Status = 200
    Error message = null
          Headers = [Content-Type:"application/json"]
     Content type = application/json
             Body = [{"id":1,"origin":{"country":"DE","postalCode":"20457","city":"Hamburg"},"destination":{"country":"DE","postalCode":"80331","city":"München"},"pickupDate":"2026-10-20","deliveryDate":"2026-10-22","bidDeadline":"2026-10-16","commodity":"Paletten mit Haushaltsgeräten","weightKg":18000,"loadingMeters":13.6,"palletCount":33,"equipmentType":"CURTAIN_SIDER","dangerousGoods":false,"adrClass":null,"temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"EUR","status":"OPEN","offerCount":2,"lowestOfferAmount":1380.00,"awardedSupplierName":null,"awardedAmount":null},{"id":2,"origin":{"country":"NL","postalCode":"3011","city":"Rotterdam"},"destination":{"country":"DE","postalCode":"50667","city":"Köln"},"pickupDate":"2026-10-21","deliveryDate":"2026-10-22","bidDeadline":"2026-10-18","commodity":"Frische Milchprodukte","weightKg":12000,"loadingMeters":7.2,"palletCount":20,"equipmentType":"REEFER","dangerousGoods":false,"adrClass":null,"temperatureControlled":true,"temperatureMinC":2,"temperatureMaxC":8,"currency":"EUR","status":"OPEN","offerCount":2,"lowestOfferAmount":890.00,"awardedSupplierName":null,"awardedAmount":null},{"id":3,"origin":{"country":"DE","postalCode":"67059","city":"Ludwigshafen"},"destination":{"country":"FR","postalCode":"67000","city":"Straßburg"},"pickupDate":"2026-10-17","deliveryDate":"2026-10-18","bidDeadline":"2026-10-13","commodity":"Lösungsmittel in Fässern","weightKg":15000,"loadingMeters":6.0,"palletCount":24,"equipmentType":"BOX","dangerousGoods":true,"adrClass":"3","temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"EUR","status":"OPEN","offerCount":1,"lowestOfferAmount":720.00,"awardedSupplierName":null,"awardedAmount":null},{"id":4,"origin":{"country":"DE","postalCode":"70173","city":"Stuttgart"},"destination":{"country":"AT","postalCode":"1010","city":"Wien"},"pickupDate":"2026-10-23","deliveryDate":"2026-10-25","bidDeadline":"2026-10-20","commodity":"Stahlträger","weightKg":24000,"loadingMeters":13.6,"palletCount":null,"equipmentType":"FLATBED","dangerousGoods":false,"adrClass":null,"temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"EUR","status":"OPEN","offerCount":1,"lowestOfferAmount":1620.00,"awardedSupplierName":null,"awardedAmount":null},{"id":5,"origin":{"country":"DE","postalCode":"04109","city":"Leipzig"},"destination":{"country":"PL","postalCode":"00-001","city":"Warschau"},"pickupDate":"2026-10-15","deliveryDate":"2026-10-17","bidDeadline":"2026-10-12","commodity":"Autoteile","weightKg":9000,"loadingMeters":8.0,"palletCount":16,"equipmentType":"MEGA_TRAILER","dangerousGoods":false,"adrClass":null,"temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"EUR","status":"OPEN","offerCount":2,"lowestOfferAmount":980.00,"awardedSupplierName":null,"awardedAmount":null},{"id":6,"origin":{"country":"DE","postalCode":"79098","city":"Freiburg"},"destination":{"country":"CH","postalCode":"8001","city":"Zürich"},"pickupDate":"2026-10-19","deliveryDate":"2026-10-20","bidDeadline":"2026-10-17","commodity":"Maschinenteile","weightKg":7000,"loadingMeters":4.5,"palletCount":10,"equipmentType":"BOX","dangerousGoods":false,"adrClass":null,"temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"CHF","status":"OPEN","offerCount":1,"lowestOfferAmount":840.00,"awardedSupplierName":null,"awardedAmount":null},{"id":7,"origin":{"country":"DE","postalCode":"28195","city":"Bremen"},"destination":{"country":"DE","postalCode":"01067","city":"Dresden"},"pickupDate":"2026-10-16","deliveryDate":"2026-10-17","bidDeadline":"2026-10-11","commodity":"Getränkekisten","weightKg":20000,"loadingMeters":13.6,"palletCount":33,"equipmentType":"CURTAIN_SIDER","dangerousGoods":false,"adrClass":null,"temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"EUR","status":"AWARDED","offerCount":2,"lowestOfferAmount":1100.00,"awardedSupplierName":"Elbe Frachtkontor GmbH","awardedAmount":1100.00},{"id":8,"origin":{"country":"DE","postalCode":"90402","city":"Nürnberg"},"destination":{"country":"DE","postalCode":"30159","city":"Hannover"},"pickupDate":"2026-10-18","deliveryDate":"2026-10-19","bidDeadline":"2026-10-10","commodity":"Büromöbel","weightKg":5000,"loadingMeters":5.0,"palletCount":12,"equipmentType":"BOX","dangerousGoods":false,"adrClass":null,"temperatureControlled":false,"temperatureMinC":null,"temperatureMaxC":null,"currency":"EUR","status":"CLOSED","offerCount":1,"lowestOfferAmount":560.00,"awardedSupplierName":null,"awardedAmount":null}]
    Forwarded URL = null
   Redirected URL = null
          Cookies = []
[ERROR] Tests run: 1, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 0.495 s <<< FAILURE! -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
[ERROR] com.senacor.freighttenders.tender.DemoProfileGatingTest.seederBeanIsAbsentAndNoTendersExist -- Time elapsed: 0.045 s <<< FAILURE!
java.lang.AssertionError: JSON path "$.length()" expected:<0> but was:<8>
	at org.springframework.test.util.AssertionErrors.fail(AssertionErrors.java:62)
	at org.springframework.test.util.AssertionErrors.assertEquals(AssertionErrors.java:129)
	at org.springframework.test.util.JsonPathExpectationsHelper.assertValue(JsonPathExpectationsHelper.java:172)
	at org.springframework.test.web.servlet.result.JsonPathResultMatchers.lambda$value$2(JsonPathResultMatchers.java:111)
	at org.springframework.test.web.servlet.MockMvc$1.andExpect(MockMvc.java:212)
	at com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile.seederBeanIsAbsentAndNoTendersExist(DemoProfileGatingTest.java:35)

[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.767 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.TenderServiceTest
[INFO] Tests run: 20, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.297 s -- in com.senacor.freighttenders.tender.TenderServiceTest
[INFO] Running com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-10-13T14:40:12.371Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:12.382Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-10-13T14:40:12.382Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:12.386Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:12.434Z  INFO 3588 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Starting TenderCreateValidationTest using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:12.434Z  INFO 3588 --- [           main] c.s.f.tender.TenderCreateValidationTest  : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:40:12.748Z  INFO 3588 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:40:12.748Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:40:12.750Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 2 ms
2026-10-13T14:40:12.762Z  INFO 3588 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Started TenderCreateValidationTest in 0.352 seconds (process running for 8.855)
[INFO] Tests run: 58, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.190 s -- in com.senacor.freighttenders.tender.TenderCreateValidationTest
[INFO] Running com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Running com.senacor.freighttenders.tender.TenderControllerTest
2026-10-13T14:40:13.564Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:13.572Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
2026-10-13T14:40:13.572Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:13.578Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.437 s -- in com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Running com.senacor.freighttenders.health.HealthControllerTest
2026-10-13T14:40:14.003Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:14.021Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest
2026-10-13T14:40:14.022Z  INFO 3588 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:40:14.026Z  INFO 3588 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:40:14.056Z  INFO 3588 --- [           main] c.s.f.health.HealthControllerTest        : Starting HealthControllerTest using Java 25.0.4.1 with PID 3588 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:40:14.056Z  INFO 3588 --- [           main] c.s.f.health.HealthControllerTest        : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:40:14.294Z  INFO 3588 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:40:14.294Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:40:14.296Z  INFO 3588 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-10-13T14:40:14.303Z  INFO 3588 --- [           main] c.s.f.health.HealthControllerTest        : Started HealthControllerTest in 0.273 seconds (process running for 10.395)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.323 s -- in com.senacor.freighttenders.health.HealthControllerTest
2026-10-13T14:40:14.333Z  INFO 3588 --- [ionShutdownHook] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
[INFO] 
[INFO] Results:
[INFO] 
[ERROR] Failures: 
[ERROR]   DemoProfileGatingTest.seederBeanIsAbsentAndNoTendersExist JSON path "$.length()" expected:<0> but was:<8>
[INFO] 
[ERROR] Tests run: 127, Failures: 1, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  14.807 s
[INFO] Finished at: 2026-10-13T14:40:14Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:3.5.6:test (default-test) on project freight-tenders-backend: There are test failures.
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
