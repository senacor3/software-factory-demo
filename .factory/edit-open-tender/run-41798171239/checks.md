---
schema_version: 1
story_slug: edit-open-tender
stage: checks
status: findings-open
updated: 2026-11-04T08:26:23Z
fix_cycle: 1
---

## Failing checks

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
[INFO] Compiling 11 source files with javac [debug parameters release 25] to target/test-classes
[INFO] 
[INFO] --- surefire:3.5.6:test (default-test) @ freight-tenders-backend ---
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.senacor.freighttenders.tender.TenderServiceTest
08:25:19.583 [main] INFO org.hibernate.validator.internal.util.Version -- HV000001: Hibernate Validator 9.1.3.Final
Mockito is currently self-attaching to enable the inline-mock-maker. This will no longer work in future releases of the JDK. Please add Mockito as an agent to your build as described in Mockito's documentation: https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html#0.3
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
WARNING: A Java agent has been loaded dynamically (/home/runner/.m2/repository/net/bytebuddy/byte-buddy-agent/1.18.11/byte-buddy-agent-1.18.11.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
[INFO] Tests run: 20, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.216 s -- in com.senacor.freighttenders.tender.TenderServiceTest
[INFO] Running com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 s -- in com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Running com.senacor.freighttenders.tender.TenderServicePersistenceTest
08:25:20.802 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
08:25:21.088 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest
08:25:21.090 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
08:25:21.114 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:21.460Z  INFO 2611 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Starting TenderServicePersistenceTest using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:21.461Z  INFO 2611 --- [           main] c.s.f.t.TenderServicePersistenceTest     : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:25:21.836Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:25:21.884Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 41 ms. Found 1 JPA repository interface.
2026-11-04T08:25:21.929Z  INFO 2611 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-11-04T08:25:22.102Z  INFO 2611 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:96182e1d-eb1e-453c-8335-5ddaa32be4ca;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-11-04T08:25:22.321Z  INFO 2611 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:25:22.357Z  INFO 2611 --- [           main] org.hibernate.orm.core                   : HHH000001: Hibernate ORM core version 7.4.5.Final
2026-11-04T08:25:22.576Z  INFO 2611 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:25:22.647Z  INFO 2611 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:96182e1d-eb1e-453c-8335-5ddaa32be4ca]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 96182E1D-EB1E-453C-8335-5DDAA32BE4CA/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:25:23.248Z  INFO 2611 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-11-04T08:25:23.303Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:25:23.387Z  INFO 2611 --- [           main] o.s.d.j.r.query.QueryEnhancerFactories   : Hibernate is in classpath; If applicable, HQL parser will be used.
2026-11-04T08:25:23.541Z  WARN 2611 --- [           main] s.c.a.AnnotationConfigApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.TenderService': Unsatisfied dependency expressed through constructor parameter 2: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
2026-11-04T08:25:23.542Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'



============================
CONDITIONS EVALUATION REPORT
============================


