import { AfterContentInit, Component, inject, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { InterestService } from './services/interest.service';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { BehaviorSubject, combineLatest, map, Observable, of, startWith } from 'rxjs';
import { CoinInterestRead } from '../../services/models';
import { Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-interests',
  imports: [
    CommonModule,

    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './interests.component.html',
  styleUrl: './interests.component.scss'
})
export class InterestsComponent implements AfterContentInit, OnDestroy {
  offset = 0
  limit = 30

  loading = true
  private _router = inject(Router)

  private _interestService = inject(InterestService)
  interests$ = this._interestService.getInterests(this.limit, this.offset)
  private filterSubject = new BehaviorSubject<string>('')
  filter$ = this.filterSubject.asObservable()

  filteredInterests$: Observable<CoinInterestRead[]> =of([])

  constructor() {
    this.interests$.subscribe(() => this.loading = false)
  }

  ngAfterContentInit() {
    this.filteredInterests$ = combineLatest([
      this.interests$,
      this.filter$.pipe(startWith(''))
    ]).pipe(
      map(([interests, filter]) => {
        const lowerFilter = filter.toLowerCase()

        return interests.filter(item =>
          (item.coin && item.coin.coin_name.toLowerCase().includes(lowerFilter)) ||
          (item.stats && item.stats.name.toLowerCase().includes(lowerFilter))
        )
      })
    )
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value
    this.filterSubject.next(filterValue)
  }


  detailView(element: CoinInterestRead) {
    this._router.navigate(['interests', element.id])
  }

  clearFilter(element: HTMLInputElement) {
    element.value = ''
    this.filterSubject.next('')
  }

  ngOnDestroy() {
    this.filteredInterests$ = of([])
  }

}
