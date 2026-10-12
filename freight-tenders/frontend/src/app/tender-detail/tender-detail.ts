import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { catchError, of } from 'rxjs';
import { TenderApiService, TenderDetail as TenderDetailModel, TenderStatus } from '../tender-api';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibung wurde nicht gefunden oder konnte nicht geladen werden.';
const REMARK_ERROR_MESSAGE =
  'Die Bemerkung konnte nicht gespeichert werden. Bitte versuchen Sie es später erneut.';
const OFFER_ERROR_MESSAGE =
  'Das Angebot konnte nicht gespeichert werden. Bitte versuchen Sie es später erneut.';
const CLOSED_EXPLANATION =
  'Diese Ausschreibung ist geschlossen, daher können keine weiteren Bemerkungen oder Angebote hinzugefügt werden.';

const STATUS_LABELS: Record<TenderStatus, string> = {
  OPEN: 'Offen',
  CLOSED: 'Geschlossen',
};

@Component({
  selector: 'app-tender-detail',
  imports: [ReactiveFormsModule],
  templateUrl: './tender-detail.html',
  styleUrl: './tender-detail.scss',
})
export class TenderDetail implements OnInit {
  private readonly tenderApi = inject(TenderApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly formBuilder = inject(FormBuilder);

  protected readonly tender = signal<TenderDetailModel | null>(null);
  protected readonly loading = signal<boolean>(true);
  protected readonly loadError = signal<string | null>(null);

  protected readonly isClosed = computed(() => this.tender()?.status === 'CLOSED');
  protected readonly statusLabel = computed(() => {
    const current = this.tender();
    return current ? STATUS_LABELS[current.status] : '';
  });

  protected readonly closedExplanation = CLOSED_EXPLANATION;

  protected readonly remarkForm = this.formBuilder.nonNullable.group({
    text: ['', Validators.required],
  });
  protected readonly remarkError = signal<string | null>(null);

  protected readonly offerForm = this.formBuilder.group({
    supplierName: this.formBuilder.nonNullable.control('', Validators.required),
    amount: this.formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(0.01),
    ]),
  });
  protected readonly offerError = signal<string | null>(null);

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

        if (tender.status === 'CLOSED') {
          this.remarkForm.disable();
          this.offerForm.disable();
        }
      });
  }

  protected onAddRemark(): void {
    const current = this.tender();
    if (this.remarkForm.invalid || current === null) {
      return;
    }

    this.remarkError.set(null);
    const { text } = this.remarkForm.getRawValue();

    this.tenderApi
      .addRemark(current.id, text)
      .pipe(catchError(() => of(null)))
      .subscribe((remark) => {
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
    if (this.offerForm.invalid || current === null) {
      return;
    }

    this.offerError.set(null);
    const { supplierName, amount } = this.offerForm.getRawValue();

    this.tenderApi
      // `amount` is guaranteed non-null here: the required validator above already blocked
      // submission (the `offerForm.invalid` check) while it is null.
      .addOffer(current.id, supplierName, amount as number)
      .pipe(catchError(() => of(null)))
      .subscribe((offer) => {
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