Positive matches:
-----------------

   DataJpaRepositoriesAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.data.jpa.repository.JpaRepository' (OnClassCondition)
      - @ConditionalOnBooleanProperty (spring.data.jpa.repositories.enabled=true) matched (OnPropertyCondition)
      - @ConditionalOnBean (types: javax.sql.DataSource; SearchStrategy: all) found bean 'dataSource'; @ConditionalOnMissingBean (types: org.springframework.data.jpa.repository.support.JpaRepositoryFactoryBean,org.springframework.data.jpa.repository.config.JpaRepositoryConfigExtension; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseType' (OnClassCondition)
      - @ConditionalOnMissingBean (types: io.r2dbc.spi.ConnectionFactory; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceAutoConfiguration.PooledDataSourceConfiguration matched:
      - AnyNestedCondition 1 matched 1 did not; NestedCondition on DataSourceAutoConfiguration.PooledDataSourceCondition.PooledDataSourceAvailable PooledDataSource found supported DataSource; NestedCondition on DataSourceAutoConfiguration.PooledDataSourceCondition.ExplicitType @ConditionalOnProperty (spring.datasource.type) did not find property 'spring.datasource.type' (DataSourceAutoConfiguration.PooledDataSourceCondition)
      - @ConditionalOnMissingBean (types: javax.sql.DataSource,javax.sql.XADataSource; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceAutoConfiguration.PooledDataSourceConfiguration#jdbcConnectionDetails matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.jdbc.autoconfigure.JdbcConnectionDetails; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceConfiguration.Hikari matched:
      - @ConditionalOnClass found required class 'com.zaxxer.hikari.HikariDataSource' (OnClassCondition)
      - @ConditionalOnProperty (spring.datasource.type=com.zaxxer.hikari.HikariDataSource) matched (OnPropertyCondition)
      - @ConditionalOnMissingBean (types: javax.sql.DataSource; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceInitializationAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.jdbc.datasource.init.DatabasePopulator' (OnClassCondition)
      - SQL InitializationDatabase Initialization default value is EMBEDDED (OnSqlInitializationCondition)
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource'; @ConditionalOnMissingBean (types: org.springframework.boot.sql.autoconfigure.init.ApplicationScriptDatabaseInitializer; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourcePoolMetadataProvidersConfiguration.HikariPoolDataSourceMetadataProviderConfiguration matched:
      - @ConditionalOnClass found required class 'com.zaxxer.hikari.HikariDataSource' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.core.JdbcTemplate', 'org.springframework.transaction.TransactionManager' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration.JdbcTransactionManagerConfiguration matched:
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource' (OnBeanCondition)

   HibernateJpaAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean', 'jakarta.persistence.EntityManager', 'org.hibernate.engine.spi.SessionImplementor' (OnClassCondition)

   HibernateJpaConfiguration matched:
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource' (OnBeanCondition)

   JdbcClientAutoConfiguration matched:
      - @ConditionalOnSingleCandidate (types: org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate; SearchStrategy: all) found a single bean 'namedParameterJdbcTemplate'; @ConditionalOnMissingBean (types: org.springframework.jdbc.core.simple.JdbcClient; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JdbcTemplateAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.core.JdbcTemplate' (OnClassCondition)
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource' (OnBeanCondition)

   JdbcTemplateConfiguration matched:
      - @ConditionalOnMissingBean (types: org.springframework.jdbc.core.JdbcOperations; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#entityManagerFactory matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean,jakarta.persistence.EntityManagerFactory; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#entityManagerFactoryBuilder matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.jpa.EntityManagerFactoryBuilder; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#jpaVendorAdapter matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.JpaVendorAdapter; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#transactionManager matched:
      - @ConditionalOnMissingBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration.PersistenceManagedTypesConfiguration matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean,jakarta.persistence.EntityManagerFactory; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration.PersistenceManagedTypesConfiguration#persistenceManagedTypes matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.persistenceunit.PersistenceManagedTypes; SearchStrategy: all) did not find any beans (OnBeanCondition)

   NamedParameterJdbcTemplateConfiguration matched:
      - @ConditionalOnSingleCandidate (types: org.springframework.jdbc.core.JdbcTemplate; SearchStrategy: all) found a single bean 'jdbcTemplate'; @ConditionalOnMissingBean (types: org.springframework.jdbc.core.namedparam.NamedParameterJdbcOperations; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TestDatabaseAutoConfiguration#nonTestEmbeddedDataSourceBeanFactoryPostProcessor matched:
      - @ConditionalOnProperty (spring.test.database.replace=NON_TEST) matched (OnPropertyCondition)

   TestEntityManagerAutoConfiguration matched:
      - @ConditionalOnClass found required class 'jakarta.persistence.EntityManagerFactory' (OnClassCondition)

   TestEntityManagerAutoConfiguration#testEntityManager matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.jpa.test.autoconfigure.TestEntityManager; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.transaction.PlatformTransactionManager' (OnClassCondition)

   TransactionAutoConfiguration.EnableTransactionManagementConfiguration matched:
      - @ConditionalOnBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) found bean 'transactionManager'; @ConditionalOnMissingBean (types: org.springframework.transaction.annotation.AbstractTransactionManagementConfiguration; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionAutoConfiguration.EnableTransactionManagementConfiguration.CglibAutoProxyConfiguration matched:
      - @ConditionalOnBooleanProperty (spring.aop.proxy-target-class=true) matched (OnPropertyCondition)

   TransactionAutoConfiguration.TransactionTemplateConfiguration matched:
      - @ConditionalOnSingleCandidate (types: org.springframework.transaction.PlatformTransactionManager; SearchStrategy: all) found a single bean 'transactionManager' (OnBeanCondition)

   TransactionAutoConfiguration.TransactionTemplateConfiguration#transactionTemplate matched:
      - @ConditionalOnMissingBean (types: org.springframework.transaction.support.TransactionOperations; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionManagerCustomizationAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.transaction.PlatformTransactionManager' (OnClassCondition)

   TransactionManagerCustomizationAutoConfiguration#platformTransactionManagerCustomizers matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizers; SearchStrategy: all) did not find any beans (OnBeanCondition)


Negative matches:
-----------------

   DataJpaRepositoriesAutoConfiguration#entityManagerFactoryBootstrapExecutorCustomizer:
      Did not match:
         - @ConditionalOnProperty (spring.data.jpa.repositories.bootstrap-mode=deferred) found different value in property 'spring.data.jpa.repositories.bootstrap-mode' (OnPropertyCondition)

   DataSourceAutoConfiguration.EmbeddedDatabaseConfiguration:
      Did not match:
         - EmbeddedDataSource spring.datasource.url is set (DataSourceAutoConfiguration.EmbeddedDatabaseCondition)

   DataSourceCheckpointRestoreConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.crac.Resource' (OnClassCondition)

   DataSourceConfiguration.Dbcp2:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.commons.dbcp2.BasicDataSource' (OnClassCondition)

   DataSourceConfiguration.Generic:
      Did not match:
         - @ConditionalOnProperty (spring.datasource.type) did not find property 'spring.datasource.type' (OnPropertyCondition)

   DataSourceConfiguration.OracleUcp:
      Did not match:
         - @ConditionalOnClass did not find required classes 'oracle.ucp.jdbc.PoolDataSourceImpl', 'oracle.jdbc.OracleConnection' (OnClassCondition)

   DataSourceConfiguration.Tomcat:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.tomcat.jdbc.pool.DataSource' (OnClassCondition)

   DataSourceJmxConfiguration:
      Did not match:
         - @ConditionalOnBooleanProperty (spring.jmx.enabled=true) found different value in property 'spring.jmx.enabled' (OnPropertyCondition)

   DataSourcePoolMetadataProvidersConfiguration.CommonsDbcp2PoolDataSourceMetadataProviderConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.commons.dbcp2.BasicDataSource' (OnClassCondition)

   DataSourcePoolMetadataProvidersConfiguration.OracleUcpPoolDataSourceMetadataProviderConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required classes 'oracle.ucp.jdbc.PoolDataSource', 'oracle.jdbc.OracleConnection' (OnClassCondition)

   DataSourcePoolMetadataProvidersConfiguration.TomcatDataSourcePoolMetadataProviderConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.tomcat.jdbc.pool.DataSource' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration.JdbcTransactionManagerConfiguration#transactionManager:
      Did not match:
         - @ConditionalOnMissingBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) found beans of type 'org.springframework.transaction.TransactionManager' transactionManager (OnBeanCondition)

   JpaBaseConfiguration.JpaWebConfiguration:
      Did not match:
         - not a servlet web application (OnWebApplicationCondition)
      Matched:
         - @ConditionalOnClass found required class 'org.springframework.web.servlet.config.annotation.WebMvcConfigurer' (OnClassCondition)

   LazyConnectionDataSourceConfiguration:
      Did not match:
         - @ConditionalOnProperty (spring.datasource.connection-fetch=lazy) did not find property 'spring.datasource.connection-fetch' (OnPropertyCondition)

   TestDatabaseAutoConfiguration#dataSource:
      Did not match:
         - @ConditionalOnProperty (spring.test.database.replace=AUTO_CONFIGURED) did not find property 'spring.test.database.replace' (OnPropertyCondition)

   TestDatabaseAutoConfiguration#embeddedDataSourceBeanFactoryPostProcessor:
      Did not match:
         - @ConditionalOnProperty (spring.test.database.replace=ANY) did not find property 'spring.test.database.replace' (OnPropertyCondition)

   TransactionAutoConfiguration#transactionalOperator:
      Did not match:
         - @ConditionalOnSingleCandidate (types: org.springframework.transaction.ReactiveTransactionManager; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionAutoConfiguration.AspectJTransactionManagementConfiguration:
      Did not match:
         - @ConditionalOnBean (types: org.springframework.transaction.aspectj.AbstractTransactionAspect; SearchStrategy: all) did not find any beans of type org.springframework.transaction.aspectj.AbstractTransactionAspect (OnBeanCondition)

   TransactionAutoConfiguration.EnableTransactionManagementConfiguration.JdkDynamicAutoProxyConfiguration:
      Did not match:
         - @ConditionalOnBooleanProperty (spring.aop.proxy-target-class=false) did not find property 'spring.aop.proxy-target-class' (OnPropertyCondition)


Exclusions:
-----------

    None


Unconditional classes:
----------------------

    org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration



2026-11-04T08:25:23.549Z  INFO 2611 --- [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2026-11-04T08:25:23.562Z ERROR 2611 --- [           main] o.s.b.d.LoggingFailureAnalysisReporter   : 

***************************
APPLICATION FAILED TO START
***************************

Description:

Parameter 2 of constructor in com.senacor.freighttenders.tender.TenderService required a bean of type 'jakarta.validation.Validator' that could not be found.


Action:

Consider defining a bean of type 'jakarta.validation.Validator' in your configuration.

2026-11-04T08:25:23.564Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.TenderServicePersistenceTest@1d2b49b2]

java.lang.IllegalStateException: Failed to load ApplicationContext for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:195) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.cache.DefaultContextCache.put(DefaultContextCache.java:214) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:160) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.TenderService': Unsatisfied dependency expressed through constructor parameter 2: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:804) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:240) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1380) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1219) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:565) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:525) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:333) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:371) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:331) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:196) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.instantiateSingleton(DefaultListableBeanFactory.java:1225) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingleton(DefaultListableBeanFactory.java:1191) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:1121) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:994) ~[spring-context-7.0.9.jar:7.0.9]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:621) ~[spring-context-7.0.9.jar:7.0.9]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:756) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:445) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:321) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader.lambda$loadContext$2(SpringBootContextLoader.java:155) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:58) ~[spring-core-7.0.9.jar:7.0.9]
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:46) ~[spring-core-7.0.9.jar:7.0.9]
	at org.springframework.boot.SpringApplication.withHook(SpringApplication.java:1465) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader$ContextLoaderHook.run(SpringBootContextLoader.java:600) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:155) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:114) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContextInternal(DefaultCacheAwareContextLoaderDelegate.java:247) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:167) ~[spring-test-7.0.9.jar:7.0.9]
	... 86 common frames omitted
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:912) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:791) ~[spring-beans-7.0.9.jar:7.0.9]
	... 112 common frames omitted

