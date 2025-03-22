import { Component, inject } from '@angular/core';
import { TokenService } from '../../core/services/token.service';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';


@Component({
  selector: 'app-overview',
  imports: [
    CommonModule,
    MatButtonModule
  ],
  templateUrl: './overview.component.html',
  styleUrl: './overview.component.scss'
})
export class OverviewComponent {
  private _tokenService = inject(TokenService)
  private _router = inject(Router)

  constructor() {
    this._tokenService.loadUserInformations()
  }

  openinterest() {
    this._router.navigate(['histories'])
  }
}
