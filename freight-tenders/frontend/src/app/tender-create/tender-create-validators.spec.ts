import { FormControl } from '@angular/forms';
import {
  deadlineNotInPast,
  deadlineNotInPastUnlessUnchanged,
  pickupNotInPast,
  pickupNotInPastUnlessUnchanged,
} from './tender-create-validators';

describe('past-date validators', () => {
  const PAST = '2000-01-01';
  const OTHER_PAST = '2000-01-02';

  it('rejects a past pickup date and bid deadline when there is no loaded original', () => {
    expect(pickupNotInPast(new FormControl(PAST))).toEqual({ pickupInPast: true });
    expect(deadlineNotInPast(new FormControl(PAST))).toEqual({ deadlineInPast: true });
  });

  it('accepts a past pickup date equal to the loaded one and rejects a changed one', () => {
    const validator = pickupNotInPastUnlessUnchanged(() => PAST);

    expect(validator(new FormControl(PAST))).toBeNull();
    expect(validator(new FormControl(OTHER_PAST))).toEqual({ pickupInPast: true });
  });

  it('accepts a past bid deadline equal to the loaded one and rejects a changed one', () => {
    const validator = deadlineNotInPastUnlessUnchanged(() => PAST);

    expect(validator(new FormControl(PAST))).toBeNull();
    expect(validator(new FormControl(OTHER_PAST))).toEqual({ deadlineInPast: true });
  });

  it('accepts a future date whatever the loaded original is', () => {
    expect(pickupNotInPastUnlessUnchanged(() => null)(new FormControl('2099-01-01'))).toBeNull();
  });
});