2026-11-04T08:25:23.578Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.TenderServicePersistenceTest@4164ab12]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:23.582Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.TenderServicePersistenceTest@2a6b6f4]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:23.584Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.TenderServicePersistenceTest@753b6846]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

[ERROR] Tests run: 4, Failures: 0, Errors: 4, Skipped: 0, Time elapsed: 2.891 s <<< FAILURE! -- in com.senacor.freighttenders.tender.TenderServicePersistenceTest
[ERROR] com.senacor.freighttenders.tender.TenderServicePersistenceTest.addOfferAppendsTheNewOfferAsTheLastElementAfterRealPersistence -- Time elapsed: 0.003 s <<< ERROR!
java.lang.IllegalStateException: Failed to load ApplicationContext for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:195)
	at org.springframework.test.context.cache.DefaultContextCache.put(DefaultContextCache.java:214)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:160)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.TenderService': Unsatisfied dependency expressed through constructor parameter 2: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:804)
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:240)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1380)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1219)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:565)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:525)
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:333)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:371)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:331)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:196)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.instantiateSingleton(DefaultListableBeanFactory.java:1225)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingleton(DefaultListableBeanFactory.java:1191)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:1121)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:994)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:621)
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:756)
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:445)
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:321)
	at org.springframework.boot.test.context.SpringBootContextLoader.lambda$loadContext$2(SpringBootContextLoader.java:155)
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:58)
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:46)
	at org.springframework.boot.SpringApplication.withHook(SpringApplication.java:1465)
	at org.springframework.boot.test.context.SpringBootContextLoader$ContextLoaderHook.run(SpringBootContextLoader.java:600)
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:155)
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:114)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContextInternal(DefaultCacheAwareContextLoaderDelegate.java:247)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:167)
	... 21 more
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:912)
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:791)
	... 47 more

