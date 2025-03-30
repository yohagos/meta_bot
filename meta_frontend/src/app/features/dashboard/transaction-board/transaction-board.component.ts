import { CommonModule } from '@angular/common';
import { AfterContentChecked, AfterContentInit, Component, inject, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { SocketService } from '../services/socket.service';
import { BehaviorSubject, combineLatest, map, Observable, of, startWith } from 'rxjs';
import { TransactionRead } from '../../../services/models';
import { MatCardModule } from '@angular/material/card';
import { TextFormatPipe } from '../../../core/pipes/text-format.pipe';

@Component({
  selector: 'app-transaction-board',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,

    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatSelectModule,
    MatSortModule,
    MatProgressSpinnerModule,

    TextFormatPipe
  ],
  templateUrl: './transaction-board.component.html',
  styleUrl: './transaction-board.component.scss'
})
export class TransactionBoardComponent implements OnInit, AfterContentInit{
  txLoading = true
  private _socketService = inject(SocketService)

  transactions$ = this._socketService.getTransactions()

  private _filterSubject = new BehaviorSubject<string>('')
  filter$ = this._filterSubject.asObservable()

  filteredTransactions$: Observable<TransactionRead[]> = of([])

  ngOnInit(): void {
    this.filteredTransactions$ =  combineLatest([
      this.transactions$,
      this.filter$.pipe(startWith(''))
    ]).pipe(
      map(([transactions, filter]) => {
        const lowerFilter = filter.toLowerCase()

        return transactions.filter(item =>
          item.coin && item.coin.coin_name.toLowerCase().includes(lowerFilter)
        )
      })
    )
  }

  ngAfterContentInit(): void {
    //this.filteredTransactions$.subscribe(data => console.log(data))

  }


  /* styling functions */
  getScssClass(transactionType: string) {
    return `card-${transactionType.toLowerCase()}`
  }

}
