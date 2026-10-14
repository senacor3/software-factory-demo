import { Component, inject, signal } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { catchError, of } from 'rxjs';
import { TenderApiService } from '../tender-api';
import { TenderForm } from '../tender-form/tender-form';
import { buildTenderForm, toTenderRequest } from '../tender-form/tender-form-model';

const CREATE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht erstellt werden. Bitte versuchen Sie es später erneut.';

@Component({
  selector: 'app-tender-create',
  imports: [TenderForm],
  templateUrl: './tender-create.html',
})
export class TenderCreate {
  private readonly tenderApi = inject(TenderApiService);
  private readonly router = inject(Router);

  protected readonly form = buildTenderForm(inject(FormBuilder));

  protected readonly submitError = signal<string | null>(null);
  protected readonly submitting = signal(false);

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
      .create(toTenderRequest(this.form))
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
}