[ERROR] com.senacor.freighttenders.tender.TenderServicePersistenceTest.addRemarkAppendsTheNewRemarkAsTheLastElementAfterRealPersistence -- Time elapsed: 0.001 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.TenderServicePersistenceTest.awardedOfferPersistsAndReloads -- Time elapsed: 0 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.TenderServicePersistenceTest.listingTendersFetchesOffersWithAConstantNumberOfQueries -- Time elapsed: 0 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-11-04T08:25:23.593Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:23.595Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-11-04T08:25:23.601Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:23.601Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:23.606Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:23.672Z  INFO 2611 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Starting DemoProfileGatingTest.WithDemoProfile using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:23.672Z  INFO 2611 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : The following 1 profile is active: "demo"
2026-11-04T08:25:23.946Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:25:23.956Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 8 ms. Found 1 JPA repository interface.
2026-11-04T08:25:24.078Z  INFO 2611 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:25:24.092Z  INFO 2611 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:25:24.094Z  INFO 2611 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2026-11-04T08:25:24.102Z  INFO 2611 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection conn3: url=jdbc:h2:mem:gating-with-demo user=SA
2026-11-04T08:25:24.103Z  INFO 2611 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2026-11-04T08:25:24.111Z  INFO 2611 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
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
2026-11-04T08:25:24.164Z  INFO 2611 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-11-04T08:25:24.177Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:25:24.277Z  WARN 2611 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-11-04T08:25:24.621Z  INFO 2611 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:25:24.621Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:25:24.623Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-11-04T08:25:24.641Z  INFO 2611 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Started DemoProfileGatingTest.WithDemoProfile in 1.022 seconds (process running for 5.879)
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.667 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-11-04T08:25:25.260Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:25.264Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-11-04T08:25:25.267Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:25.268Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:25.269Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:25.293Z  INFO 2611 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Starting DemoProfileGatingTest.WithoutDemoProfile using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:25.293Z  INFO 2611 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:25:25.390Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:25:25.395Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 4 ms. Found 1 JPA repository interface.
2026-11-04T08:25:25.462Z  INFO 2611 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:25:25.476Z  INFO 2611 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:25:25.477Z  INFO 2611 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Starting...
2026-11-04T08:25:25.480Z  INFO 2611 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-2 - Added connection conn13: url=jdbc:h2:mem:gating-without-demo user=SA
2026-11-04T08:25:25.480Z  INFO 2611 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Start completed.
2026-11-04T08:25:25.480Z  INFO 2611 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
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
2026-11-04T08:25:25.530Z  INFO 2611 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-11-04T08:25:25.538Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:25:25.576Z  WARN 2611 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-11-04T08:25:25.663Z  INFO 2611 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:25:25.664Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:25:25.664Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 0 ms
2026-11-04T08:25:25.673Z  INFO 2611 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Started DemoProfileGatingTest.WithoutDemoProfile in 0.396 seconds (process running for 6.911)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.436 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.106 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.TenderRepositoryTest
2026-11-04T08:25:25.698Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:25.704Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest
2026-11-04T08:25:25.705Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:25.711Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:25.732Z  INFO 2611 --- [           main] c.s.f.tender.TenderRepositoryTest        : Starting TenderRepositoryTest using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:25.732Z  INFO 2611 --- [           main] c.s.f.tender.TenderRepositoryTest        : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:25:25.780Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:25:25.786Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 4 ms. Found 1 JPA repository interface.
2026-11-04T08:25:25.795Z  INFO 2611 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-11-04T08:25:25.801Z  INFO 2611 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:b7e20f52-ddeb-4135-b73f-cd99969782d4;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-11-04T08:25:25.811Z  INFO 2611 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:25:25.830Z  INFO 2611 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:25:25.832Z  INFO 2611 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:b7e20f52-ddeb-4135-b73f-cd99969782d4]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: B7E20F52-DDEB-4135-B73F-CD99969782D4/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:25:25.879Z  INFO 2611 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-11-04T08:25:25.887Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:25:25.932Z  INFO 2611 --- [           main] c.s.f.tender.TenderRepositoryTest        : Started TenderRepositoryTest in 0.219 seconds (process running for 7.171)
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
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.348 s -- in com.senacor.freighttenders.tender.TenderRepositoryTest
[INFO] Running com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-11-04T08:25:26.053Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:26.062Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-11-04T08:25:26.063Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:26.066Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:26.109Z  INFO 2611 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Starting TenderCreateValidationTest using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:26.109Z  INFO 2611 --- [           main] c.s.f.tender.TenderCreateValidationTest  : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:25:26.371Z  INFO 2611 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:25:26.371Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:25:26.372Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-11-04T08:25:26.381Z  INFO 2611 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Started TenderCreateValidationTest in 0.289 seconds (process running for 7.62)
[INFO] Tests run: 58, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.015 s -- in com.senacor.freighttenders.tender.TenderCreateValidationTest
[INFO] Running com.senacor.freighttenders.tender.TenderControllerTest
2026-11-04T08:25:27.067Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:27.074Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
2026-11-04T08:25:27.074Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:27.079Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.335 s -- in com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Running com.senacor.freighttenders.tender.DemoDataSeederTest
2026-11-04T08:25:27.406Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:27.418Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest
2026-11-04T08:25:27.419Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:27.424Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:27.446Z  INFO 2611 --- [           main] c.s.f.tender.DemoDataSeederTest          : Starting DemoDataSeederTest using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:27.446Z  INFO 2611 --- [           main] c.s.f.tender.DemoDataSeederTest          : The following 1 profile is active: "demo"
2026-11-04T08:25:27.516Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-11-04T08:25:27.523Z  INFO 2611 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 5 ms. Found 1 JPA repository interface.
2026-11-04T08:25:27.534Z  INFO 2611 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-11-04T08:25:27.543Z  INFO 2611 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:ebd86e23-c51e-4383-a2db-a14839b84e9a;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-11-04T08:25:27.557Z  INFO 2611 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-11-04T08:25:27.576Z  INFO 2611 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-11-04T08:25:27.578Z  INFO 2611 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:ebd86e23-c51e-4383-a2db-a14839b84e9a]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: EBD86E23-C51E-4383-A2DB-A14839B84E9A/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-11-04T08:25:27.631Z  INFO 2611 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-11-04T08:25:27.639Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-11-04T08:25:27.669Z  WARN 2611 --- [           main] s.c.a.AnnotationConfigApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.TenderService': Unsatisfied dependency expressed through constructor parameter 2: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
2026-11-04T08:25:27.670Z  INFO 2611 --- [           main] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'



============================
CONDITIONS EVALUATION REPORT
============================


