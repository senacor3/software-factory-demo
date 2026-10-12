import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';
import { TenderApiService } from '../tender-api';

const CREATE_ERROR_MESSAGE =
  'Die Ausschreibung konnte nicht erstellt werden. Bitte versuchen Sie es später erneut.';

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

  protected readonly form = this.formBuilder.nonNullable.group({
    origin: ['', Validators.required],
    destination: ['', Validators.required],
  });

  protected readonly submitError = signal<string | null>(null);
  protected readonly submitting = signal(false);

  protected onSubmit(): void {
    if (this.form.invalid) {
      return;
    }

    this.submitting.set(true);
    this.submitError.set(null);

    const { origin, destination } = this.form.getRawValue();

    this.tenderApi
      .create(origin, destination)
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
