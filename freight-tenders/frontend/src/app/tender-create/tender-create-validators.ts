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
  typeof control.value === 'number' && !Number.isInteger(control.value) ? { integer: true } : null;

export const oneFractionDigit: ValidatorFn = (control) => {
  const value = control.value;
  return typeof value === 'number' && Math.abs(value * 10 - Math.round(value * 10)) > 1e-9
    ? { fractionDigits: true }
    : null;
};

// A date in the past is an error, except an unchanged one: the edit form passes the stored value
// so a tender whose date has since passed can still be saved with that date left alone.
export function notInPast(error: string, stored: () => string | null = () => null): ValidatorFn {
  return (control) =>
    isFilled(control.value) && control.value < todayIso() && control.value !== stored()
      ? { [error]: true }
      : null;
}

export const pickupNotInPast: ValidatorFn = notInPast('pickupInPast');

export const deliveryNotBeforePickup: ValidatorFn = (control) => {
  const pickup = sibling(control, 'pickupDate');
  return isFilled(control.value) && isFilled(pickup) && control.value < pickup
    ? { deliveryBeforePickup: true }
    : null;
};

export const deadlineNotInPast: ValidatorFn = notInPast('deadlineInPast');

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
