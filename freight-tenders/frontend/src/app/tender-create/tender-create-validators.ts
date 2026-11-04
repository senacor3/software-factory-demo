import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

// Client-side mirror of the backend's tender rules (CreateTenderRequestValidator). Dates are
// ISO yyyy-MM-dd strings, which compare correctly as plain strings.

export function todayIso(): string {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${now.getFullYear()}-${month}-${day}`;
}

function sibling(control: AbstractControl, name: string): unknown {
  return control.parent?.get(name)?.value;
}

function isFilled(value: unknown): value is string {
  return typeof value === 'string' && value !== '';
}

export const notBlank: ValidatorFn = (control) =>
  typeof control.value === 'string' && control.value.trim() === '' ? { required: true } : null;

export const integer: ValidatorFn = (control) =>
  typeof control.value === 'number' && !Number.isInteger(control.value)
    ? { integer: true }
    : null;

export const oneFractionDigit: ValidatorFn = (control) => {
  const value = control.value;
  return typeof value === 'number' && Math.abs(value * 10 - Math.round(value * 10)) > 1e-9
    ? { fractionDigits: true }
    : null;
};

// The dates of the tender being edited. A past date equal to the stored one is accepted, since
// the backend only applies the "today or later" rules to dates the update changes.
export interface LoadedDates {
  pickupDate: string;
  bidDeadline: string;
}

export function pickupNotInPastUnlessUnchanged(loaded: () => string | null): ValidatorFn {
  return (control) =>
    isFilled(control.value) && control.value < todayIso() && control.value !== loaded()
      ? { pickupInPast: true }
      : null;
}

export function deadlineNotInPastUnlessUnchanged(loaded: () => string | null): ValidatorFn {
  return (control) =>
    isFilled(control.value) && control.value < todayIso() && control.value !== loaded()
      ? { deadlineInPast: true }
      : null;
}

export const pickupNotInPast: ValidatorFn = pickupNotInPastUnlessUnchanged(() => null);

export const deliveryNotBeforePickup: ValidatorFn = (control) => {
  const pickup = sibling(control, 'pickupDate');
  return isFilled(control.value) && isFilled(pickup) && control.value < pickup
    ? { deliveryBeforePickup: true }
    : null;
};

export const deadlineNotInPast: ValidatorFn = deadlineNotInPastUnlessUnchanged(() => null);

export const deadlineNotAfterPickup: ValidatorFn = (control) => {
  const pickup = sibling(control, 'pickupDate');
  return isFilled(control.value) && isFilled(pickup) && control.value > pickup
    ? { deadlineAfterPickup: true }
    : null;
};

export const reeferWhenTemperatureControlled: ValidatorFn = (control) =>
  sibling(control, 'temperatureControlled') === true &&
  isFilled(control.value) &&
  control.value !== 'REEFER'
    ? { reeferRequired: true }
    : null;

export const temperatureRangeOrdered: ValidatorFn = (control): ValidationErrors | null => {
  const min = sibling(control, 'temperatureMinC');
  const max = sibling(control, 'temperatureMaxC');
  return typeof min === 'number' && typeof max === 'number' && min > max
    ? { temperatureOrder: true }
    : null;
};