Positive matches:
-----------------

   DataJpaRepositoriesAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.data.jpa.repository.JpaRepository' (OnClassCondition)
      - @ConditionalOnBooleanProperty (spring.data.jpa.repositories.enabled=true) matched (OnPropertyCondition)
      - @ConditionalOnBean (types: javax.sql.DataSource; SearchStrategy: all) found bean 'dataSource'; @ConditionalOnMissingBean (types: org.springframework.data.jpa.repository.support.JpaRepositoryFactoryBean,org.springframework.data.jpa.repository.config.JpaRepositoryConfigExtension; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseType' (OnClassCondition)
      - @ConditionalOnMissingBean (types: io.r2dbc.spi.ConnectionFactory; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceAutoConfiguration.PooledDataSourceConfiguration matched:
      - AnyNestedCondition 1 matched 1 did not; NestedCondition on DataSourceAutoConfiguration.PooledDataSourceCondition.PooledDataSourceAvailable PooledDataSource found supported DataSource; NestedCondition on DataSourceAutoConfiguration.PooledDataSourceCondition.ExplicitType @ConditionalOnProperty (spring.datasource.type) did not find property 'spring.datasource.type' (DataSourceAutoConfiguration.PooledDataSourceCondition)
      - @ConditionalOnMissingBean (types: javax.sql.DataSource,javax.sql.XADataSource; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceAutoConfiguration.PooledDataSourceConfiguration#jdbcConnectionDetails matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.jdbc.autoconfigure.JdbcConnectionDetails; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceConfiguration.Hikari matched:
      - @ConditionalOnClass found required class 'com.zaxxer.hikari.HikariDataSource' (OnClassCondition)
      - @ConditionalOnProperty (spring.datasource.type=com.zaxxer.hikari.HikariDataSource) matched (OnPropertyCondition)
      - @ConditionalOnMissingBean (types: javax.sql.DataSource; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceInitializationAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.jdbc.datasource.init.DatabasePopulator' (OnClassCondition)
      - SQL InitializationDatabase Initialization default value is EMBEDDED (OnSqlInitializationCondition)
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource'; @ConditionalOnMissingBean (types: org.springframework.boot.sql.autoconfigure.init.ApplicationScriptDatabaseInitializer; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourcePoolMetadataProvidersConfiguration.HikariPoolDataSourceMetadataProviderConfiguration matched:
      - @ConditionalOnClass found required class 'com.zaxxer.hikari.HikariDataSource' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.core.JdbcTemplate', 'org.springframework.transaction.TransactionManager' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration.JdbcTransactionManagerConfiguration matched:
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource' (OnBeanCondition)

   HibernateJpaAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean', 'jakarta.persistence.EntityManager', 'org.hibernate.engine.spi.SessionImplementor' (OnClassCondition)

   HibernateJpaConfiguration matched:
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource' (OnBeanCondition)

   JdbcClientAutoConfiguration matched:
      - @ConditionalOnSingleCandidate (types: org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate; SearchStrategy: all) found a single bean 'namedParameterJdbcTemplate'; @ConditionalOnMissingBean (types: org.springframework.jdbc.core.simple.JdbcClient; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JdbcTemplateAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.core.JdbcTemplate' (OnClassCondition)
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a single bean 'dataSource' (OnBeanCondition)

   JdbcTemplateConfiguration matched:
      - @ConditionalOnMissingBean (types: org.springframework.jdbc.core.JdbcOperations; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#entityManagerFactory matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean,jakarta.persistence.EntityManagerFactory; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#entityManagerFactoryBuilder matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.jpa.EntityManagerFactoryBuilder; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#jpaVendorAdapter matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.JpaVendorAdapter; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration#transactionManager matched:
      - @ConditionalOnMissingBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration.PersistenceManagedTypesConfiguration matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean,jakarta.persistence.EntityManagerFactory; SearchStrategy: all) did not find any beans (OnBeanCondition)

   JpaBaseConfiguration.PersistenceManagedTypesConfiguration#persistenceManagedTypes matched:
      - @ConditionalOnMissingBean (types: org.springframework.orm.jpa.persistenceunit.PersistenceManagedTypes; SearchStrategy: all) did not find any beans (OnBeanCondition)

   NamedParameterJdbcTemplateConfiguration matched:
      - @ConditionalOnSingleCandidate (types: org.springframework.jdbc.core.JdbcTemplate; SearchStrategy: all) found a single bean 'jdbcTemplate'; @ConditionalOnMissingBean (types: org.springframework.jdbc.core.namedparam.NamedParameterJdbcOperations; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TestDatabaseAutoConfiguration#nonTestEmbeddedDataSourceBeanFactoryPostProcessor matched:
      - @ConditionalOnProperty (spring.test.database.replace=NON_TEST) matched (OnPropertyCondition)

   TestEntityManagerAutoConfiguration matched:
      - @ConditionalOnClass found required class 'jakarta.persistence.EntityManagerFactory' (OnClassCondition)

   TestEntityManagerAutoConfiguration#testEntityManager matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.jpa.test.autoconfigure.TestEntityManager; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.transaction.PlatformTransactionManager' (OnClassCondition)

   TransactionAutoConfiguration.EnableTransactionManagementConfiguration matched:
      - @ConditionalOnBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) found bean 'transactionManager'; @ConditionalOnMissingBean (types: org.springframework.transaction.annotation.AbstractTransactionManagementConfiguration; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionAutoConfiguration.EnableTransactionManagementConfiguration.CglibAutoProxyConfiguration matched:
      - @ConditionalOnBooleanProperty (spring.aop.proxy-target-class=true) matched (OnPropertyCondition)

   TransactionAutoConfiguration.TransactionTemplateConfiguration matched:
      - @ConditionalOnSingleCandidate (types: org.springframework.transaction.PlatformTransactionManager; SearchStrategy: all) found a single bean 'transactionManager' (OnBeanCondition)

   TransactionAutoConfiguration.TransactionTemplateConfiguration#transactionTemplate matched:
      - @ConditionalOnMissingBean (types: org.springframework.transaction.support.TransactionOperations; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionManagerCustomizationAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.transaction.PlatformTransactionManager' (OnClassCondition)

   TransactionManagerCustomizationAutoConfiguration#platformTransactionManagerCustomizers matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizers; SearchStrategy: all) did not find any beans (OnBeanCondition)


Negative matches:
-----------------

   DataJpaRepositoriesAutoConfiguration#entityManagerFactoryBootstrapExecutorCustomizer:
      Did not match:
         - @ConditionalOnProperty (spring.data.jpa.repositories.bootstrap-mode=deferred) found different value in property 'spring.data.jpa.repositories.bootstrap-mode' (OnPropertyCondition)

   DataSourceAutoConfiguration.EmbeddedDatabaseConfiguration:
      Did not match:
         - EmbeddedDataSource spring.datasource.url is set (DataSourceAutoConfiguration.EmbeddedDatabaseCondition)

   DataSourceCheckpointRestoreConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.crac.Resource' (OnClassCondition)

   DataSourceConfiguration.Dbcp2:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.commons.dbcp2.BasicDataSource' (OnClassCondition)

   DataSourceConfiguration.Generic:
      Did not match:
         - @ConditionalOnProperty (spring.datasource.type) did not find property 'spring.datasource.type' (OnPropertyCondition)

   DataSourceConfiguration.OracleUcp:
      Did not match:
         - @ConditionalOnClass did not find required classes 'oracle.ucp.jdbc.PoolDataSourceImpl', 'oracle.jdbc.OracleConnection' (OnClassCondition)

   DataSourceConfiguration.Tomcat:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.tomcat.jdbc.pool.DataSource' (OnClassCondition)

   DataSourceJmxConfiguration:
      Did not match:
         - @ConditionalOnBooleanProperty (spring.jmx.enabled=true) found different value in property 'spring.jmx.enabled' (OnPropertyCondition)

   DataSourcePoolMetadataProvidersConfiguration.CommonsDbcp2PoolDataSourceMetadataProviderConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.commons.dbcp2.BasicDataSource' (OnClassCondition)

   DataSourcePoolMetadataProvidersConfiguration.OracleUcpPoolDataSourceMetadataProviderConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required classes 'oracle.ucp.jdbc.PoolDataSource', 'oracle.jdbc.OracleConnection' (OnClassCondition)

   DataSourcePoolMetadataProvidersConfiguration.TomcatDataSourcePoolMetadataProviderConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required class 'org.apache.tomcat.jdbc.pool.DataSource' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration.JdbcTransactionManagerConfiguration#transactionManager:
      Did not match:
         - @ConditionalOnMissingBean (types: org.springframework.transaction.TransactionManager; SearchStrategy: all) found beans of type 'org.springframework.transaction.TransactionManager' transactionManager (OnBeanCondition)

   JpaBaseConfiguration.JpaWebConfiguration:
      Did not match:
         - not a servlet web application (OnWebApplicationCondition)
      Matched:
         - @ConditionalOnClass found required class 'org.springframework.web.servlet.config.annotation.WebMvcConfigurer' (OnClassCondition)

   LazyConnectionDataSourceConfiguration:
      Did not match:
         - @ConditionalOnProperty (spring.datasource.connection-fetch=lazy) did not find property 'spring.datasource.connection-fetch' (OnPropertyCondition)

   TestDatabaseAutoConfiguration#dataSource:
      Did not match:
         - @ConditionalOnProperty (spring.test.database.replace=AUTO_CONFIGURED) did not find property 'spring.test.database.replace' (OnPropertyCondition)

   TestDatabaseAutoConfiguration#embeddedDataSourceBeanFactoryPostProcessor:
      Did not match:
         - @ConditionalOnProperty (spring.test.database.replace=ANY) did not find property 'spring.test.database.replace' (OnPropertyCondition)

   TransactionAutoConfiguration#transactionalOperator:
      Did not match:
         - @ConditionalOnSingleCandidate (types: org.springframework.transaction.ReactiveTransactionManager; SearchStrategy: all) did not find any beans (OnBeanCondition)

   TransactionAutoConfiguration.AspectJTransactionManagementConfiguration:
      Did not match:
         - @ConditionalOnBean (types: org.springframework.transaction.aspectj.AbstractTransactionAspect; SearchStrategy: all) did not find any beans of type org.springframework.transaction.aspectj.AbstractTransactionAspect (OnBeanCondition)

   TransactionAutoConfiguration.EnableTransactionManagementConfiguration.JdkDynamicAutoProxyConfiguration:
      Did not match:
         - @ConditionalOnBooleanProperty (spring.aop.proxy-target-class=false) did not find property 'spring.aop.proxy-target-class' (OnPropertyCondition)


Exclusions:
-----------

    None


Unconditional classes:
----------------------

    org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration



2026-11-04T08:25:27.671Z  INFO 2611 --- [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2026-11-04T08:25:27.673Z ERROR 2611 --- [           main] o.s.b.d.LoggingFailureAnalysisReporter   : 

***************************
APPLICATION FAILED TO START
***************************

Description:

Parameter 2 of constructor in com.senacor.freighttenders.tender.TenderService required a bean of type 'jakarta.validation.Validator' that could not be found.


Action:

Consider defining a bean of type 'jakarta.validation.Validator' in your configuration.

2026-11-04T08:25:27.673Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@2c32bf87]

java.lang.IllegalStateException: Failed to load ApplicationContext for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:195) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.cache.DefaultContextCache.put(DefaultContextCache.java:214) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:160) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.TenderService': Unsatisfied dependency expressed through constructor parameter 2: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:804) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:240) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1380) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1219) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:565) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:525) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:333) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:371) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:331) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:196) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.instantiateSingleton(DefaultListableBeanFactory.java:1225) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingleton(DefaultListableBeanFactory.java:1191) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:1121) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:994) ~[spring-context-7.0.9.jar:7.0.9]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:621) ~[spring-context-7.0.9.jar:7.0.9]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:756) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:445) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:321) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader.lambda$loadContext$2(SpringBootContextLoader.java:155) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:58) ~[spring-core-7.0.9.jar:7.0.9]
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:46) ~[spring-core-7.0.9.jar:7.0.9]
	at org.springframework.boot.SpringApplication.withHook(SpringApplication.java:1465) ~[spring-boot-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader$ContextLoaderHook.run(SpringBootContextLoader.java:600) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:155) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:114) ~[spring-boot-test-4.1.1.jar:4.1.1]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContextInternal(DefaultCacheAwareContextLoaderDelegate.java:247) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:167) ~[spring-test-7.0.9.jar:7.0.9]
	... 86 common frames omitted
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:912) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:791) ~[spring-beans-7.0.9.jar:7.0.9]
	... 112 common frames omitted

