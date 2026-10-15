import { DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { AbstractControl, FormBuilder, ValidationErrors, Validators } from '@angular/forms';
import { CreateTenderRequest, Currency, EquipmentType } from '../tender-api';
import {
  deadlineNotAfterPickup,
  deliveryNotBeforePickup,
  integer,
  notBlank,
  notInPast,
  oneFractionDigit,
  reeferWhenTemperatureControlled,
  temperatureRangeOrdered,
} from '../tender-create/tender-create-validators';

export const FORM_ERROR_MESSAGES: Record<string, (error: ValidationErrors) => string> = {
  required: () => 'Dieses Feld ist erforderlich.',
  maxlength: (error) => `Es sind höchstens ${error['requiredLength']} Zeichen erlaubt.`,
  min: (error) => `Der Wert muss mindestens ${error['min']} betragen.`,
  max: (error) => `Der Wert darf höchstens ${error['max']} betragen.`,
  integer: () => 'Bitte geben Sie eine ganze Zahl ein.',
  fractionDigits: () => 'Es ist höchstens eine Nachkommastelle erlaubt.',
  pickupInPast: () => 'Die Abholung darf nicht in der Vergangenheit liegen.',
  deliveryBeforePickup: () => 'Die Zustellung darf nicht vor der Abholung liegen.',
  deadlineInPast: () => 'Die Angebotsfrist darf nicht in der Vergangenheit liegen.',
  deadlineAfterPickup: () => 'Die Angebotsfrist darf nicht nach der Abholung liegen.',
  temperatureOrder: () => 'Die Temperatur von darf nicht über der Temperatur bis liegen.',
  reeferRequired: () => 'Temperaturgeführte Ladung erfordert einen Kühlauflieger.',
};

// The dates an edited tender currently has: the "today or later" rules ignore them when unchanged.
export interface StoredDates {
  pickupDate: string | null;
  bidDeadline: string | null;
}

/**
 * The tender form shared by the create and edit pages: fields, validators and the wiring between
 * them. Must be called in an injection context.
 */
export function buildTenderForm(
  formBuilder: FormBuilder,
  stored: () => StoredDates = () => ({ pickupDate: null, bidDeadline: null }),
) {
  const destroyRef = inject(DestroyRef);

  const addressGroup = () =>
    formBuilder.nonNullable.group({
      country: ['DE', Validators.required],
      postalCode: ['', [Validators.required, notBlank, Validators.maxLength(10)]],
      city: ['', [Validators.required, notBlank, Validators.maxLength(100)]],
    });

  const form = formBuilder.nonNullable.group({
    origin: addressGroup(),
    destination: addressGroup(),
    pickupDate: ['', [Validators.required, notInPast('pickupInPast', () => stored().pickupDate)]],
    deliveryDate: ['', [Validators.required, deliveryNotBeforePickup]],
    commodity: ['', [Validators.required, notBlank, Validators.maxLength(200)]],
    weightKg: formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(1),
      Validators.max(40000),
      integer,
    ]),
    loadingMeters: formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(0.1),
      Validators.max(13.6),
      oneFractionDigit,
    ]),
    palletCount: formBuilder.control<number | null>(null, [
      Validators.min(1),
      Validators.max(66),
      integer,
    ]),
    dangerousGoods: [false],
    adrClass: ['', Validators.required],
    temperatureControlled: [false],
    temperatureMinC: formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(-30),
      Validators.max(30),
      integer,
      temperatureRangeOrdered,
    ]),
    temperatureMaxC: formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(-30),
      Validators.max(30),
      integer,
      temperatureRangeOrdered,
    ]),
    equipmentType: formBuilder.control<EquipmentType | ''>('', [
      Validators.required,
      reeferWhenTemperatureControlled,
    ]),
    bidDeadline: [
      '',
      [
        Validators.required,
        notInPast('deadlineInPast', () => stored().bidDeadline),
        deadlineNotAfterPickup,
      ],
    ],
    currency: formBuilder.control<Currency>('EUR', Validators.required),
  });

  const controls = form.controls;

  // ADR-Klasse and the temperature range exist only while their checkbox is checked: while
  // unchecked they are disabled (so they neither validate nor count) and cleared.
  controls.adrClass.disable();
  controls.temperatureMinC.disable();
  controls.temperatureMaxC.disable();

  const toggle = (checked: boolean, ...targets: AbstractControl[]) => {
    for (const control of targets) {
      if (checked) {
        control.enable();
      } else {
        control.reset();
        control.disable();
      }
    }
  };

  controls.dangerousGoods.valueChanges
    .pipe(takeUntilDestroyed(destroyRef))
    .subscribe((checked) => toggle(checked, controls.adrClass));
  controls.temperatureControlled.valueChanges
    .pipe(takeUntilDestroyed(destroyRef))
    .subscribe((checked) => toggle(checked, controls.temperatureMinC, controls.temperatureMaxC));

  // Cross-field rules sit on the field to fix, so that field is checked again whenever one it
  // depends on changes. Without emitting, two fields depending on each other cannot loop.
  const revalidateOnChange = (source: AbstractControl, ...targets: AbstractControl[]) => {
    source.valueChanges.pipe(takeUntilDestroyed(destroyRef)).subscribe(() => {
      for (const target of targets) {
        target.updateValueAndValidity({ emitEvent: false });
      }
    });
  };
  revalidateOnChange(controls.pickupDate, controls.deliveryDate, controls.bidDeadline);
  revalidateOnChange(controls.temperatureControlled, controls.equipmentType);
  revalidateOnChange(controls.temperatureMinC, controls.temperatureMaxC);
  revalidateOnChange(controls.temperatureMaxC, controls.temperatureMinC);

  return form;
}

export type TenderFormGroup = ReturnType<typeof buildTenderForm>;

// Only the values of the conditional fields whose checkbox is checked go into the request.
export function toTenderRequest(form: TenderFormGroup): CreateTenderRequest {
  const value = form.getRawValue();

  return {
    origin: value.origin,
    destination: value.destination,
    pickupDate: value.pickupDate,
    deliveryDate: value.deliveryDate,
    bidDeadline: value.bidDeadline,
    commodity: value.commodity,
    weightKg: value.weightKg as number,
    loadingMeters: value.loadingMeters as number,
    ...(value.palletCount === null ? {} : { palletCount: value.palletCount }),
    equipmentType: value.equipmentType as EquipmentType,
    dangerousGoods: value.dangerousGoods,
    ...(value.dangerousGoods ? { adrClass: value.adrClass } : {}),
    temperatureControlled: value.temperatureControlled,
    ...(value.temperatureControlled
      ? {
          temperatureMinC: value.temperatureMinC as number,
          temperatureMaxC: value.temperatureMaxC as number,
        }
      : {}),
    currency: value.currency as Currency,
  };
}
