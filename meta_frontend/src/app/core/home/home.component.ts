import { CommonModule } from '@angular/common';
import { Component, inject, OnDestroy } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { NgxEchartsModule } from 'ngx-echarts';
import { ExamplesService } from './example/examples.service';
import { BehaviorSubject, interval, Subscription } from 'rxjs';
import { TransactionRead } from '../../services/models';
import { MatCardModule } from '@angular/material/card';
import { TextFormatPipe } from '../pipes/text-format.pipe';
import { PiechartService } from '../../shared/services/piechart/piechart.service';
import { ViewportTriggerDirective } from '../directives/viewport-trigger.directive';


@Component({
  selector: 'app-home',
  imports: [
    CommonModule,
    NgxEchartsModule,

    MatButtonModule,
    MatCardModule,

    TextFormatPipe,
    ViewportTriggerDirective,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnDestroy {
  private _examplesService = inject(ExamplesService)
  private _pieChartService = inject(PiechartService)

  chartTheme: string = 'dark'

  private _shortTransactionsSubject = new BehaviorSubject<TransactionRead[]>([])
  shortTransaction$ = this._shortTransactionsSubject.asObservable()
  chartOptions: any[] = []

  isArray = Array.isArray

  private _subscription: Subscription = interval(12000).subscribe(() => {
    var data = this._examplesService.generateData()

    const subTransactions = data.slice(0, 9)
    this._shortTransactionsSubject.next(subTransactions)

    this.chartOptions = this._pieChartService._createPieChartsTransaction(data)
  })

  getScssClass(transactionType: string) {
    return `card-${transactionType.toLowerCase()}`
  }

  ngOnDestroy(): void {
    this._subscription.unsubscribe()
  }

}
