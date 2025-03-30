import { Routes } from "@angular/router";
import { canActivateAuthRole } from "../../core/guard/keycloak-guard.guard";
import { DashboardComponent } from "./dashboard.component";
import { StatsBoardComponent } from "./stats-board/stats-board.component";
import { TransactionBoardComponent } from "./transaction-board/transaction-board.component";




export const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    canActivate: [canActivateAuthRole],
    data: {role: 'User'},
    children: [
      {
        path: 'stats',
        component: StatsBoardComponent,
        canActivate: [canActivateAuthRole],
        data: {role: 'User'},
      },
      {
        path: 'transactions',
        component: TransactionBoardComponent,
        canActivate: [canActivateAuthRole],
        data: {role: 'User'},
      },
    ]
  },
  {
    path: '',
    redirectTo: '',
    pathMatch: 'full'
  }
]
