import { inject, Injectable } from '@angular/core';
import { SocketsService } from '../../../services/services';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private _socketApiService = inject(SocketsService)

  private _categorySubject = new BehaviorSubject<string[]>([])
  categories$ = this._categorySubject.asObservable()

  private _loadCategories() {
    this._socketApiService.consumerGroupsApiV1SocketsGroupsGet()
      .subscribe(
        (data: string[]) => {
          this._categorySubject.next(data)
    })
  }

  getCategories() {
    this._loadCategories()
    return this.categories$
  }

}
