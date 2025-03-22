import { inject, Injectable } from '@angular/core';
import { CoinHistoryService } from '../../../services/services';
import { SnackbarService } from '../../../shared/services/snackbar.service';
import { BehaviorSubject } from 'rxjs';
import { CoinHistoryRead } from '../../../services/models';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  private _historyApi = inject(CoinHistoryService)
  private _snackbarService = inject(SnackbarService)

  private _historySubject = new BehaviorSubject<CoinHistoryRead[]>([])
  histories$ = this._historySubject.asObservable()

  private _loadHistories(
    limit?: number,
    offset?: number
  ) {
    this._historyApi.getApiV1HistoryGet({
      limit,
      offset
    }).subscribe({
      next: (data) => {
        this._historySubject.next(data)
      },
      error: (err) => {
        this._snackbarService.openSnackBar('Error while loading histories', 'error')
      }
    })
  }

  getHistories(
    limit?: number,
    offset?: number
  ) {
    this._loadHistories(limit, offset)
    return this.histories$
  }

  destroy() {
    this._historySubject.next([])
  }
}
