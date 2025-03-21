import { Component, Inject, inject, Injectable, Input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MAT_SNACK_BAR_DATA, MatSnackBar, MatSnackBarAction, MatSnackBarActions, MatSnackBarLabel, MatSnackBarModule, MatSnackBarRef } from "@angular/material/snack-bar";

interface SnackBarType {
  message?: string
  snackBarType?: string
  icon?: string
}

@Injectable({
  providedIn: 'root'
})
export class SnackbarService {
  private _snackbar = inject(MatSnackBar)

  durationInSeconds = 4000

  openSnackBar(message: string, status: 'success' | 'error' = 'success') {
    let snack: SnackBarType = {
      message,
      icon: status === 'error' ? 'error' : 'check',
      snackBarType: status
    }

    this._snackbar.openFromComponent(SnackBarTemplateComponent, {
      duration: this.durationInSeconds,
      data: snack
    })
  }
}

@Component({
  selector: 'snackbar-notification',
  template: `
      <span class="{{snackbar.snackBarType}}  {{borderClass}}" matSnackBarLabel>
        {{snackbar.message}}
      </span>
      <span class="{{snackbar.snackBarType}}" matSnackBarActions>
        <button mat-button matSnackBarAction (click)="snackBarRef.dismissWithAction()">
          <mat-icon class="{{snackbar.snackBarType}}"> {{snackbar.icon}} </mat-icon>
        </button>
      </span>
  `,
  styles: `
  :host {
    display: flex;
  }

  @keyframes fadeOutBorder {
    0% {
      border-width: 4px;
      opacity: 1;
    }
    50% {
      border-width: 4.5px;
      opacity: 0.7;
      transform: scale(1.05);
    }
    100% {
      border-width: 0px;
      opacity: 0.3;
    }
  }
    .mat-mdc-snack-bar-label {
      border-left: 4px solid  ;
      border-bottom: 4px solid  ;
      border-top: 4px solid ;

      &.border-success::before {
        border-color: limegreen;
      }
      &.border-error::before {
        border-color: red;
      }

      animation: fadeOutBorder 7s ease-out forwards;
    }

    .mat-mdc-snack-bar-actions {
      border-right: 4px solid  ;
      border-bottom: 4px solid  ;
      border-top: 4px solid  ;

      &.border-success::before {
        border-color: limegreen;
      }
      &.border-error::before {
        border-color: red;
      }

      animation: fadeOutBorder 7s ease-out forwards;
    }

  .error {
    color: red;
  }

  .success {
    color: limegreen;
  }
  `,
  imports: [
    MatButtonModule,
    MatIconModule,
    MatSnackBarAction,
    MatSnackBarActions,
    MatSnackBarLabel
  ]
})
export class SnackBarTemplateComponent {
  snackBarRef = inject(MatSnackBarRef<SnackBarTemplateComponent>)
  snackbar: SnackBarType = {}

  constructor(
    @Inject(MAT_SNACK_BAR_DATA) data: SnackBarType
  ) {
    this.snackbar = data
  }

  get borderClass() {
    return `border-${this.snackbar.snackBarType || 'success' } `
  }

}
