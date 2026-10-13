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
import {
  EQUIPMENT_LABELS,
  STATUS_LABELS,
  TenderApiService,
  TenderStatus,
  TenderSummary,
} from '../tender-api';
import {
  cargoHint,
  deadlineHint,
  formatAmount,
  formatDate,
  formatLoadingMeters,
  formatWeight,
  localToday,
} from '../tender-format';

const LOAD_ERROR_MESSAGE =
  'Die Ausschreibungen konnten nicht geladen werden. Bitte versuchen Sie es später erneut.';

// Each column sorts by the underlying value of its first line: Von and Nach by city, the rest by
// their own property (ISO dates sort correctly as strings, weightKg and offerCount as numbers).
const SORT_ACCESSORS: SortAccessors<TenderSummary> = {
  origin: (tender) => tender.origin.city,
  destination: (tender) => tender.destination.city,
  status: (tender) => STATUS_LABELS[tender.status],
};

interface Column {
  key: keyof TenderSummary;
  label: string;
  sortable: boolean;
  numeric?: boolean;
}

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

  protected readonly equipmentLabels = EQUIPMENT_LABELS;
  protected readonly ariaSort = ariaSort;
  protected readonly sortIndicator = sortIndicator;
  protected readonly formatDate = formatDate;
  protected readonly formatWeight = formatWeight;
  protected readonly formatLoadingMeters = formatLoadingMeters;
  protected readonly formatAmount = formatAmount;
  protected readonly cargoHint = cargoHint;
  protected readonly deadlineHint = deadlineHint;

  // The browser's local date, read once per render pass of the template.
  protected today(): string {
    return localToday();
  }

  // Ladung sorts by weightKg and Angebote by offerCount; Fahrzeug is the one plain header.
  protected readonly columns: Column[] = [
    { key: 'origin', label: 'Von', sortable: true },
    { key: 'destination', label: 'Nach', sortable: true },
    { key: 'pickupDate', label: 'Abholung', sortable: true },
    { key: 'weightKg', label: 'Ladung', sortable: true },
    { key: 'equipmentType', label: 'Fahrzeug', sortable: false },
    { key: 'bidDeadline', label: 'Angebotsfrist', sortable: true },
    { key: 'offerCount', label: 'Angebote', sortable: true, numeric: true },
  ];

  protected readonly statusLabels = STATUS_LABELS;

  // The finished tenders table additionally tells awarded from closed ones apart.
  private readonly statusColumn: Column = {
    key: 'status',
    label: 'Status',
    sortable: true,
  };

  protected readonly tables = [
    this.tenderTable(
      'open-tenders',
      ['OPEN'],
      'Offene Ausschreibungen',
      'Keine offenen Ausschreibungen vorhanden.',
      this.columns,
    ),
    this.tenderTable(
      'closed-tenders',
      ['AWARDED', 'CLOSED'],
      'Abgeschlossene Ausschreibungen',
      'Keine abgeschlossenen Ausschreibungen vorhanden.',
      [...this.columns, this.statusColumn],
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
  private tenderTable(
    testId: string,
    statuses: TenderStatus[],
    heading: string,
    emptyMessage: string,
    columns: Column[],
  ) {
    const sort = signal<SortState<TenderSummary>>(UNSORTED);
    const rows = computed(() =>
      sortRows(
        this.tenders().filter((tender) => statuses.includes(tender.status)),
        sort(),
        SORT_ACCESSORS,
      ),
    );

    return { testId, heading, emptyMessage, columns, sort, rows };
  }
}
