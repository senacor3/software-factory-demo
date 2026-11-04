import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { LoadedDates } from '../tender-create/tender-create-validators';
import { TenderApiService, TenderDetail } from '../tender-api';
import {
  TenderForm,
  createTenderForm,
  toTenderRequest,
  wireTenderForm,
} from '../tender-form/tender-form';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibung wurde nicht gefunden oder konnte nicht geladen werden.';
const NOT_EDITABLE_MESSAGE =
  'Diese Ausschreibung ist nicht mehr offen und kann daher nicht mehr bearbeitet werden.';
const LOCKED_FIELDS_NOTICE =
  'Zu dieser Ausschreibung liegen bereits Angebote vor. Nur Zustellung und Angebotsfrist können noch geändert werden.';
const CONFLICT_ERROR_MESSAGE =
  'Die Ausschreibung kann nicht geändert werden: Sie ist nicht mehr offen oder die Änderung betrifft gesperrte Felder, zu denen bereits Angebote vorliegen.';
const SAVE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht gespeichert werden. Bitte versuchen Sie es später erneut.';

// With offers on the tender, only these two fields stay editable.
const EDITABLE_WITH_OFFERS = ['deliveryDate', 'bidDeadline'];

type SaveFailure = 'conflict' | 'failure';

@Component({
  selector: 'app-tender-edit',
  imports: [ReactiveFormsModule, RouterLink, TenderForm],
  templateUrl: './tender-edit.html',
  styleUrl: './tender-edit.scss',
})
export class TenderEdit implements OnInit {
  private readonly tenderApi = inject(TenderApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  // Declared before the form: its past-date validators read the loaded dates.
  private readonly loadedDates = signal<LoadedDates | null>(null);

  protected readonly form = createTenderForm(inject(FormBuilder), () => this.loadedDates());

  protected readonly tenderId = signal<number | null>(null);
  protected readonly tender = signal<TenderDetail | null>(null);
  protected readonly loading = signal(true);
  protected readonly loadError = signal<string | null>(null);
  protected readonly hasOffers = signal(false);
  protected readonly changed = signal(false);
  protected readonly submitting = signal(false);
  protected readonly submitError = signal<string | null>(null);
  protected readonly submitConflict = signal<string | null>(null);

  protected readonly notEditableMessage = NOT_EDITABLE_MESSAGE;
  protected readonly lockedFieldsNotice = LOCKED_FIELDS_NOTICE;

  private baseline = '';

  constructor() {
    wireTenderForm(this.form);

    this.form.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe(() => this.changed.set(this.snapshot() !== this.baseline));
  }

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = idParam === null ? NaN : Number(idParam);

    if (Number.isNaN(id)) {
      this.loading.set(false);
      this.loadError.set(LOAD_ERROR_MESSAGE);
      return;
    }

    this.tenderId.set(id);

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

        if (tender.status === 'OPEN') {
          this.prefill(tender);
        }
      });
  }

  protected onSubmit(): void {
    const id = this.tenderId();

    if (id === null || this.submitting() || !this.changed()) {
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting.set(true);
    this.submitError.set(null);
    this.submitConflict.set(null);

    this.tenderApi
      .update(id, toTenderRequest(this.form))
      .pipe(
        catchError((error: unknown) =>
          of<SaveFailure>(
            error instanceof HttpErrorResponse && error.status === 409 ? 'conflict' : 'failure',
          ),
        ),
      )
      .subscribe((result) => {
        this.submitting.set(false);

        if (result === 'conflict') {
          this.submitConflict.set(CONFLICT_ERROR_MESSAGE);
          return;
        }

        if (result === 'failure') {
          this.submitError.set(SAVE_ERROR_MESSAGE);
          return;
        }

        this.router.navigateByUrl(`/tenders/${id}`);
      });
  }

  private prefill(tender: TenderDetail): void {
    // Set first: the past-date validators accept these dates while they are unchanged.
    this.loadedDates.set({ pickupDate: tender.pickupDate, bidDeadline: tender.bidDeadline });

    // The checkboxes first, so the fields they switch on exist when their values arrive.
    this.form.patchValue({
      dangerousGoods: tender.dangerousGoods,
      temperatureControlled: tender.temperatureControlled,
    });
    this.form.patchValue({
      origin: tender.origin,
      destination: tender.destination,
      pickupDate: tender.pickupDate,
      deliveryDate: tender.deliveryDate,
      bidDeadline: tender.bidDeadline,
      commodity: tender.commodity,
      weightKg: tender.weightKg,
      loadingMeters: tender.loadingMeters,
      palletCount: tender.palletCount,
      equipmentType: tender.equipmentType,
      adrClass: tender.adrClass ?? '',
      temperatureMinC: tender.temperatureMinC,
      temperatureMaxC: tender.temperatureMaxC,
      currency: tender.currency,
    });

    if (tender.offers.length > 0) {
      this.hasOffers.set(true);
      this.form.disable();
      for (const name of EDITABLE_WITH_OFFERS) {
        this.form.get(name)?.enable();
      }
    }

    this.baseline = this.snapshot();
    this.changed.set(false);
  }

  // Raw value, so the locked (disabled) fields take part in the comparison.
  private snapshot(): string {
    return JSON.stringify(this.form.getRawValue());
  }
}
