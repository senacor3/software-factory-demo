---
schema_version: 1
story_slug: seed-demo-tenders
stage: checks
status: findings-open
updated: 2026-10-13T14:39:31Z
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
[INFO] Recompiling the module because of changed source code.
[INFO] Compiling 33 source files with javac [debug parameters release 25] to target/classes
[INFO] 
[INFO] --- resources:3.5.0:testResources (default-testResources) @ freight-tenders-backend ---
[INFO] skip non existing resourceDirectory /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend/src/test/resources
[INFO] 
[INFO] --- compiler:3.15.0:testCompile (default-testCompile) @ freight-tenders-backend ---
[INFO] Recompiling the module because of changed dependency.
[INFO] Compiling 11 source files with javac [debug parameters release 25] to target/test-classes
[INFO] 
[INFO] --- surefire:3.5.6:test (default-test) @ freight-tenders-backend ---
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.senacor.freighttenders.tender.DemoDataSeederTest
14:39:21.241 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
14:39:21.526 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest
14:39:21.529 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils -- Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoDataSeederTest]: DemoDataSeederTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
14:39:21.549 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper -- Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoDataSeederTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:22.026Z  INFO 3008 --- [           main] c.s.f.tender.DemoDataSeederTest          : Starting DemoDataSeederTest using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:22.028Z  INFO 3008 --- [           main] c.s.f.tender.DemoDataSeederTest          : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:39:22.455Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:39:22.532Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 66 ms. Found 1 JPA repository interface.
2026-10-13T14:39:22.592Z  INFO 3008 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-10-13T14:39:22.762Z  INFO 3008 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:2d498338-425a-4056-b237-e0ed4435299a;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-10-13T14:39:23.043Z  INFO 3008 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:39:23.081Z  INFO 3008 --- [           main] org.hibernate.orm.core                   : HHH000001: Hibernate ORM core version 7.4.5.Final
2026-10-13T14:39:23.416Z  INFO 3008 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:39:23.500Z  INFO 3008 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:2d498338-425a-4056-b237-e0ed4435299a]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 2D498338-425A-4056-B237-E0ED4435299A/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:39:24.352Z  INFO 3008 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-10-13T14:39:24.411Z  INFO 3008 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:39:24.500Z  INFO 3008 --- [           main] o.s.d.j.r.query.QueryEnhancerFactories   : Hibernate is in classpath; If applicable, HQL parser will be used.
2026-10-13T14:39:24.716Z  INFO 3008 --- [           main] c.s.f.tender.DemoDataSeederTest          : Started DemoDataSeederTest in 3.098 seconds (process running for 4.779)
2026-10-13T14:39:24.721Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@381c826c]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

2026-10-13T14:39:24.749Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@7859fc7]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

2026-10-13T14:39:24.758Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@5da799]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

2026-10-13T14:39:24.768Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@46c92d27]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

2026-10-13T14:39:24.799Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@4e797a39]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

2026-10-13T14:39:24.810Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@147203c2]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

2026-10-13T14:39:24.819Z  WARN 3008 --- [           main] o.s.test.context.TestContextManager      : Caught exception while allowing TestExecutionListener [org.springframework.test.context.support.DependencyInjectionTestExecutionListener] to prepare test instance [com.senacor.freighttenders.tender.DemoDataSeederTest@6ccfce5a]

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157) ~[spring-test-7.0.9.jar:7.0.9]
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658) ~[spring-beans-7.0.9.jar:7.0.9]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764) ~[spring-beans-7.0.9.jar:7.0.9]
	... 88 common frames omitted