2026-11-04T08:25:27.679Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@ebfa509]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:27.682Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@24a99b1c]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:27.684Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@71280545]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:27.686Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@281dfc79]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:27.690Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@3c52060]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

2026-11-04T08:25:27.693Z  WARN 2611 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@4a73cc75]

java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260) ~[spring-test-7.0.9.jar:7.0.9]
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242) ~[spring-test-7.0.9.jar:7.0.9]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$1(ClassBasedTestDescriptor.java:423) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.executeAndMaskThrowable(ClassBasedTestDescriptor.java:428) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$invokeTestInstancePostProcessors$0(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214) ~[na:na]
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153) ~[na:na]
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176) ~[na:na]
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265) ~[na:na]
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.invokeTestInstancePostProcessors(ClassBasedTestDescriptor.java:422) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$instantiateAndPostProcessTestInstance$0(ClassBasedTestDescriptor.java:334) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.instantiateAndPostProcessTestInstance(ClassBasedTestDescriptor.java:333) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$1(ClassBasedTestDescriptor.java:322) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.Optional.orElseGet(Optional.java:364) ~[na:na]
	at org.junit.jupiter.engine.descriptor.ClassBasedTestDescriptor.lambda$testInstancesProvider$0(ClassBasedTestDescriptor.java:321) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.execution.TestInstancesProvider.getTestInstances(TestInstancesProvider.java:27) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.lambda$prepare$0(TestMethodTestDescriptor.java:127) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:126) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.jupiter.engine.descriptor.TestMethodTestDescriptor.prepare(TestMethodTestDescriptor.java:70) ~[junit-jupiter-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$prepare$0(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.prepare(NodeTestTask.java:144) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:110) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604) ~[na:na]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.invokeAll(SameThreadHierarchicalTestExecutorService.java:42) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$2(NodeTestTask.java:180) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$1(NodeTestTask.java:166) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.Node.around(Node.java:138) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.lambda$executeRecursively$0(NodeTestTask.java:164) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.ThrowableCollector.execute(ThrowableCollector.java:74) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.executeRecursively(NodeTestTask.java:163) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.NodeTestTask.execute(NodeTestTask.java:116) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.SameThreadHierarchicalTestExecutorService.submit(SameThreadHierarchicalTestExecutorService.java:36) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestExecutor.execute(HierarchicalTestExecutor.java:52) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.engine.support.hierarchical.HierarchicalTestEngine.execute(HierarchicalTestEngine.java:58) ~[junit-platform-engine-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.executeEngine(EngineExecutionOrchestrator.java:246) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.failOrExecuteEngine(EngineExecutionOrchestrator.java:218) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:179) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:108) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.lambda$execute$0(EngineExecutionOrchestrator.java:66) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.withInterceptedStreams(EngineExecutionOrchestrator.java:157) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.EngineExecutionOrchestrator.execute(EngineExecutionOrchestrator.java:65) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:125) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DefaultLauncher.execute(DefaultLauncher.java:114) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.lambda$execute$2(InterceptingLauncher.java:57) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.ClasspathAlignmentCheckingLauncherInterceptor.intercept(ClasspathAlignmentCheckingLauncherInterceptor.java:25) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.InterceptingLauncher.execute(InterceptingLauncher.java:56) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at org.junit.platform.launcher.core.DelegatingLauncher.execute(DelegatingLauncher.java:58) ~[junit-platform-launcher-6.0.3.jar:6.0.3]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:565) ~[na:na]
	at org.apache.maven.surefire.api.util.ReflectionUtils.invokeMethodWithArray(ReflectionUtils.java:125) ~[surefire-api-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.executeWithCancellationToken(LauncherAdapter.java:68) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.LauncherAdapter.execute(LauncherAdapter.java:54) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.execute(JUnitPlatformProvider.java:203) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invokeAllTests(JUnitPlatformProvider.java:168) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.junitplatform.JUnitPlatformProvider.invoke(JUnitPlatformProvider.java:136) ~[surefire-junit-platform-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:385) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.execute(ForkedBooter.java:162) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.run(ForkedBooter.java:507) ~[surefire-booter-3.5.6.jar:3.5.6]
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:495) ~[surefire-booter-3.5.6.jar:3.5.6]

