import { Routes } from '@angular/router';
import { HomeComponent } from './core/home/home.component';
import { OverviewComponent } from './features/overview/overview.component';
import { canActivateAuthRole } from './core/guard/keycloak-guard.guard';
import { NoPageComponent } from './shared/error-page/no-page/no-page.component';
import { ForbiddenComponent } from './shared/forbidden/forbidden.component';
import { HistoriesComponent } from './features/histories/histories.component';
import { CoinsComponent } from './features/coins/coins.component';
import { TransactionsComponent } from './features/transactions/transactions.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';


export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'overview',
    component: OverviewComponent,
    canActivate: [ canActivateAuthRole ],
    data: { role: 'User' }
  },
  {
    path: 'histories',
    component: HistoriesComponent,
    canActivate: [ canActivateAuthRole ],
    data: { role: 'User' }
  },
  {
    path: 'interests',
    loadChildren: () => import('./features/interests/interest.routes').then(mod => mod.routes),
    canActivate: [ canActivateAuthRole ],
    data: { role: 'User' }
  },
  {
    path: 'coins',
    component: CoinsComponent,
    canActivate: [ canActivateAuthRole ],
    data: { role: 'User' }
  },
  {
    path: 'transactions',
    component: TransactionsComponent,
    canActivate: [ canActivateAuthRole ],
    data: { role: 'User' }
  },
  {
    path: 'dashboard',
    loadChildren: () => import('./features/dashboard/dashboard.routes').then(mod => mod.routes),
    canActivate: [ canActivateAuthRole ],
    data: { role: 'User' }
  },
  {
    path: 'forbidden',
    component: ForbiddenComponent
  },
  {
    path: '**',
    component: NoPageComponent
  },

];
