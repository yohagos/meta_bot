import { inject, Injectable } from '@angular/core';
import { GeneralChartService } from '../general-chart/general-chart.service';
import { TransactionRead } from '../../../services/models/transaction-read';

@Injectable({
  providedIn: 'root'
})
export class LinechartService {
  private _generalChartService = inject(GeneralChartService)

  _createLineChartForTransactions(transactions: TransactionRead[]) {
        var option = {
          title: {
            text: 'Transactions'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: this._generalChartService._retrieveTransactionNames(transactions)
          },
          grid: {
            left: '5%',
            right: '5%',
            bottom: '5%',
            containLabel: true
          },
          xAxis: {
            type: 'time',
          },
          yAxis: {
            type: 'value'
          },
          series: this._generalChartService._retrieveTransactionSeries(transactions),
          darkMode: true
        }

        return option
      }
}