[ERROR] Tests run: 7, Failures: 0, Errors: 7, Skipped: 0, Time elapsed: 0.291 s <<< FAILURE! -- in com.senacor.freighttenders.tender.DemoDataSeederTest
[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.awardedAndClosedTendersMatchWhatTheServiceProduces -- Time elapsed: 0.001 s <<< ERROR!
java.lang.IllegalStateException: Failed to load ApplicationContext for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:195)
	at org.springframework.test.context.cache.DefaultContextCache.put(DefaultContextCache.java:214)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:160)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.TenderService': Unsatisfied dependency expressed through constructor parameter 2: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:804)
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:240)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1380)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1219)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:565)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:525)
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:333)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:371)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:331)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:196)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.instantiateSingleton(DefaultListableBeanFactory.java:1225)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingleton(DefaultListableBeanFactory.java:1191)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:1121)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:994)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:621)
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:756)
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:445)
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:321)
	at org.springframework.boot.test.context.SpringBootContextLoader.lambda$loadContext$2(SpringBootContextLoader.java:155)
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:58)
	at org.springframework.util.function.ThrowingSupplier.get(ThrowingSupplier.java:46)
	at org.springframework.boot.SpringApplication.withHook(SpringApplication.java:1465)
	at org.springframework.boot.test.context.SpringBootContextLoader$ContextLoaderHook.run(SpringBootContextLoader.java:600)
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:155)
	at org.springframework.boot.test.context.SpringBootContextLoader.loadContext(SpringBootContextLoader.java:114)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContextInternal(DefaultCacheAwareContextLoaderDelegate.java:247)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.lambda$loadContext$0(DefaultCacheAwareContextLoaderDelegate.java:167)
	... 21 more
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'jakarta.validation.Validator' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:912)
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:791)
	... 47 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.seededTenderWithPassedDeadlineRejectsNewOffers -- Time elapsed: 0 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.bidDeadlinesAreRelativeToToday -- Time elapsed: 0.001 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.tendersCarryTheirSpecialFields -- Time elapsed: 0 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.runningAgainDoesNotSeedTwice -- Time elapsed: 0 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.hasRemarksAndOfferNotes -- Time elapsed: 0.002 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.seedsEightTendersWithTheExpectedStatuses -- Time elapsed: 0 s <<< ERROR!
