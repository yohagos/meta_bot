import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { NavigationEnd, Router, RouterModule } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { CoinInterestRead } from '../../../services/models';
import { InterestService } from '../services/interest.service';
import { SnackbarService } from '../../../shared/services/snackbar.service';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-interest-detail',
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,

    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSelectModule,
  ],
  templateUrl: './interest-detail.component.html',
  styleUrl: './interest-detail.component.scss'
})
export class InterestDetailComponent {
  loading = true
  private _routerSnapshot = inject(Router)
  private _snackbarService = inject(SnackbarService)

  interest$ = new BehaviorSubject<CoinInterestRead | null>(null)
  private _interestService = inject(InterestService)

  currencies = ['USD', 'EUR']
  currency!: string

  constructor() {
    this._routerSnapshot.events.subscribe((data) => {
      if (data instanceof NavigationEnd) {
        const interestId = data.url.split('/')[2]
        if (interestId) {
          this._interestService.getInterestById(interestId).subscribe({
            next: (data) => {
              this.interest$.next(data)
              this.loading = false
            },
            error: (err: Error) => {
              this._snackbarService.openSnackBar(`Coin Id ${interestId} was not found`, 'error')
              this._routerSnapshot.navigate(['interests'])
            }
          })
        }
      }
    })
  }

  currencyFilter(desiredCurrency: string) {
    if (!this.currency || this.currency.length === 0) return true
    if (desiredCurrency === this.currency) return true
    return false
  }

  clearFilter() {
    this.currency = ''
  }
}
