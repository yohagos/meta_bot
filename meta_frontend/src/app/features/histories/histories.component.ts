import { CommonModule } from '@angular/common';
import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { HistoryService } from './services/history.service';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { BehaviorSubject, combineLatest, map, Observable, of, startWith } from 'rxjs';
import { CoinHistoryRead } from '../../services/models';

@Component({
  selector: 'app-histories',
  imports: [
    CommonModule,
    FormsModule,

    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSelectModule,
  ],
  templateUrl: './histories.component.html',
  styleUrl: './histories.component.scss'
})
export class HistoriesComponent implements OnInit, OnDestroy {
  limit = 30
  offset = 0
  loading = true

  private _historyService = inject(HistoryService)

  histories$ = this._historyService.getHistories(this.limit, this.offset)
  historyNames$ = new BehaviorSubject<string[]>([])

  private _filterSubject$ = new BehaviorSubject<string>('')
  filter$ = this._filterSubject$.asObservable()

  filteredHistories$: Observable<CoinHistoryRead[]> = of([])

  constructor() {
    this.filteredHistories$ = combineLatest([
      this.histories$,
      this.filter$.pipe(startWith(''))
    ]).pipe(
      map(([histories, filter]) => {
        const lowerFilter = filter.toLowerCase()

        return histories.filter(item =>
            item.coin.coin_name.toLowerCase().includes(lowerFilter))
      })
    )
  }

  ngOnInit(): void {
    this.histories$.pipe(
      map(items => items.map(item => item.coin.coin_name)),
      map(names => [...new Set(names)])
    ).subscribe(names => {
      this.historyNames$.next(names)
    })
  }

  applyFilter(item: string) {
    this._filterSubject$.next(item)
  }

  ngOnDestroy(): void {
      this.histories$ = of()
  }


  /* styling functions */

  getScssClass(transactionType: string) {
    return `card-title-${transactionType.toLowerCase()}`
  }
}
