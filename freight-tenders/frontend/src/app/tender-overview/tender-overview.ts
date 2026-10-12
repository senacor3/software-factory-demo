import { Component, inject, OnInit, signal } from '@angular/core';
import { catchError, of } from 'rxjs';
import { TenderApiService, TenderSummary } from '../tender-api';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibungen konnten nicht geladen werden. Bitte versuchen Sie es später erneut.';

@Component({
  selector: 'app-tender-overview',
  imports: [],
  templateUrl: './tender-overview.html',
  styleUrl: './tender-overview.scss',
})
export class TenderOverview implements OnInit {
  private readonly tenderApi = inject(TenderApiService);

  protected readonly openTenders = signal<TenderSummary[]>([]);
  protected readonly closedTenders = signal<TenderSummary[]>([]);
  protected readonly loadError = signal<string | null>(null);
  protected readonly loading = signal<boolean>(true);

  ngOnInit(): void {
    this.tenderApi
      .list()
      .pipe(catchError(() => of(null)))
      .subscribe((tenders) => {
        this.loading.set(false);

        if (tenders === null) {
          this.loadError.set(LOAD_ERROR_MESSAGE);
          return;
        }

        this.openTenders.set(tenders.filter((tender) => tender.status === 'OPEN'));
        this.closedTenders.set(tenders.filter((tender) => tender.status === 'CLOSED'));
      });
  }
}
