import { Component, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  AbstractControl,
  FormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import {
  ADR_CLASSES,
  COUNTRY_LABELS,
  CURRENCIES,
  CreateTenderRequest,
  Currency,
  EQUIPMENT_LABELS,
  EquipmentType,
  TenderApiService,
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
} from './tender-create-validators';

const CREATE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht erstellt werden. Bitte versuchen Sie es später erneut.';

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

@Component({
  selector: 'app-tender-create',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './tender-create.html',
  styleUrl: './tender-create.scss',
})
export class TenderCreate {
  private readonly tenderApi = inject(TenderApiService);
  private readonly router = inject(Router);
  private readonly formBuilder = inject(FormBuilder);

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
    pickupDate: ['', [Validators.required, pickupNotInPast]],
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
    bidDeadline: ['', [Validators.required, deadlineNotInPast, deadlineNotAfterPickup]],
    currency: this.formBuilder.control<Currency>('EUR', Validators.required),
  });

  protected readonly submitError = signal<string | null>(null);
  protected readonly submitting = signal(false);

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

  protected onSubmit(): void {
    if (this.submitting()) {
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting.set(true);
    this.submitError.set(null);

    this.tenderApi
      .create(this.toRequest())
      .pipe(catchError(() => of(null)))
      .subscribe((result) => {
        this.submitting.set(false);

        if (result === null) {
          this.submitError.set(CREATE_ERROR_MESSAGE);
          return;
        }

        this.router.navigateByUrl('/');
      });
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
