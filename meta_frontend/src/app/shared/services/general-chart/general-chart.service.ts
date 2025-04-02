import { Injectable } from '@angular/core';

import { TransactionRead } from '../../../services/models';

export type ChartSeries = {
  name: string
  type: string
  step: string
  data: any[]
}

@Injectable({
  providedIn: 'root'
})
export class GeneralChartService {

  _retrieveTransactionNames(transactions: TransactionRead[]): string[] {
    var distinctNames: string[] = []

    var names = transactions.map(tx => tx.coin.coin_name)
    names.forEach(name => {
      if (!distinctNames.includes(name)) distinctNames.push(name)
    })
    return distinctNames
  }

  _retrieveTransactionSeries(transactions: TransactionRead[]): ChartSeries[] {
    const groups: { [coin_id: string]: ChartSeries} = {}
    transactions.forEach(tx => {
      const coin_id = tx.coin.coin_name
      const value = tx.transaction_type === 'SOLD' ? tx.amount : -tx.amount
      if (!groups[coin_id]) {
        groups[coin_id] = {
          name: coin_id,
          type: 'line',
          step: 'middle',
          data: []
        }
      }
      var time = Date.parse(tx.timestamp)
      groups[coin_id].data.push([time, value])
    })
    return Object.values(groups)
  }
}
