import { inject, Injectable } from '@angular/core';
import { CoinsService } from '../../../services/services';
import { BehaviorSubject } from 'rxjs';
import { CoinRead } from '../../../services/models';
import { SnackbarService } from '../../../shared/services/snackbar.service';

@Injectable({
  providedIn: 'root'
})
export class CoinBehaviorService {
  private _snackbarService = inject(SnackbarService)
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
      error: (err: Error) => {
        this._snackbarService.openSnackBar(`${err.message}`, 'error')
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
