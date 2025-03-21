import { inject, Injectable, OnInit } from '@angular/core';
import Keycloak, { KeycloakProfile } from "keycloak-js";


@Injectable({
  providedIn: 'root'
})
export class TokenService {
  private _keycloak = inject(Keycloak)

  userInfo: any

  constructor() {}

  loadUserInformations() {
    this._keycloak.loadUserInfo().then((data: KeycloakProfile) => this.userInfo = data)
  }

  getUserProfile() {
    return this.userInfo
  }
}
