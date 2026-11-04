import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { TenderApiService } from '../tender-api';
import {
  TenderForm,
  createTenderForm,
  toTenderRequest,
  wireTenderForm,
} from '../tender-form/tender-form';

const CREATE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht erstellt werden. Bitte versuchen Sie es später erneut.';

@Component({
  selector: 'app-tender-create',
  imports: [ReactiveFormsModule, RouterLink, TenderForm],
  templateUrl: './tender-create.html',
  styleUrl: './tender-create.scss',
})
export class TenderCreate {
  private readonly tenderApi = inject(TenderApiService);
  private readonly router = inject(Router);

  protected readonly form = createTenderForm(inject(FormBuilder));

  protected readonly submitError = signal<string | null>(null);
  protected readonly submitting = signal(false);

  constructor() {
    wireTenderForm(this.form);
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