[ERROR] Tests run: 7, Failures: 0, Errors: 7, Skipped: 0, Time elapsed: 3.798 s <<< FAILURE! -- in com.senacor.freighttenders.tender.DemoDataSeederTest
[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.awardedAndClosedTendersMatchWhatTheServiceProduces -- Time elapsed: 0.010 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.seededTenderWithPassedDeadlineRejectsNewOffers -- Time elapsed: 0.001 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.bidDeadlinesAreRelativeToToday -- Time elapsed: 0.001 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.tendersCarryTheirSpecialFields -- Time elapsed: 0.005 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.runningAgainDoesNotSeedTwice -- Time elapsed: 0.001 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.hasRemarksAndOfferNotes -- Time elapsed: 0.002 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[ERROR] com.senacor.freighttenders.tender.DemoDataSeederTest.seedsEightTendersWithTheExpectedStatuses -- Time elapsed: 0.002 s <<< ERROR!
org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:767)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:748)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:146)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessProperties(AutowiredAnnotationBeanPostProcessor.java:493)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1444)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireBeanProperties(AbstractAutowireCapableBeanFactory.java:402)
	at org.springframework.test.context.support.DependencyInjectionTestExecutionListener.injectDependencies(DependencyInjectionTestExecutionListener.java:157)
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
Caused by: org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.raiseNoMatchingBeanFound(DefaultListableBeanFactory.java:2304)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1732)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1658)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.resolveFieldValue(AutowiredAnnotationBeanPostProcessor.java:764)
	... 23 more

[INFO] Running com.senacor.freighttenders.tender.TenderServicePersistenceTest
2026-10-13T14:39:24.845Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:24.863Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest
2026-10-13T14:39:24.864Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderServicePersistenceTest]: TenderServicePersistenceTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:24.873Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderServicePersistenceTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:24.909Z  INFO 3008 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Starting TenderServicePersistenceTest using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:24.909Z  INFO 3008 --- [           main] c.s.f.t.TenderServicePersistenceTest     : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:39:25.056Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:39:25.078Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 18 ms. Found 1 JPA repository interface.
2026-10-13T14:39:25.095Z  INFO 3008 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-10-13T14:39:25.107Z  INFO 3008 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:3cf76e79-6e95-45ef-a003-90cbb4745493;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-10-13T14:39:25.132Z  INFO 3008 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:39:25.155Z  INFO 3008 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:39:25.157Z  INFO 3008 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:3cf76e79-6e95-45ef-a003-90cbb4745493]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: 3CF76E79-6E95-45EF-A003-90CBB4745493/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:39:25.234Z  INFO 3008 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-10-13T14:39:25.246Z  INFO 3008 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:39:25.314Z  INFO 3008 --- [           main] c.s.f.t.TenderServicePersistenceTest     : Started TenderServicePersistenceTest in 0.432 seconds (process running for 5.376)
Mockito is currently self-attaching to enable the inline-mock-maker. This will no longer work in future releases of the JDK. Please add Mockito as an agent to your build as described in Mockito's documentation: https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html#0.3
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
WARNING: A Java agent has been loaded dynamically (/home/runner/.m2/repository/net/bytebuddy/byte-buddy-agent/1.18.11/byte-buddy-agent-1.18.11.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
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
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.291 s -- in com.senacor.freighttenders.tender.TenderServicePersistenceTest
[INFO] Running com.senacor.freighttenders.tender.TenderRepositoryTest
2026-10-13T14:39:26.132Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:26.143Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest
2026-10-13T14:39:26.144Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderRepositoryTest]: TenderRepositoryTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:26.153Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderRepositoryTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:26.192Z  INFO 3008 --- [           main] c.s.f.tender.TenderRepositoryTest        : Starting TenderRepositoryTest using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:26.192Z  INFO 3008 --- [           main] c.s.f.tender.TenderRepositoryTest        : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:39:26.283Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:39:26.292Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 7 ms. Found 1 JPA repository interface.
2026-10-13T14:39:26.305Z  INFO 3008 --- [           main] beddedDataSourceBeanFactoryPostProcessor : Replacing 'dataSource' DataSource bean with embedded version
2026-10-13T14:39:26.314Z  INFO 3008 --- [           main] o.s.j.d.e.EmbeddedDatabaseFactory        : Starting embedded database: url='jdbc:h2:mem:e64c5732-95ed-4a88-a0f7-93dcbd575f4a;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=false', username='sa'
2026-10-13T14:39:26.332Z  INFO 3008 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:39:26.351Z  INFO 3008 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:39:26.353Z  INFO 3008 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:e64c5732-95ed-4a88-a0f7-93dcbd575f4a]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
	Default catalog/schema: E64C5732-95ED-4A88-A0F7-93DCBD575F4A/PUBLIC
	Autocommit mode: undefined/unknown
	Isolation level: READ_COMMITTED [default READ_COMMITTED]
	JDBC fetch size: 100
	Pool: DataSourceConnectionProvider
	Minimum pool size: undefined/unknown
	Maximum pool size: undefined/unknown
