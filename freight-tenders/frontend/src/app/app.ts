import { Component } from '@angular/core';
import { TenderOverview } from './tender-overview/tender-overview';

@Component({
  selector: 'app-root',
  imports: [TenderOverview],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {}
