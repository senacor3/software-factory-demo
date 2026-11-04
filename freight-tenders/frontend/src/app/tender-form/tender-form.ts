import { Component, OnInit, inject, input, output } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  AbstractControl,
  FormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  ADR_CLASSES,
  COUNTRY_LABELS,
  CURRENCIES,
  CreateTenderRequest,
  Currency,
  EQUIPMENT_LABELS,
  EquipmentType,
  TenderDetail,
} from '../tender-api';
import {
  deadlineNotAfterPickup,
  deadlineNotInPast,
  deliveryNotBeforePickup,
  integer,
  notBlank,
  oneFractionDigit,
  pickupNotInPast,
  reeferWhenTemperatureControlled,
  temperatureRangeOrdered,
} from '../tender-create/tender-create-validators';

const ERROR_MESSAGES: Record<string, (error: ValidationErrors) => string> = {
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

// With offers on the tender, only these two fields may still be changed.
const EDITABLE_WHEN_LOCKED = ['deliveryDate', 'bidDeadline'];

/**
 * The tender form shared by the create and edit pages: fields, validation and the request
 * mapping live here once. The host page owns the HTTP call and the submit/error state.
 */
@Component({
  selector: 'app-tender-form',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './tender-form.html',
  styleUrl: '../tender-create/tender-create.scss',
})
export class TenderForm implements OnInit {
  private readonly formBuilder = inject(FormBuilder);

  readonly mode = input<'create' | 'edit'>('create');
  // The loaded tender in edit mode; the form is prefilled from it.
  readonly initial = input<TenderDetail | null>(null);
  // True when the tender has offers: every field but the two dates is disabled.
  readonly lockedFields = input(false);
  readonly submitLabel = input('Erstellen');
  readonly cancelLink = input('/');
  readonly submitting = input(false);
  readonly submitError = input<string | null>(null);

  readonly submitted = output<CreateTenderRequest>();

  protected readonly countries = Object.entries(COUNTRY_LABELS).map(([code, label]) => ({
    code,
    label,
  }));
  protected readonly equipmentTypes = Object.entries(EQUIPMENT_LABELS).map(([code, label]) => ({
    code: code as EquipmentType,
    label,
  }));
  protected readonly currencies = CURRENCIES;
  protected readonly adrClasses = ADR_CLASSES;

  protected readonly form = this.formBuilder.nonNullable.group({
    origin: this.addressGroup(),
    destination: this.addressGroup(),
    pickupDate: [
      '',
      [Validators.required, pickupNotInPast(() => this.initial()?.pickupDate ?? null)],
    ],
    deliveryDate: ['', [Validators.required, deliveryNotBeforePickup]],
    commodity: ['', [Validators.required, notBlank, Validators.maxLength(200)]],
    weightKg: this.formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(1),
      Validators.max(40000),
      integer,
    ]),
    loadingMeters: this.formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(0.1),
      Validators.max(13.6),
      oneFractionDigit,
    ]),
    palletCount: this.formBuilder.control<number | null>(null, [
      Validators.min(1),
      Validators.max(66),
      integer,
    ]),
    dangerousGoods: [false],
    adrClass: ['', Validators.required],
    temperatureControlled: [false],
    temperatureMinC: this.formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(-30),
      Validators.max(30),
      integer,
      temperatureRangeOrdered,
    ]),
    temperatureMaxC: this.formBuilder.control<number | null>(null, [
      Validators.required,
      Validators.min(-30),
      Validators.max(30),
      integer,
      temperatureRangeOrdered,
    ]),
    equipmentType: this.formBuilder.control<EquipmentType | ''>('', [
      Validators.required,
      reeferWhenTemperatureControlled,
    ]),
    bidDeadline: [
      '',
      [
        Validators.required,
        deadlineNotInPast(() => this.initial()?.bidDeadline ?? null),
        deadlineNotAfterPickup,
      ],
    ],
    currency: this.formBuilder.control<Currency>('EUR', Validators.required),
  });

  // JSON of the request built from the loaded values; the edit form is saved only when different.
  private baseline: string | null = null;

  constructor() {
    const controls = this.form.controls;

    // ADR-Klasse and the temperature range exist only while their checkbox is checked: while
    // unchecked they are disabled (so they neither validate nor count) and cleared.
    controls.adrClass.disable();
    controls.temperatureMinC.disable();
    controls.temperatureMaxC.disable();

    controls.dangerousGoods.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe((checked) => this.toggle(checked, controls.adrClass));
    controls.temperatureControlled.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe((checked) =>
        this.toggle(checked, controls.temperatureMinC, controls.temperatureMaxC),
      );

    // Cross-field rules sit on the field to fix, so that field is checked again whenever one it
    // depends on changes. Without emitting, two fields depending on each other cannot loop.
    this.revalidateOnChange(controls.pickupDate, controls.deliveryDate, controls.bidDeadline);
    this.revalidateOnChange(controls.temperatureControlled, controls.equipmentType);
    this.revalidateOnChange(controls.temperatureMinC, controls.temperatureMaxC);
    this.revalidateOnChange(controls.temperatureMaxC, controls.temperatureMinC);
  }

  ngOnInit(): void {
    const tender = this.initial();
    if (this.mode() !== 'edit' || tender === null) {
      return;
    }

    const controls = this.form.controls;
    // The checkboxes first: checking one enables the conditional controls patched below.
    this.form.patchValue({
      dangerousGoods: tender.dangerousGoods,
      temperatureControlled: tender.temperatureControlled,
    });
    this.form.patchValue({
      origin: tender.origin,
      destination: tender.destination,
      pickupDate: tender.pickupDate,
      deliveryDate: tender.deliveryDate,
      commodity: tender.commodity,
      weightKg: tender.weightKg,
      loadingMeters: tender.loadingMeters,
      palletCount: tender.palletCount,
      adrClass: tender.adrClass ?? '',
      temperatureMinC: tender.temperatureMinC,
      temperatureMaxC: tender.temperatureMaxC,
      equipmentType: tender.equipmentType,
      bidDeadline: tender.bidDeadline,
      currency: tender.currency,
    });

    if (this.lockedFields()) {
      for (const [name, control] of Object.entries(controls)) {
        if (!EDITABLE_WHEN_LOCKED.includes(name)) {
          control.disable({ emitEvent: false });
        }
      }
    }

    this.baseline = JSON.stringify(this.toRequest());
    this.form.markAsPristine();
  }

  // The first error message of a control that has been touched, or null.
  protected errorOf(path: string): string | null {
    const control = this.form.get(path);

    if (!control || !control.touched || !control.errors) {
      return null;
    }

    for (const [key, error] of Object.entries(control.errors)) {
      const message = ERROR_MESSAGES[key];
      if (message) {
        return message(error !== null && typeof error === 'object' ? error : {});
      }
    }

    return null;
  }

  protected submitDisabled(): boolean {
    if (this.form.invalid || this.submitting()) {
      return true;
    }
    // Unchanged covers pristine: a form never touched still equals the loaded values.
    return this.mode() === 'edit' && this.isUnchanged();
  }

  private isUnchanged(): boolean {
    return this.baseline !== null && JSON.stringify(this.toRequest()) === this.baseline;
  }

  protected onSubmit(): void {
    if (this.submitting()) {
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    if (this.mode() === 'edit' && this.submitDisabled()) {
      return;
    }

    this.submitted.emit(this.toRequest());
  }

  private addressGroup() {
    return this.formBuilder.nonNullable.group({
      country: ['DE', Validators.required],
      postalCode: ['', [Validators.required, notBlank, Validators.maxLength(10)]],
      city: ['', [Validators.required, notBlank, Validators.maxLength(100)]],
    });
  }

  private toggle(checked: boolean, ...controls: AbstractControl[]): void {
    for (const control of controls) {
      if (checked) {
        control.enable();
      } else {
        control.reset();
        control.disable();
      }
    }
  }

  private revalidateOnChange(source: AbstractControl, ...targets: AbstractControl[]): void {
    source.valueChanges.pipe(takeUntilDestroyed()).subscribe(() => {
      for (const target of targets) {
        target.updateValueAndValidity({ emitEvent: false });
      }
    });
  }

  // Only the values of the conditional fields whose checkbox is checked go into the request.
  // getRawValue() includes disabled (locked) controls, so the request always carries every field.
  private toRequest(): CreateTenderRequest {
    const value = this.form.getRawValue();

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
}
