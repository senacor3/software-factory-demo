export type SortDirection = 'ascending' | 'descending';

export interface SortState<T> {
  column: keyof T | null;
  direction: SortDirection;
}

export const UNSORTED = { column: null, direction: 'ascending' } as const;

export function toggleSort<T>(state: SortState<T>, column: keyof T): SortState<T> {
  if (state.column === column) {
    return { column, direction: state.direction === 'ascending' ? 'descending' : 'ascending' };
  }

  return { column, direction: 'ascending' };
}

// Reads the value a column sorts by, for columns whose displayed value is not the row's own
// property (e.g. a nested object).
export type SortAccessors<T> = Partial<Record<keyof T, (row: T) => unknown>>;

export function sortRows<T extends { id: number }>(
  rows: readonly T[],
  state: SortState<T>,
  accessors: SortAccessors<T> = {},
): T[] {
  const newestFirst = (a: T, b: T) => b.id - a.id;
  const { column, direction } = state;

  if (column === null) {
    return [...rows].sort(newestFirst);
  }

  const valueOf = accessors[column] ?? ((row: T) => row[column]);
  const sign = direction === 'ascending' ? 1 : -1;
  return [...rows].sort((a, b) => sign * compareValues(valueOf(a), valueOf(b)) || newestFirst(a, b));
}

export function ariaSort<T>(state: SortState<T>, column: keyof T): SortDirection | 'none' {
  return state.column === column ? state.direction : 'none';
}

export function sortIndicator<T>(state: SortState<T>, column: keyof T): '▲' | '▼' | null {
  if (state.column !== column) {
    return null;
  }

  return state.direction === 'ascending' ? '▲' : '▼';
}

function compareValues(a: unknown, b: unknown): number {
  if (typeof a === 'number' && typeof b === 'number') {
    return a - b;
  }

  return String(a).localeCompare(String(b), 'de');
}
