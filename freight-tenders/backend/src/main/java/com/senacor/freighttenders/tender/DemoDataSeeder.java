package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.LocalDate;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

/**
 * Seeds eight demo tenders at startup when the {@code demo} profile is active and the database is
 * empty. Data is built through the domain model and repository rather than the API, so a tender can
 * carry a bid deadline in the past and an already-expired offer without weakening any API
 * validation. Dates are relative to today (per the application {@link Clock}), so the data never
 * goes stale.
 */
@Component
@Profile("demo")
public class DemoDataSeeder implements ApplicationRunner {

  private final TenderRepository tenderRepository;

  private final TenderService tenderService;

  private final Clock clock;

  public DemoDataSeeder(
      TenderRepository tenderRepository, TenderService tenderService, Clock clock) {
    this.tenderRepository = tenderRepository;
    this.tenderService = tenderService;
    this.clock = clock;
  }

  @Override
  @Transactional
  public void run(ApplicationArguments args) {
    if (tenderRepository.count() > 0) {
      return;
    }
    LocalDate today = LocalDate.now(clock);

    // 1: open, one offer delivers after the requested delivery date
    Tender t1 =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("DE", "80331", "München"),
            today.plusDays(7),
            today.plusDays(9),
            today.plusDays(3),
            "Paletten mit Haushaltsgeräten",
            18000,
            new BigDecimal("13.6"),
            33,
            EquipmentType.CURTAIN_SIDER,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    t1.addOffer(
        new Offer(
            "Nordtrans GmbH",
            new BigDecimal("1450.00"),
            today.plusDays(9),
            today.plusDays(10),
            null));
    t1.addOffer(
        new Offer(
            "Bavaria Logistik AG",
            new BigDecimal("1380.00"),
            today.plusDays(10),
            today.plusDays(10),
            "Lieferung einen Tag später möglich, dafür günstiger."));
    t1.addRemark(new Remark("Anlieferung nur werktags zwischen 7 und 15 Uhr."));
    tenderRepository.save(t1);

    // 2: open, temperature-controlled with a reefer
    Tender t2 =
        new Tender(
            new Address("NL", "3011", "Rotterdam"),
            new Address("DE", "50667", "Köln"),
            today.plusDays(8),
            today.plusDays(9),
            today.plusDays(5),
            "Frische Milchprodukte",
            12000,
            new BigDecimal("7.2"),
            20,
            EquipmentType.REEFER,
            false,
            null,
            true,
            2,
            8,
            Currency.EUR);
    t2.addOffer(
        new Offer(
            "Kühlfracht Rhein GmbH",
            new BigDecimal("890.00"),
            today.plusDays(9),
            today.plusDays(6),
            "Kühlkette wird lückenlos dokumentiert."));
    t2.addOffer(
        new Offer(
            "FrostExpress BV",
            new BigDecimal("940.00"),
            today.plusDays(8),
            today.plusDays(7),
            null));
    t2.addRemark(new Remark("Temperaturprotokoll bei Übergabe erforderlich."));
    tenderRepository.save(t2);

    // 3: open, dangerous goods ADR class 3, bid deadline today
    Tender t3 =
        new Tender(
            new Address("DE", "67059", "Ludwigshafen"),
            new Address("FR", "67000", "Straßburg"),
            today.plusDays(4),
            today.plusDays(5),
            today,
            "Lösungsmittel in Fässern",
            15000,
            new BigDecimal("6.0"),
            24,
            EquipmentType.BOX,
            true,
            "3",
            false,
            null,
            null,
            Currency.EUR);
    t3.addOffer(
        new Offer(
            "ADR Spezialtransporte GmbH",
            new BigDecimal("720.00"),
            today.plusDays(5),
            today.plusDays(2),
            null));
    tenderRepository.save(t3);

    // 4: open, no pallet count
    Tender t4 =
        new Tender(
            new Address("DE", "70173", "Stuttgart"),
            new Address("AT", "1010", "Wien"),
            today.plusDays(10),
            today.plusDays(12),
            today.plusDays(7),
            "Stahlträger",
            24000,
            new BigDecimal("13.6"),
            null,
            EquipmentType.FLATBED,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    t4.addOffer(
        new Offer(
            "Alpen Cargo GmbH",
            new BigDecimal("1620.00"),
            today.plusDays(12),
            today.plusDays(9),
            "Inklusive Planen und Spanngurte."));
    tenderRepository.save(t4);

    // 5: open, bid deadline yesterday, one expired offer
    Tender t5 =
        new Tender(
            new Address("DE", "04109", "Leipzig"),
            new Address("PL", "00-001", "Warschau"),
            today.plusDays(2),
            today.plusDays(4),
            today.minusDays(1),
            "Autoteile",
            9000,
            new BigDecimal("8.0"),
            16,
            EquipmentType.MEGA_TRAILER,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    t5.addOffer(
        new Offer(
            "Polska Trans Sp. z o.o.",
            new BigDecimal("980.00"),
            today.plusDays(4),
            today.minusDays(1),
            "Angebot war nur bis gestern gültig."));
    t5.addOffer(
        new Offer(
            "Ostroute Logistik GmbH",
            new BigDecimal("1050.00"),
            today.plusDays(4),
            today.plusDays(3),
            null));
    tenderRepository.save(t5);

    // 6: open, quoted in CHF
    Tender t6 =
        new Tender(
            new Address("DE", "79098", "Freiburg"),
            new Address("CH", "8001", "Zürich"),
            today.plusDays(6),
            today.plusDays(7),
            today.plusDays(4),
            "Maschinenteile",
            7000,
            new BigDecimal("4.5"),
            10,
            EquipmentType.BOX,
            false,
            null,
            false,
            null,
            null,
            Currency.CHF);
    t6.addOffer(
        new Offer(
            "Helvetia Transport AG",
            new BigDecimal("840.00"),
            today.plusDays(7),
            today.plusDays(5),
            null));
    t6.addRemark(new Remark("Zollabfertigung erfolgt durch den Auftraggeber."));
    tenderRepository.save(t6);

    // 7: awarded to the lower offer
    Tender t7 =
        new Tender(
            new Address("DE", "28195", "Bremen"),
            new Address("DE", "01067", "Dresden"),
            today.plusDays(3),
            today.plusDays(4),
            today.minusDays(2),
            "Getränkekisten",
            20000,
            new BigDecimal("13.6"),
            33,
            EquipmentType.CURTAIN_SIDER,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    t7.addOffer(
        new Offer(
            "Elbe Frachtkontor GmbH",
            new BigDecimal("1100.00"),
            today.plusDays(4),
            today.plusDays(2),
            null));
    t7.addOffer(
        new Offer(
            "Hansa Spedition KG",
            new BigDecimal("1240.00"),
            today.plusDays(4),
            today.plusDays(2),
            null));
    t7.addRemark(new Remark("Zuschlag an den günstigeren Anbieter."));
    t7 = tenderRepository.save(t7);
    Offer lowerOffer =
        t7.getOffers().stream().min((a, b) -> a.getAmount().compareTo(b.getAmount())).orElseThrow();
    tenderService.awardTender(t7.getId(), lowerOffer.getId());

    // 8: closed without an award
    Tender t8 =
        new Tender(
            new Address("DE", "90402", "Nürnberg"),
            new Address("DE", "30159", "Hannover"),
            today.plusDays(5),
            today.plusDays(6),
            today.minusDays(3),
            "Büromöbel",
            5000,
            new BigDecimal("5.0"),
            12,
            EquipmentType.BOX,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    t8.addOffer(
        new Offer(
            "Franken Logistik GmbH",
            new BigDecimal("560.00"),
            today.plusDays(6),
            today.plusDays(1),
            null));
    t8.addRemark(new Remark("Transport wurde intern übernommen, Ausschreibung geschlossen."));
    t8 = tenderRepository.save(t8);
    tenderService.closeTender(t8.getId());
  }
}
