import { Component, input, output } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  ADR_CLASSES,
  COUNTRY_LABELS,
  CURRENCIES,
  EQUIPMENT_LABELS,
  EquipmentType,
} from '../tender-api';
import { FORM_ERROR_MESSAGES, TenderFormGroup } from './tender-form-model';

/** The tender form card (fields, groups, messages and actions) shared by create and edit. */
@Component({
  selector: 'app-tender-form',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './tender-form.html',
  styleUrl: './tender-form.scss',
})
export class TenderForm {
  readonly form = input.required<TenderFormGroup>();
  readonly submitLabel = input.required<string>();
  readonly cancelLink = input.required<string>();
  readonly submitDisabled = input(false);
  readonly submitError = input<string | null>(null);
  readonly submitted = output<void>();

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

  // The first error message of a control that has been touched, or null.
  protected errorOf(path: string): string | null {
    const control = this.form().get(path);

    if (!control || !control.touched || !control.errors) {
      return null;
    }

    for (const [key, error] of Object.entries(control.errors)) {
      const message = FORM_ERROR_MESSAGES[key];
      if (message) {
        return message(error !== null && typeof error === 'object' ? error : {});
      }
    }

    return null;
  }
}
