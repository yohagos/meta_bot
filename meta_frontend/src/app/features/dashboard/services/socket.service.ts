import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { Stats } from '../../../services/models';


@Injectable({
  providedIn: 'root'
})
export class SocketService {
  wsSubject$: WebSocketSubject<Stats[]> = webSocket('ws://localhost:8000/api/v1/sockets/coins')

  disconnect() {
    if (this.wsSubject$) {
      this.wsSubject$.complete()
    }
  }
}