java.lang.IllegalStateException: ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:157)
	at org.springframework.test.context.support.DefaultTestContext.getApplicationContext(DefaultTestContext.java:128)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:156)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.prepareTestInstance(DependencyInjectionTestExecutionListener.java:111)
	at org.springframework.test.context.TestContextManager.prepareTestInstance(TestContextManager.java:260)
	at org.springframework.test.context.junit.jupiter.SpringExtension.postProcessTestInstance(SpringExtension.java:242)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:186)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.stream.ReferencePipeline$2$1.accept(ReferencePipeline.java:197)
	at java.base/java.util.stream.ReferencePipeline$3$1.accept(ReferencePipeline.java:214)
	at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1716)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:570)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:153)
	at java.base/java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:176)
	at java.base/java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:265)
	at java.base/java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:632)
	at java.base/java.util.Optional.orElseGet(Optional.java:364)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)
	at java.base/java.util.ArrayList.forEach(ArrayList.java:1604)

[INFO] Running com.senacor.freighttenders.health.HealthControllerTest
2026-11-04T08:25:27.697Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:27.708Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest
2026-11-04T08:25:27.708Z  INFO 2611 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-11-04T08:25:27.711Z  INFO 2611 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-11-04T08:25:27.736Z  INFO 2611 --- [           main] c.s.f.health.HealthControllerTest        : Starting HealthControllerTest using Java 25.0.5 with PID 2611 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-11-04T08:25:27.737Z  INFO 2611 --- [           main] c.s.f.health.HealthControllerTest        : No active profile set, falling back to 1 default profile: "default"
2026-11-04T08:25:27.905Z  INFO 2611 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-11-04T08:25:27.905Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-11-04T08:25:27.906Z  INFO 2611 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-11-04T08:25:27.911Z  INFO 2611 --- [           main] c.s.f.health.HealthControllerTest        : Started HealthControllerTest in 0.196 seconds (process running for 9.149)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.231 s -- in com.senacor.freighttenders.health.HealthControllerTest
[INFO] 
[INFO] Results:
[INFO] 
[ERROR] Errors: 
[ERROR]   DemoDataSeederTest.awardedAndClosedTendersMatchWhatTheServiceProduces » IllegalState Failed to load ApplicationContext for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   DemoDataSeederTest.bidDeadlinesAreRelativeToToday » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   DemoDataSeederTest.hasRemarksAndOfferNotes » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   DemoDataSeederTest.runningAgainDoesNotSeedTwice » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   DemoDataSeederTest.seededTenderWithPassedDeadlineRejectsNewOffers » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   DemoDataSeederTest.seedsEightTendersWithTheExpectedStatuses » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   DemoDataSeederTest.tendersCarryTheirSpecialFields » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@4c08cf9b testClass = com.senacor.freighttenders.tender.DemoDataSeederTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = ["demo"], propertySourceDescriptors = [], propertySourceProperties = ["org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@55aa6fd0 key = [com.senacor.freighttenders.tender.DemoDataSeeder, org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   TenderServicePersistenceTest.addOfferAppendsTheNewOfferAsTheLastElementAfterRealPersistence » IllegalState Failed to load ApplicationContext for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   TenderServicePersistenceTest.addRemarkAppendsTheNewRemarkAsTheLastElementAfterRealPersistence » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   TenderServicePersistenceTest.awardedOfferPersistsAndReloads » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[ERROR]   TenderServicePersistenceTest.listingTendersFetchesOffersWithAConstantNumberOfQueries » IllegalState ApplicationContext failure threshold (1) exceeded: skipping repeated attempt to load context for [MergedContextConfiguration@12e8c5c4 testClass = com.senacor.freighttenders.tender.TenderServicePersistenceTest, locations = [], classes = [com.senacor.freighttenders.FreightTendersApplication], contextInitializerClasses = [], activeProfiles = [], propertySourceDescriptors = [], propertySourceProperties = ["spring.jpa.properties.hibernate.generate_statistics=true", "org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTestContextBootstrapper=true"], contextCustomizers = [[ImportsContextCustomizer@27a717a7 key = [org.springframework.boot.jdbc.autoconfigure.JdbcClientAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration, org.springframework.boot.hibernate.autoconfigure.HibernateJpaAutoConfiguration, org.springframework.boot.jpa.test.autoconfigure.TestEntityManagerAutoConfiguration, org.springframework.boot.transaction.autoconfigure.TransactionAutoConfiguration, com.senacor.freighttenders.tender.TenderService, org.springframework.boot.transaction.autoconfigure.TransactionManagerCustomizationAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceTransactionManagerAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.JdbcTemplateAutoConfiguration, org.springframework.boot.data.jpa.autoconfigure.DataJpaRepositoriesAutoConfiguration, org.springframework.boot.jdbc.autoconfigure.DataSourceInitializationAutoConfiguration, org.springframework.boot.jdbc.test.autoconfigure.TestDatabaseAutoConfiguration, com.senacor.freighttenders.tender.FixedClockConfiguration]], org.springframework.boot.test.context.PropertyMappingContextCustomizer@22fb5f05, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@590765c4, org.springframework.boot.test.context.filter.annotation.TypeExcludeFiltersContextCustomizer@34be3d80, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@577536e0, org.springframework.boot.test.autoconfigure.OnFailureConditionReportContextCustomizerFactory$OnFailureConditionReportContextCustomizer@7f0b93b4, org.springframework.boot.test.autoconfigure.OverrideAutoConfigurationContextCustomizerFactory$DisableAutoConfigurationContextCustomizer@4bc6da03, org.springframework.test.context.support.DynamicPropertiesContextCustomizer@0, org.springframework.boot.webmvc.test.autoconfigure.WebDriverContextCustomizer@3ba1308d, org.springframework.boot.web.server.context.SpringBootTestRandomPortContextCustomizer@36bed37a, org.springframework.boot.test.context.SpringBootTestAnnotation@820297cf], contextLoader = org.springframework.boot.test.context.SpringBootContextLoader, parent = null]
[INFO] 
[ERROR] Tests run: 128, Failures: 0, Errors: 11, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  12.634 s
[INFO] Finished at: 2026-11-04T08:25:28Z
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
