import { SortState, UNSORTED, ariaSort, sortIndicator, sortRows, toggleSort } from './table-sort';

interface Row {
  id: number;
  name: string;
  amount: number;
}

const ROWS: Row[] = [
  { id: 1, name: 'Zeppelin', amount: 980 },
  { id: 2, name: 'Ärmel', amount: 1234.56 },
  { id: 3, name: 'Bremen', amount: 99 },
];

function ids(rows: Row[]): number[] {
  return rows.map((row) => row.id);
}

describe('table-sort', () => {
  describe('toggleSort', () => {
    it('sorts ascending when an unsorted column is selected', () => {
      expect(toggleSort<Row>(UNSORTED, 'name')).toEqual({ column: 'name', direction: 'ascending' });
    });

    it('reverses to descending when the active column is selected again, and back again after that', () => {
      const descending = toggleSort<Row>({ column: 'name', direction: 'ascending' }, 'name');
      expect(descending).toEqual({ column: 'name', direction: 'descending' });
      expect(toggleSort(descending, 'name')).toEqual({ column: 'name', direction: 'ascending' });
    });

    it('starts ascending on the new column when a different column is selected', () => {
      expect(toggleSort<Row>({ column: 'name', direction: 'descending' }, 'amount')).toEqual({
        column: 'amount',
        direction: 'ascending',
      });
    });
  });

  describe('sortRows', () => {
    it('orders rows newest-first by id while no column is active', () => {
      expect(ids(sortRows(ROWS, UNSORTED))).toEqual([3, 2, 1]);
    });

    it('does not mutate the rows it is given', () => {
      sortRows(ROWS, { column: 'amount', direction: 'ascending' });

      expect(ids(ROWS)).toEqual([1, 2, 3]);
    });

    it('compares numbers numerically, not as strings', () => {
      const ascending = sortRows(ROWS, { column: 'amount', direction: 'ascending' });
      expect(ascending.map((row) => row.amount)).toEqual([99, 980, 1234.56]);

      const descending = sortRows(ROWS, { column: 'amount', direction: 'descending' });
      expect(descending.map((row) => row.amount)).toEqual([1234.56, 980, 99]);
    });

    it('compares strings by German collation, so an umlaut sorts next to its base letter', () => {
      const ascending = sortRows(ROWS, { column: 'name', direction: 'ascending' });
      expect(ascending.map((row) => row.name)).toEqual(['Ärmel', 'Bremen', 'Zeppelin']);

      const descending = sortRows(ROWS, { column: 'name', direction: 'descending' });
      expect(descending.map((row) => row.name)).toEqual(['Zeppelin', 'Bremen', 'Ärmel']);
    });

    it('keeps rows with equal values newest-first in both directions', () => {
      const rows: Row[] = [
        { id: 1, name: 'Hamburg', amount: 5 },
        { id: 2, name: 'Hamburg', amount: 5 },
        { id: 3, name: 'Aachen', amount: 5 },
      ];

      expect(ids(sortRows(rows, { column: 'name', direction: 'ascending' }))).toEqual([3, 2, 1]);
      expect(ids(sortRows(rows, { column: 'name', direction: 'descending' }))).toEqual([2, 1, 3]);
    });
  });

  describe('ariaSort and sortIndicator', () => {
    it('report none and no indicator for every column while nothing is sorted', () => {
      expect(ariaSort<Row>(UNSORTED, 'name')).toBe('none');
      expect(sortIndicator<Row>(UNSORTED, 'name')).toBeNull();
    });

    it('report the direction on the active column only', () => {
      const ascending: SortState<Row> = { column: 'name', direction: 'ascending' };
      expect(ariaSort(ascending, 'name')).toBe('ascending');
      expect(sortIndicator(ascending, 'name')).toBe('▲');
      expect(ariaSort(ascending, 'amount')).toBe('none');
      expect(sortIndicator(ascending, 'amount')).toBeNull();

      const descending: SortState<Row> = { column: 'name', direction: 'descending' };
      expect(ariaSort(descending, 'name')).toBe('descending');
      expect(sortIndicator(descending, 'name')).toBe('▼');
    });
  });
});
