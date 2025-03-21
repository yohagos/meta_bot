import { AfterViewInit, ChangeDetectionStrategy, ChangeDetectorRef, Component, inject, OnDestroy, signal, ViewChild } from '@angular/core';
import { CoinRead } from '../../services/models';


import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatTableDataSource, MatTableModule } from "@angular/material/table";
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { CoinBehaviorService } from './services/coin-behavior.service';
import { catchError, finalize, of, Subject, takeUntil } from 'rxjs';


@Component({
  selector: 'app-coins',
  imports: [
    CommonModule,

    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatPaginatorModule,
    MatSortModule,
    MatTableModule,

  ],
  templateUrl: './coins.component.html',
  styleUrl: './coins.component.scss',
})
export class CoinsComponent implements AfterViewInit, OnDestroy {
  private _coinBehaviorService = inject(CoinBehaviorService)
  coins$ = this._coinBehaviorService.getCoins()

  displayedColumns: string[] = [ 'coin_name', 'coin_symbol']
  displayedColumnsWithExpand = [...this.displayedColumns, 'expand']
  dataSource: MatTableDataSource<CoinRead> = new MatTableDataSource

  @ViewChild(MatPaginator) paginator!: MatPaginator
  @ViewChild(MatSort) sort!: MatSort

  expandedElementId!: string | null

  private destroy$ = new Subject<void>()

  isLoading = signal(true)

  constructor() {
    this.coins$
      .pipe(
        takeUntil(this.destroy$),
        catchError(err => {
          console.error("Error loading coins: ", err)
          return of([])
        }),
        finalize(() => this.isLoading.set(false))
      )
      .subscribe((data: CoinRead[]) => {
        this.dataSource.data = data
      })
  }

  ngAfterViewInit(): void {
      this.dataSource.paginator = this.paginator
      this.dataSource.sort = this.sort
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value
    this.dataSource.filter = filterValue.trim().toLowerCase()

    this.dataSource.filterPredicate = (data: CoinRead, filter: string) => {
      return data.coin_name.toLowerCase().includes(filter) ||
              data.coin_symbol.toLowerCase().includes(filter)
    }

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage()
    }
  }

  toggle(element: CoinRead) {
    console.log('toggle clicked')
    this.expandedElementId = this.isExpanded(element) ? null : element.id
  }

  isExpanded(element: CoinRead) {
    return this.expandedElementId === element.id
  }

  ngOnDestroy(): void {
      this.destroy$.next()
      this.destroy$.complete()
  }
}
