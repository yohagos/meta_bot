import { inject, Injectable } from '@angular/core';
import { CoinInterestService } from '../../../services/services/coin-interest.service';
import { TokenService } from '../../../core/services/token.service';
import { CoinInterestCreate, CoinInterestRead, Stats } from '../../../services/models';
import { SnackbarService } from '../../../shared/services/snackbar.service';
import { BehaviorSubject } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class InterestService {
  private _snackbarService = inject(SnackbarService)
  private _interestApi = inject(CoinInterestService)
  private _tokenService = inject(TokenService)
  private _router = inject(Router)

  private _interestSubject = new BehaviorSubject<CoinInterestRead[]>([])
  interest$ = this._interestSubject.asObservable()

  addStatsCoin(
    stat: Stats
  ) {
    const userinfo = this._tokenService.getUserProfile()
    if (userinfo && userinfo?.sub) {
      let ci: CoinInterestCreate = {
        keycloak_user_id: userinfo.sub,
        stats_id: stat.data_id,
        coin_id: null
      }
      this._interestApi.addApiV1InterestCreatePost({
        body: ci
      }).subscribe({
        next: (data) => {
          this._snackbarService.openSnackBar(`Added ${data.stats_id} to favorites`, 'success')
        },
        error: (err: Error) => {
          this._snackbarService.openSnackBar(`Could not add ${stat.data_id} to favorites`, 'error')
        }
      })
    }
  }

  private _loadInterests(
    limit?: number,
    offset?: number
  ) {
    this._interestApi.getApiV1InterestGet({
      limit: limit,
      offset: offset
    }).subscribe({
      next: (data) => {
        this._interestSubject.next(data)
      },
      error: (err: Error) => {
        this._snackbarService.openSnackBar(`Could not load favorites`, 'error')
        this._router.navigate(['/overview'])
      }
    })
  }

  getInterests(
    limit?: number,
    offset?: number
  ) {
    this._loadInterests(limit, offset)
    return this.interest$
  }

  getInterestById(coin_id: string) {
    return this._interestApi.getByIdApiV1InterestCoinIdGet({coin_id})
  }

  checkExistence(element: Stats) {
    return this._interestSubject.value.some(
      item => item.stats?.symbol.toLowerCase() === element.symbol.toLowerCase() ||
              item.coin?.coin_symbol.toLowerCase() === element.symbol.toLowerCase()
    )
  }

  removeInterestById(element: Stats) {
    const data: CoinInterestRead | undefined = this._interestSubject.value.find(item =>
    {
      if (
        (item.coin && item.coin.coin_symbol.toLowerCase() === element.symbol.toLowerCase()) ||
        (item.stats && item.stats.symbol.toLowerCase() === element.symbol.toLowerCase())
      ) {
        return item
      }
      return
    }
    )
    if (data) {
      this._interestApi.deleteApiV1InterestDeleteCoinIdDelete({
        coin_id: data.id
      }).subscribe()
    }
    this._loadInterests()
  }
}
