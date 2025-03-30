import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { Stats, TransactionRead } from '../../../services/models';
import { BehaviorSubject } from 'rxjs';

export type DataMessage = Stats[] | TransactionRead[]

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  aggregateSubject$!: WebSocketSubject<any>

  private _transactionSubject: BehaviorSubject<TransactionRead[]> = new BehaviorSubject<TransactionRead[]>([])
  transactions$ = this._transactionSubject.asObservable()
  private _statsSubject: BehaviorSubject<Stats[]> = new BehaviorSubject<Stats[]>([])
  stats$ = this._statsSubject.asObservable()

  connect() {
    this.aggregateSubject$ = webSocket('ws://localhost:8000/api/v1/sockets/ws/all')
    this.aggregateSubject$.subscribe(
      message => this._handleData(message),
      err => console.error(err),
      () => console.warn('warning ')
    )
  }

  private _handleData(message: DataMessage) {
    if (!Array.isArray(message) || message.length === 0) {
      return
    }
    if ((message[0] as any).data_id !== undefined) {
      this._statsSubject.next(message as Stats[])
    } else if ((message[0] as any).keycloak_user_id !== undefined) {
      this._transactionSubject.next(message as TransactionRead[])
    }
  }

  getTransactions() {
    return this.transactions$
  }

  disconnect() {
    this.aggregateSubject$.complete()
    this._statsSubject.complete()
    this._transactionSubject.complete()
  }
}
