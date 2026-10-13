import {
  Component,
  ElementRef,
  Injector,
  OnInit,
  afterNextRender,
  computed,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { SortState, UNSORTED, ariaSort, sortIndicator, sortRows, toggleSort } from '../table-sort';
import {
  COUNTRY_LABELS,
  EQUIPMENT_LABELS,
  OfferSummary,
  RemarkSummary,
  STATUS_LABELS,
  TenderApiService,
  TenderDetail as TenderDetailModel,
} from '../tender-api';
import {
  deadlineHint,
  formatAmount,
  formatDate,
  formatLoadingMeters,
  formatTemperatureRange,
  formatWeight,
  isBidDeadlinePassed,
  isDeliveryLate,
  isOfferExpired,
  localToday,
} from '../tender-format';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibung wurde nicht gefunden oder konnte nicht geladen werden.';
const REMARK_ERROR_MESSAGE =
  'Die Bemerkung konnte nicht gespeichert werden. Bitte versuchen Sie es später erneut.';
const OFFER_ERROR_MESSAGE =
  'Das Angebot konnte nicht gespeichert werden. Bitte versuchen Sie es später erneut.';
const CLOSE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht geschlossen werden. Bitte versuchen Sie es später erneut.';
const CLOSED_EXPLANATION =
  'Diese Ausschreibung ist geschlossen, daher können keine weiteren Bemerkungen oder Angebote hinzugefügt werden.';

const BID_DEADLINE_PASSED_NOTICE =
  'Die Angebotsfrist ist abgelaufen, daher können keine weiteren Angebote abgegeben werden. Bemerkungen sind weiterhin möglich.';

const OFFER_FIELD_ERRORS: Record<string, Record<string, string>> = {
  supplierName: {
    required: 'Bitte geben Sie einen Anbieter an.',
    maxlength: 'Der Anbieter darf höchstens 100 Zeichen lang sein.',
  },
  amount: {
    required: 'Bitte geben Sie einen Betrag an.',
    min: 'Der Betrag muss größer als 0 sein.',
  },
  deliveryDate: {
    required: 'Bitte geben Sie ein Zustelldatum an.',
    beforePickup: 'Die Zustellung darf nicht vor der Abholung der Ausschreibung liegen.',
  },
  validUntil: {
    required: 'Bitte geben Sie an, bis wann das Angebot gültig ist.',
    inPast: 'Die Gültigkeit darf nicht in der Vergangenheit liegen.',
  },
  note: {
    maxlength: 'Der Hinweis darf höchstens 500 Zeichen lang sein.',
  },
};

const NO_INFO = 'Keine Angabe';

@Component({
  selector: 'app-tender-detail',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './tender-detail.html',
  styleUrl: './tender-detail.scss',
})
export class TenderDetail implements OnInit {
  private readonly tenderApi = inject(TenderApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly formBuilder = inject(FormBuilder);
  private readonly injector = inject(Injector);

  private readonly closedExplanationRef =
    viewChild<ElementRef<HTMLElement>>('closedExplanationRef');

  protected readonly tender = signal<TenderDetailModel | null>(null);
  protected readonly loading = signal<boolean>(true);
  protected readonly loadError = signal<string | null>(null);

  protected readonly closing = signal(false);
  protected readonly closeError = signal<string | null>(null);

  protected readonly isClosed = computed(() => this.tender()?.status === 'CLOSED');
  protected readonly statusLabel = computed(() => {
    const current = this.tender();
    return current ? STATUS_LABELS[current.status] : '';
  });

  protected readonly summaryLine = computed(() => {
    const current = this.tender();
    if (!current) {
      return '';
    }
    return [
      formatDate(current.pickupDate),
      formatDate(current.deliveryDate),
      EQUIPMENT_LABELS[current.equipmentType],
      formatWeight(current.weightKg),
    ].join(' · ');
  });

  protected readonly bidDeadlineText = computed(() => {
    const current = this.tender();
    if (!current) {
      return '';
    }
    const date = formatDate(current.bidDeadline);
    const hint = deadlineHint(current.bidDeadline, current.status, localToday());
    return hint ? `${date} (${hint})` : date;
  });

  protected readonly originCountry = computed(() =>
    this.countryLabel(this.tender()?.origin.country),
  );
  protected readonly destinationCountry = computed(() =>
    this.countryLabel(this.tender()?.destination.country),
  );
  protected readonly weightText = computed(() => formatWeight(this.tender()?.weightKg ?? 0));
  protected readonly loadingMetersText = computed(() =>
    formatLoadingMeters(this.tender()?.loadingMeters ?? 0),
  );
  protected readonly equipmentLabel = computed(() => {
    const current = this.tender();
    return current ? EQUIPMENT_LABELS[current.equipmentType] : '';
  });
  protected readonly palletText = computed(() => {
    const count = this.tender()?.palletCount;
    return count === null || count === undefined ? NO_INFO : String(count);
  });
  protected readonly dangerousGoodsText = computed(() => {
    const current = this.tender();
    if (!current?.dangerousGoods) {
      return 'Nein';
    }
    return current.adrClass ? `Ja, ADR-Klasse ${current.adrClass}` : 'Ja';
  });
  protected readonly temperatureText = computed(() => {
    const current = this.tender();
    if (
      !current?.temperatureControlled ||
      current.temperatureMinC === null ||
      current.temperatureMaxC === null
    ) {
      return 'Keine Vorgabe';
    }
    return formatTemperatureRange(current.temperatureMinC, current.temperatureMaxC);
  });

  protected readonly deadlinePassed = computed(() => {
    const current = this.tender();
    return (
      current !== null && isBidDeadlinePassed(current.bidDeadline, current.status, localToday())
    );
  });
  protected readonly deadlinePassedNotice = BID_DEADLINE_PASSED_NOTICE;

  protected readonly formatDate = formatDate;
  protected readonly isOfferExpired = isOfferExpired;
  protected readonly isDeliveryLate = isDeliveryLate;
  protected readonly localToday = localToday;
  protected readonly closedExplanation = CLOSED_EXPLANATION;
  protected readonly ariaSort = ariaSort;
  protected readonly sortIndicator = sortIndicator;

  protected readonly remarkSort = signal<SortState<RemarkSummary>>(UNSORTED);
  protected readonly sortedRemarks = computed(() =>
    sortRows(this.tender()?.remarks ?? [], this.remarkSort()),
  );

  protected readonly offerSort = signal<SortState<OfferSummary>>(UNSORTED);
  protected readonly sortedOffers = computed(() =>
    sortRows(this.tender()?.offers ?? [], this.offerSort()),
  );

  protected readonly remarkForm = this.formBuilder.nonNullable.group({
    text: ['', Validators.required],
  });
  protected readonly remarkError = signal<string | null>(null);
  protected readonly remarkSubmitting = signal(false);

  protected readonly offerForm = this.formBuilder.group({
    supplierName: this.formBuilder.nonNullable.control('', [
      Validators.required,
      Validators.maxLength(100),
    ]),
    amount: this.formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(0.01),
    ]),
    deliveryDate: this.formBuilder.nonNullable.control('', [
      Validators.required,
      (control) => this.deliveryNotBeforePickup(control),
    ]),
    validUntil: this.formBuilder.nonNullable.control('', [
      Validators.required,
      (control) => this.validUntilNotInPast(control),
    ]),
    note: this.formBuilder.nonNullable.control('', Validators.maxLength(500)),
  });
  protected readonly offerError = signal<string | null>(null);
  protected readonly offerSubmitting = signal(false);

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = idParam === null ? NaN : Number(idParam);

    if (Number.isNaN(id)) {
      this.loading.set(false);
      this.loadError.set(LOAD_ERROR_MESSAGE);
      return;
    }

    this.tenderApi
      .detail(id)
      .pipe(catchError(() => of(null)))
      .subscribe((tender) => {
        this.loading.set(false);

        if (tender === null) {
          this.loadError.set(LOAD_ERROR_MESSAGE);
          return;
        }

        this.tender.set(tender);
        this.offerForm.controls.deliveryDate.updateValueAndValidity();

        if (tender.status === 'CLOSED') {
          this.remarkForm.disable();
          this.offerForm.disable();
        } else if (this.deadlinePassed()) {
          this.offerForm.disable();
        }
      });
  }

  protected onSortRemarks(column: keyof RemarkSummary): void {
    this.remarkSort.update((state) => toggleSort(state, column));
  }

  protected onSortOffers(column: keyof OfferSummary): void {
    this.offerSort.update((state) => toggleSort(state, column));
  }

  protected offerErrorOf(field: keyof typeof OFFER_FIELD_ERRORS): string | null {
    const control = this.offerForm.get(field);

    if (!control || !control.touched || !control.errors) {
      return null;
    }

    for (const key of Object.keys(control.errors)) {
      const message = OFFER_FIELD_ERRORS[field][key];
      if (message) {
        return message;
      }
    }

    return null;
  }

  private deliveryNotBeforePickup(control: AbstractControl): ValidationErrors | null {
    const pickup = this.tender()?.pickupDate;
    return control.value && pickup && control.value < pickup ? { beforePickup: true } : null;
  }

  private validUntilNotInPast(control: AbstractControl): ValidationErrors | null {
    return control.value && control.value < localToday() ? { inPast: true } : null;
  }

  protected formatAmount(amount: number): string {
    const currency = this.tender()?.currency ?? 'EUR';
    return formatAmount(amount, currency);
  }

  private countryLabel(code: string | undefined): string {
    return code ? (COUNTRY_LABELS[code] ?? code) : '';
  }

  protected onClose(): void {
    const current = this.tender();
    if (current === null || this.closing()) {
      return;
    }

    this.closing.set(true);
    this.closeError.set(null);

    this.tenderApi
      .close(current.id)
      .pipe(catchError(() => of(null)))
      .subscribe((result) => {
        this.closing.set(false);

        if (result === null) {
          this.closeError.set(CLOSE_ERROR_MESSAGE);
          return;
        }

        // The response is a summary without remarks/offers, so merge only the status.
        this.tender.update((value) => value && { ...value, status: result.status });
        this.remarkForm.disable();
        this.offerForm.disable();

        // The close button (the focused element) is removed on this change; the explanation
        // only exists after the next render, so focus it then.
        afterNextRender(() => this.closedExplanationRef()?.nativeElement.focus(), {
          injector: this.injector,
        });
      });
  }

  protected onAddRemark(): void {
    const current = this.tender();
    if (this.remarkForm.invalid || current === null || this.remarkSubmitting()) {
      return;
    }

    this.remarkSubmitting.set(true);
    this.remarkError.set(null);
    const { text } = this.remarkForm.getRawValue();

    this.tenderApi
      .addRemark(current.id, text)
      .pipe(catchError(() => of(null)))
      .subscribe((remark) => {
        this.remarkSubmitting.set(false);

        if (remark === null) {
          this.remarkError.set(REMARK_ERROR_MESSAGE);
          return;
        }

        this.tender.update((value) =>
          value === null ? value : { ...value, remarks: [...value.remarks, remark] },
        );
        this.remarkForm.reset();
      });
  }

  protected onAddOffer(): void {
    const current = this.tender();
    if (this.offerForm.invalid || current === null || this.offerSubmitting()) {
      return;
    }

    this.offerSubmitting.set(true);
    this.offerError.set(null);
    const { supplierName, amount, deliveryDate, validUntil, note } = this.offerForm.getRawValue();

    this.tenderApi
      // `amount` is guaranteed non-null here: the required validator above already blocked
      // submission (the `offerForm.invalid` check) while it is null.
      .addOffer(current.id, {
        supplierName,
        amount: amount as number,
        deliveryDate,
        validUntil,
        ...(note.trim() === '' ? {} : { note }),
      })
      .pipe(catchError(() => of(null)))
      .subscribe((offer) => {
        this.offerSubmitting.set(false);

        if (offer === null) {
          this.offerError.set(OFFER_ERROR_MESSAGE);
          return;
        }

        this.tender.update((value) =>
          value === null ? value : { ...value, offers: [...value.offers, offer] },
        );
        this.offerForm.reset();
      });
  }
}
