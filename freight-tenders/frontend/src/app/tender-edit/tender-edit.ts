import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { CreateTenderRequest, TenderApiService, TenderDetail } from '../tender-api';
import { TenderForm } from '../tender-form/tender-form';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibung wurde nicht gefunden oder konnte nicht geladen werden.';
const CONFLICT_MESSAGE =
  'Die Ausschreibung kann nicht mehr in dieser Form geändert werden. Bitte kehren Sie zur Ausschreibung zurück und prüfen Sie den aktuellen Stand.';
const SAVE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht gespeichert werden. Bitte versuchen Sie es später erneut.';

@Component({
  selector: 'app-tender-edit',
  imports: [RouterLink, TenderForm],
  templateUrl: './tender-edit.html',
})
export class TenderEdit implements OnInit {
  private readonly tenderApi = inject(TenderApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  // The raw route param, so the back link works even when it is not a number.
  protected readonly idParam = this.route.snapshot.paramMap.get('id') ?? '';
  protected readonly tender = signal<TenderDetail | null>(null);
  protected readonly loading = signal(true);
  protected readonly loadError = signal<string | null>(null);
  protected readonly submitting = signal(false);
  protected readonly submitError = signal<string | null>(null);

  protected readonly isOpen = computed(() => this.tender()?.status === 'OPEN');
  protected readonly hasOffers = computed(() => (this.tender()?.offers.length ?? 0) > 0);

  ngOnInit(): void {
    const id = this.idParam === '' ? NaN : Number(this.idParam);

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
      });
  }

  protected onSubmit(request: CreateTenderRequest): void {
    const current = this.tender();
    if (current === null || this.submitting()) {
      return;
    }

    this.submitting.set(true);
    this.submitError.set(null);

    this.tenderApi
      .update(current.id, request)
      .pipe(catchError((error: unknown) => of(error instanceof HttpErrorResponse ? error : null)))
      .subscribe((result) => {
        this.submitting.set(false);

        if (result === null || result instanceof HttpErrorResponse) {
          this.submitError.set(result?.status === 409 ? CONFLICT_MESSAGE : SAVE_ERROR_MESSAGE);
          return;
        }

        this.router.navigateByUrl(`/tenders/${current.id}`);
      });
  }
}
