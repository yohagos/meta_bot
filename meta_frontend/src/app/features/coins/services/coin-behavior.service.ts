import { inject, Injectable } from '@angular/core';
import { CoinsService } from '../../../services/services';
import { BehaviorSubject } from 'rxjs';
import { CoinRead } from '../../../services/models';

@Injectable({
  providedIn: 'root'
})
export class CoinBehaviorService {
  private _coinService = inject(CoinsService)

  private _coinBehavior = new BehaviorSubject<CoinRead[]>([])
  coinBehavior$ = this._coinBehavior.asObservable()

  private loadCoins(
    offset?: number,
    limit?: number
  ) {
    this._coinService.getApiV1CoinsGet({
      offset: offset,
      limit: limit
    }).subscribe({
      next: (data: CoinRead[]) => {
        this._coinBehavior.next(data)
      },
      error: (err) => {
        console.error(err)
      }
    })
  }

  getCoins(
    offset?: number,
    limit?: number
  ) {
    this.loadCoins(offset, limit)
    return this.coinBehavior$
  }
}
