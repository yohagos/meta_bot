import { Routes } from "@angular/router";
import { canActivateAuthRole } from './../../core/guard/keycloak-guard.guard';
import { InterestsComponent } from "./interests.component";
import { InterestDetailComponent } from "./interest-detail/interest-detail.component";


export const routes: Routes = [
  {
    path: '',
    component: InterestsComponent,
    canActivate: [canActivateAuthRole],
    data: {role: 'User'}
  },
  {
    path: ':id',
    component: InterestDetailComponent,
    canActivate: [canActivateAuthRole],
    data: {role: 'User'}
  },
  {
    path: '',
    redirectTo: '',
    pathMatch: 'full'
  }
]
