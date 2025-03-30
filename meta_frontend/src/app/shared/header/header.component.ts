import { Component, effect, inject, Renderer2, ViewChild, ViewChildren } from '@angular/core';

import { MatButtonModule } from "@angular/material/button";
import { MatDividerModule } from "@angular/material/divider";
import { MatIconModule } from "@angular/material/icon";
import { MatListModule } from "@angular/material/list";
import { MatDrawer, MatSidenavModule } from "@angular/material/sidenav";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatTooltipModule } from "@angular/material/tooltip";
import { Router, RouterModule, RouterOutlet } from '@angular/router';

import { CommonModule } from '@angular/common';
import Keycloak from "keycloak-js";
import { KEYCLOAK_EVENT_SIGNAL, KeycloakEventType, ReadyArgs, typeEventArgs } from 'keycloak-angular';
import { DrawerMenu } from './drawer.menu.model';
import { SocketService } from '../../features/dashboard/services/socket.service';


@Component({
  selector: 'app-header',
  imports: [
    RouterOutlet,
    RouterModule,

    CommonModule,
    MatButtonModule,
    MatDividerModule,
    MatIconModule,
    MatListModule,
    MatSidenavModule,
    MatToolbarModule,
    MatTooltipModule,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @ViewChild('drawer') drawer!: MatDrawer

  tooltipDelay = 1200

  authenticated = false
  keycloakStatus: string | undefined
  private _keycloak = inject(Keycloak)
  private _keycloakSignal = inject(KEYCLOAK_EVENT_SIGNAL)

  private _socketService = inject(SocketService)

  _router = inject(Router)

  renderer2 = inject(Renderer2)

  themeIcon = 'light_mode'

  drawerMenu: DrawerMenu[] = [
    {
      name: 'Overview',
      info: 'Personal overview of everything',
      uri: 'overview',
    },
    {
      name: 'Coins',
      info: 'Listing current Coins',
      uri: 'coins',
    },
    {
      name: 'Transactions',
      info: 'Listing bought and sold coins',
      uri: 'transactions',
    },
    {
      name: 'Interests',
      info: 'Managing favorite coins',
      uri: 'interests',
    },
    {
      name: 'Histories',
      info: 'Overview of histories of coins',
      uri: 'histories',
    },
    {
      name: 'Dashboard',
      info: 'Overview of coins',
      uri: 'dashboard',
    },
  ]

  constructor() {
    effect(() => {
      const keycloakEvent = this._keycloakSignal()

      this.keycloakStatus = keycloakEvent.type

      switch(keycloakEvent.type) {
        case KeycloakEventType.Ready:
          this.authenticated = typeEventArgs<ReadyArgs>(keycloakEvent.args)
          if (this.authenticated) {
            this._socketService.connect()
            this._router.navigate(['overview'])
          }
          break

        case KeycloakEventType.AuthSuccess:
          this.authenticated = true
          this._router.navigate(['overview'])
          break

        case KeycloakEventType.AuthLogout:
          this._socketService.disconnect()
          this.authenticated = false
          this._router.navigate([''])
          break
      }
    })
  }

  login() {
    this._keycloak.login()
  }

  logout() {
    this._keycloak.logout()
  }


  toggle() {
    if (document.body.className.includes("light")) {
      this.renderer2.removeClass(document.body, 'light')
      this.themeIcon = 'light_mode'
    } else {
      this.renderer2.addClass(document.body, 'light')
      this.themeIcon = 'dark_mode'
    }
  }

  navigateTo(item: DrawerMenu) {
    this._router.navigate([item.uri])
    if (this.drawer.opened) {
      this.drawer.close()
    }
  }
}
