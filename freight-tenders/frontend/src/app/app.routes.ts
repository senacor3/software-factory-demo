import { Routes } from '@angular/router';
import { TenderCreate } from './tender-create/tender-create';
import { TenderDetail } from './tender-detail/tender-detail';
import { TenderOverview } from './tender-overview/tender-overview';

export const routes: Routes = [
  { path: '', component: TenderOverview },
  { path: 'tenders/new', component: TenderCreate },
  { path: 'tenders/:id', component: TenderDetail },
];
