import { Injectable } from '@angular/core';
import { TransactionRead, CoinRead, TransactionTypeEnum } from '../../../services/models';


export const TransactionTypeEnumMap: Record<TransactionTypeEnum, TransactionTypeEnum> = {
  SOLD: "SOLD" as TransactionTypeEnum,
  BOUGHT: "BOUGHT" as TransactionTypeEnum
};

@Injectable({
  providedIn: 'root'
})
export class ExamplesService {
  private _exampleTransactions: TransactionRead[] = [
    {
      amount: 10,
      coin: {
        coin_name: 'Etherum',
        coin_symbol: 'ETH',
        created_date: new Date().toDateString(),
        description: null,
        id: '-',
        website: null
      },
      coin_id: '-',
      id: '-',
      keycloak_user_id: '-',
      price: 1000,
      timestamp: new Date().toDateString(),
      transaction_type: TransactionTypeEnumMap.SOLD,
      user: null
    },
    {
      amount: 10,
      coin: {
        coin_name: 'Bitcoin',
        coin_symbol: 'BTC',
        created_date: new Date().toDateString(),
        description: null,
        id: '-',
        website: null
      },
      coin_id: '-',
      id: '-',
      keycloak_user_id: '-',
      price: 3000,
      timestamp: new Date().toDateString(),
      transaction_type: TransactionTypeEnumMap.SOLD,
      user: null
    },
    {
      amount: 10,
      coin: {
        coin_name: 'XRP',
        coin_symbol: 'XRP',
        created_date: new Date().toDateString(),
        description: null,
        id: '-',
        website: null
      },
      coin_id: '-',
      id: '-',
      keycloak_user_id: '-',
      price: 900,
      timestamp: new Date().toDateString(),
      transaction_type: TransactionTypeEnumMap.SOLD,
      user: null
    }
  ]

  generateData() {
    const data = []
    const originalData = JSON.parse(JSON.stringify(this._exampleTransactions))

    for (let i = 0; i < 20; i++) {
      const tx = JSON.parse(JSON.stringify(
        originalData[Math.floor(Math.random() * originalData.length)]
      ))
      tx.price = this._generateRandomPrice(tx.price)
      tx.amount = this._generateRandomAmount(tx.amount)
      tx.transaction_type = this._randomTransactionType()
      data.push(tx)
    }
    return data
  }

  private _generateRandomPrice(val: number) {
    var min = val * 0.5
    var max = val * 1.5
    return Math.trunc(Math.floor(Math.random() * (max - min + 1)) + min)
  }

  private _generateRandomAmount(val: number) {
    var min = val - 5
    var max = val + 5
    return Math.floor(Math.random() * (max - min + 1)) + min
  }

  private _randomTransactionType() {
    const values = Object.keys(TransactionTypeEnumMap) as TransactionTypeEnum[]
    const randomIndex = Math.floor(Math.random() * values.length )
    return values[randomIndex]
  }
}