2026-10-13T14:39:26.421Z  INFO 3008 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
Hibernate: create table offer (id bigint generated by default as identity, amount numeric(38,2), delivery_date date, note varchar(255), supplier_name varchar(255), valid_until date, tender_id bigint, primary key (id))
Hibernate: create table remark (id bigint generated by default as identity, text varchar(255), tender_id bigint, primary key (id))
Hibernate: create table tender (id bigint generated by default as identity, adr_class varchar(255), bid_deadline date, commodity varchar(255), currency enum ('CHF','CZK','DKK','EUR','GBP','PLN','SEK'), dangerous_goods boolean not null, delivery_date date, destination_country varchar(255), destination_postal_code varchar(255), destination_city varchar(255), equipment_type enum ('BOX','CURTAIN_SIDER','FLATBED','MEGA_TRAILER','REEFER'), loading_meters numeric(3,1), origin_country varchar(255), origin_postal_code varchar(255), origin_city varchar(255), pallet_count integer, pickup_date date, status enum ('AWARDED','CLOSED','OPEN'), temperature_controlled boolean not null, temperature_maxc integer, temperature_minc integer, weight_kg integer, awarded_offer_id bigint, primary key (id))
Hibernate: alter table if exists offer add constraint FK9ellj02i4t2gjbtedvhhy29a6 foreign key (tender_id) references tender
Hibernate: alter table if exists remark add constraint FKp4ny4jy2vvl8qd96dcbnc4kyb foreign key (tender_id) references tender
Hibernate: alter table if exists tender add constraint FKkcg3b0y15nrtsqx3bu0wnji2n foreign key (awarded_offer_id) references offer
2026-10-13T14:39:26.431Z  INFO 3008 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:39:26.482Z  INFO 3008 --- [           main] c.s.f.tender.TenderRepositoryTest        : Started TenderRepositoryTest in 0.325 seconds (process running for 6.545)
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
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.735 s -- in com.senacor.freighttenders.tender.TenderRepositoryTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-10-13T14:39:26.874Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:26.878Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
2026-10-13T14:39:26.883Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile]: WithDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:26.883Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:26.886Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:26.935Z  INFO 3008 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Starting DemoProfileGatingTest.WithDemoProfile using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:26.935Z  INFO 3008 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : The following 1 profile is active: "demo"
2026-10-13T14:39:27.182Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:39:27.190Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 6 ms. Found 1 JPA repository interface.
2026-10-13T14:39:27.364Z  INFO 3008 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:39:27.386Z  INFO 3008 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:39:27.389Z  INFO 3008 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2026-10-13T14:39:27.403Z  INFO 3008 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection conn17: url=jdbc:h2:mem:freighttenders user=SA
2026-10-13T14:39:27.405Z  INFO 3008 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2026-10-13T14:39:27.418Z  INFO 3008 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
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
2026-10-13T14:39:27.520Z  INFO 3008 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-10-13T14:39:27.548Z  INFO 3008 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:39:27.705Z  WARN 3008 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-10-13T14:39:28.091Z  INFO 3008 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:39:28.091Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:39:28.093Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 2 ms
2026-10-13T14:39:28.111Z  INFO 3008 --- [           main] .t.DemoProfileGatingTest$WithDemoProfile : Started DemoProfileGatingTest.WithDemoProfile in 1.216 seconds (process running for 8.174)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.467 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithDemoProfile
[INFO] Running com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-10-13T14:39:28.341Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:28.343Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
2026-10-13T14:39:28.344Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile]: WithoutDemoProfile does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:28.344Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.DemoProfileGatingTest]: DemoProfileGatingTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:28.345Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:28.371Z  INFO 3008 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Starting DemoProfileGatingTest.WithoutDemoProfile using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:28.371Z  INFO 3008 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:39:28.506Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-10-13T14:39:28.513Z  INFO 3008 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 6 ms. Found 1 JPA repository interface.
2026-10-13T14:39:28.572Z  INFO 3008 --- [           main] org.hibernate.orm.jpa                    : HHH008540: Processing PersistenceUnitInfo [name: default]
2026-10-13T14:39:28.591Z  INFO 3008 --- [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-10-13T14:39:28.591Z  INFO 3008 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Starting...
2026-10-13T14:39:28.593Z  INFO 3008 --- [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-2 - Added connection conn27: url=jdbc:h2:mem:freighttenders user=SA
2026-10-13T14:39:28.593Z  INFO 3008 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-2 - Start completed.
2026-10-13T14:39:28.593Z  INFO 3008 --- [           main] org.hibernate.orm.connections.pooling    : HHH10001005: Database info:
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
2026-10-13T14:39:28.668Z  INFO 3008 --- [           main] org.hibernate.orm.core                   : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-10-13T14:39:28.687Z  INFO 3008 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-10-13T14:39:28.740Z  WARN 3008 --- [           main] JpaBaseConfiguration$JpaWebConfiguration : spring.jpa.open-in-view is enabled by default. Therefore, database queries may be performed during view rendering. Explicitly configure spring.jpa.open-in-view to disable this warning
2026-10-13T14:39:28.833Z  INFO 3008 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:39:28.834Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:39:28.835Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-10-13T14:39:28.842Z  INFO 3008 --- [           main] DemoProfileGatingTest$WithoutDemoProfile : Started DemoProfileGatingTest.WithoutDemoProfile in 0.493 seconds (process running for 8.905)

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
[ERROR] Tests run: 1, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 0.542 s <<< FAILURE! -- in com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile
[ERROR] com.senacor.freighttenders.tender.DemoProfileGatingTest.seederBeanIsAbsentAndNoTendersExist -- Time elapsed: 0.036 s <<< FAILURE!
java.lang.AssertionError: JSON path "$.length()" expected:<0> but was:<8>
	at org.springframework.test.util.AssertionErrors.fail(AssertionErrors.java:62)
	at org.springframework.test.util.AssertionErrors.assertEquals(AssertionErrors.java:129)
	at org.springframework.test.util.JsonPathExpectationsHelper.assertValue(JsonPathExpectationsHelper.java:172)
	at org.springframework.test.web.servlet.result.JsonPathResultMatchers.lambda$value$2(JsonPathResultMatchers.java:111)
	at org.springframework.test.web.servlet.MockMvc$1.andExpect(MockMvc.java:212)
	at com.senacor.freighttenders.tender.DemoProfileGatingTest$WithoutDemoProfile.seederBeanIsAbsentAndNoTendersExist(DemoProfileGatingTest.java:35)

[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.016 s -- in com.senacor.freighttenders.tender.DemoProfileGatingTest
[INFO] Running com.senacor.freighttenders.tender.TenderServiceTest
[INFO] Tests run: 20, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.285 s -- in com.senacor.freighttenders.tender.TenderServiceTest
[INFO] Running com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-10-13T14:39:29.183Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:29.194Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest
2026-10-13T14:39:29.195Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderCreateValidationTest]: TenderCreateValidationTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:29.199Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderCreateValidationTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:29.253Z  INFO 3008 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Starting TenderCreateValidationTest using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:29.253Z  INFO 3008 --- [           main] c.s.f.tender.TenderCreateValidationTest  : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:39:29.604Z  INFO 3008 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:39:29.604Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:39:29.606Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 2 ms
2026-10-13T14:39:29.620Z  INFO 3008 --- [           main] c.s.f.tender.TenderCreateValidationTest  : Started TenderCreateValidationTest in 0.388 seconds (process running for 9.683)
[INFO] Tests run: 58, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.333 s -- in com.senacor.freighttenders.tender.TenderCreateValidationTest
[INFO] Running com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 s -- in com.senacor.freighttenders.tender.ClockConfigurationTest
[INFO] Running com.senacor.freighttenders.tender.TenderControllerTest
2026-10-13T14:39:30.519Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:30.528Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
2026-10-13T14:39:30.528Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.tender.TenderControllerTest]: TenderControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:30.535Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.492 s -- in com.senacor.freighttenders.tender.TenderControllerTest
[INFO] Running com.senacor.freighttenders.health.HealthControllerTest
2026-10-13T14:39:31.011Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:31.024Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest
2026-10-13T14:39:31.024Z  INFO 3008 --- [           main] t.c.s.AnnotationConfigContextLoaderUtils : Could not detect default configuration classes for test class [com.senacor.freighttenders.health.HealthControllerTest]: HealthControllerTest does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
2026-10-13T14:39:31.030Z  INFO 3008 --- [           main] .b.t.c.SpringBootTestContextBootstrapper : Found @SpringBootConfiguration com.senacor.freighttenders.FreightTendersApplication for test class com.senacor.freighttenders.health.HealthControllerTest

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-13T14:39:31.066Z  INFO 3008 --- [           main] c.s.f.health.HealthControllerTest        : Starting HealthControllerTest using Java 25.0.4.1 with PID 3008 (started by runner in /home/runner/work/software-factory-demo/software-factory-demo/freight-tenders/backend)
2026-10-13T14:39:31.066Z  INFO 3008 --- [           main] c.s.f.health.HealthControllerTest        : No active profile set, falling back to 1 default profile: "default"
2026-10-13T14:39:31.311Z  INFO 3008 --- [           main] o.s.b.t.m.w.SpringBootMockServletContext : Initializing Spring TestDispatcherServlet ''
2026-10-13T14:39:31.312Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Initializing Servlet ''
2026-10-13T14:39:31.313Z  INFO 3008 --- [           main] o.s.t.web.servlet.TestDispatcherServlet  : Completed initialization in 1 ms
2026-10-13T14:39:31.319Z  INFO 3008 --- [           main] c.s.f.health.HealthControllerTest        : Started HealthControllerTest in 0.285 seconds (process running for 11.382)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.329 s -- in com.senacor.freighttenders.health.HealthControllerTest
[INFO] 
[INFO] Results:
[INFO] 
[ERROR] Failures: 
[ERROR]   DemoProfileGatingTest.seederBeanIsAbsentAndNoTendersExist JSON path "$.length()" expected:<0> but was:<8>
[ERROR] Errors: 
[ERROR]   DemoDataSeederTest.awardedAndClosedTendersMatchWhatTheServiceProduces » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[ERROR]   DemoDataSeederTest.bidDeadlinesAreRelativeToToday » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[ERROR]   DemoDataSeederTest.hasRemarksAndOfferNotes » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[ERROR]   DemoDataSeederTest.runningAgainDoesNotSeedTwice » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[ERROR]   DemoDataSeederTest.seededTenderWithPassedDeadlineRejectsNewOffers » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[ERROR]   DemoDataSeederTest.seedsEightTendersWithTheExpectedStatuses » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[ERROR]   DemoDataSeederTest.tendersCarryTheirSpecialFields » UnsatisfiedDependency Error creating bean with name 'com.senacor.freighttenders.tender.DemoDataSeederTest': Unsatisfied dependency expressed through field 'seeder': No qualifying bean of type 'com.senacor.freighttenders.tender.DemoDataSeeder' available: expected at least 1 bean which qualifies as autowire candidate. Dependency annotations: {@org.springframework.beans.factory.annotation.Autowired(required=true)}
[INFO] 
[ERROR] Tests run: 127, Failures: 1, Errors: 7, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[ERROR] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  16.926 s
[INFO] Finished at: 2026-10-13T14:39:31Z
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
