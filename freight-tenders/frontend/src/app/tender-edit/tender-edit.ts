import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { TenderApiService, TenderDetail } from '../tender-api';
import { TenderForm } from '../tender-form/tender-form';
import { StoredDates, buildTenderForm, toTenderRequest } from '../tender-form/tender-form-model';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibung wurde nicht gefunden oder konnte nicht geladen werden.';
const NOT_EDITABLE_MESSAGE =
  'Diese Ausschreibung ist nicht mehr offen und kann daher nicht bearbeitet werden.';
const LOCKED_FIELDS_NOTICE =
  'Für diese Ausschreibung liegen bereits Angebote vor. Nur Zustellung bis und Angebotsfrist können noch geändert werden.';
const CONFLICT_MESSAGE =
  'Die Ausschreibung kann nicht mehr in dieser Form geändert werden, weil sie geschlossen oder vergeben wurde oder inzwischen Angebote vorliegen. Bitte laden Sie die Seite neu.';
const UPDATE_ERROR_MESSAGE =
  'Die Änderungen konnten nicht gespeichert werden. Bitte versuchen Sie es später erneut.';

// Fields that stay editable once a tender has offers.
const EDITABLE_WITH_OFFERS = ['deliveryDate', 'bidDeadline'] as const;

@Component({
  selector: 'app-tender-edit',
  imports: [RouterLink, TenderForm],
  templateUrl: './tender-edit.html',
})
export class TenderEdit implements OnInit {
  private readonly tenderApi = inject(TenderApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  private stored: StoredDates = { pickupDate: null, bidDeadline: null };

  protected readonly form = buildTenderForm(inject(FormBuilder), () => this.stored);

  protected readonly tender = signal<TenderDetail | null>(null);
  protected readonly loading = signal(true);
  protected readonly loadError = signal<string | null>(null);
  protected readonly editable = signal(true);
  protected readonly hasOffers = signal(false);
  protected readonly detailLink = signal('/');
  protected readonly submitting = signal(false);
  protected readonly submitError = signal<string | null>(null);

  protected readonly notEditableMessage = NOT_EDITABLE_MESSAGE;
  protected readonly lockedFieldsNotice = LOCKED_FIELDS_NOTICE;

  // The request the form produced right after loading, and a counter that changes with the form,
  // so "nothing changed yet" can be told without comparing field by field.
  private readonly initialRequest = signal<string | null>(null);
  private readonly formVersion = signal(0);
  protected readonly unchanged = computed(() => {
    this.formVersion();
    const initial = this.initialRequest();
    return initial === null || JSON.stringify(toTenderRequest(this.form)) === initial;
  });

  constructor() {
    this.form.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe(() => this.formVersion.update((version) => version + 1));
  }

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = idParam === null ? NaN : Number(idParam);

    if (Number.isNaN(id)) {
      this.loading.set(false);
      this.loadError.set(LOAD_ERROR_MESSAGE);
      return;
    }

    this.detailLink.set(`/tenders/${id}`);

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

        if (tender.status !== 'OPEN') {
          this.editable.set(false);
          return;
        }

        this.prefill(tender);
      });
  }

  protected onSubmit(): void {
    const current = this.tender();
    if (current === null || this.submitting()) {
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting.set(true);
    this.submitError.set(null);

    this.tenderApi
      .update(current.id, toTenderRequest(this.form))
      .pipe(
        catchError((error: unknown) =>
          of(error instanceof HttpErrorResponse && error.status === 409 ? 'conflict' : null),
        ),
      )
      .subscribe((result) => {
        this.submitting.set(false);

        if (result === 'conflict') {
          this.submitError.set(CONFLICT_MESSAGE);
          return;
        }

        if (result === null) {
          this.submitError.set(UPDATE_ERROR_MESSAGE);
          return;
        }

        this.router.navigateByUrl(`/tenders/${current.id}`);
      });
  }

  private prefill(tender: TenderDetail): void {
    const controls = this.form.controls;

    this.stored = { pickupDate: tender.pickupDate, bidDeadline: tender.bidDeadline };

    // The checkboxes first: checking one enables the conditional fields patched below.
    controls.dangerousGoods.setValue(tender.dangerousGoods);
    controls.temperatureControlled.setValue(tender.temperatureControlled);
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
      this.form.disable({ emitEvent: false });
      for (const name of EDITABLE_WITH_OFFERS) {
        controls[name].enable({ emitEvent: false });
      }
    }

    this.initialRequest.set(JSON.stringify(toTenderRequest(this.form)));
  }
}
