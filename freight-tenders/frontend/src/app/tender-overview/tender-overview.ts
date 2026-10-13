import { Component, inject, OnInit, WritableSignal, computed, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import {
  SortAccessors,
  SortState,
  UNSORTED,
  ariaSort,
  sortIndicator,
  sortRows,
  toggleSort,
} from '../table-sort';
import { STATUS_LABELS, TenderApiService, TenderStatus, TenderSummary } from '../tender-api';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibungen konnten nicht geladen werden. Bitte versuchen Sie es später erneut.';

// Von and Nach show, and so sort by, the city of the address.
const SORT_ACCESSORS: SortAccessors<TenderSummary> = {
  origin: (tender) => tender.origin.city,
  destination: (tender) => tender.destination.city,
};

@Component({
  selector: 'app-tender-overview',
  imports: [RouterLink],
  templateUrl: './tender-overview.html',
  styleUrl: './tender-overview.scss',
})
export class TenderOverview implements OnInit {
  private readonly tenderApi = inject(TenderApiService);
  private readonly router = inject(Router);

  private readonly tenders = signal<TenderSummary[]>([]);
  protected readonly loadError = signal<string | null>(null);
  protected readonly loading = signal<boolean>(true);

  protected readonly statusLabels = STATUS_LABELS;
  protected readonly ariaSort = ariaSort;
  protected readonly sortIndicator = sortIndicator;

  protected readonly sortableColumns: { key: 'origin' | 'destination'; label: string }[] = [
    { key: 'origin', label: 'Von' },
    { key: 'destination', label: 'Nach' },
  ];

  protected readonly tables = [
    this.tenderTable(
      'open-tenders',
      'OPEN',
      'Offene Ausschreibungen',
      'Keine offenen Ausschreibungen vorhanden.',
    ),
    this.tenderTable(
      'closed-tenders',
      'CLOSED',
      'Geschlossene Ausschreibungen',
      'Keine geschlossenen Ausschreibungen vorhanden.',
    ),
  ];

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

        this.tenders.set(tenders);
      });
  }

  protected onSort(
    sort: WritableSignal<SortState<TenderSummary>>,
    column: keyof TenderSummary,
  ): void {
    sort.update((state) => toggleSort(state, column));
  }

  protected openTender(id: number, event: MouseEvent): void {
    // Only a plain primary click navigates in place: the row's own link handles clicks on itself,
    // modified or non-primary clicks are left alone, and so is the click that ends a text selection.
    if (
      (event.target instanceof Element && event.target.closest('a')) ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      window.getSelection()?.toString()
    ) {
      return;
    }

    this.router.navigate(['/tenders', id]);
  }

  // Each table keeps its own sort state, so sorting one never reorders the other.
  private tenderTable(testId: string, status: TenderStatus, heading: string, emptyMessage: string) {
    const sort = signal<SortState<TenderSummary>>(UNSORTED);
    const rows = computed(() =>
      sortRows(
        this.tenders().filter((tender) => tender.status === status),
        sort(),
        SORT_ACCESSORS,
      ),
    );

    return { testId, heading, emptyMessage, sort, rows };
  }
}
