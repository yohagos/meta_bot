import { inject, Injectable } from '@angular/core';
import { GeneralChartService } from '../general-chart/general-chart.service';
import { TransactionRead } from '../../../services/models/transaction-read';
import { TransactionTypeEnumMap } from '../../../features/dashboard/example.data';

@Injectable({
  providedIn: 'root'
})
export class PiechartService {
  pieChartOptions: any[] = []

  private _generaleChartService = inject(GeneralChartService)

  private _generatePieCharts(multiTransactions: TransactionRead[][]) {
    this.pieChartOptions = []
    for (let tx of multiTransactions) {
      var option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '5%',
          bottom: '10%',
          left: 'center'
        },
        series: [
          {
            name: 'US Dollar ',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '70%'],
            startAngle: 180,
            endAngle: 360,
            data: this._generateDataPieChart(tx)
          }
        ],
        darkMode: 'auto'
      }
      this.pieChartOptions.push(option)
    }

    return this.pieChartOptions
  }

  _generateDataPieChart(transactions: TransactionRead[]) {
      var sold = 0
      var soldAmount = 0
      var bought = 0
      var boughtAmount = 0
      var coin = ''
      transactions.forEach((element, index) => {
        if (index === 0) {
          coin = element.coin.coin_name
        }
        if (element.transaction_type === TransactionTypeEnumMap.SOLD) {
          sold += element.price
          soldAmount += element.amount
        } else  {
          bought += element.price
          boughtAmount += element.amount
        }
      })
      return [
        { value: sold.toFixed(3), name: `${coin} Sold` },
        { value: soldAmount.toFixed(3), name: `${coin} Amount Sold` },
        { value: bought.toFixed(3), name: `${coin} Bought` },
        { value: boughtAmount.toFixed(3), name: `${coin} Amount Bought` }
      ]
  }

  _createPieChartsTransaction(transactions: TransactionRead[]) {
    var distinctNames = this._generaleChartService._retrieveTransactionNames(transactions)

    var multiCoins: TransactionRead[][] = []

    distinctNames.forEach(item => {
      multiCoins.push(transactions.filter(element => element.coin.coin_name === item))
    })

    return this._generatePieCharts(multiCoins)
  }

}
