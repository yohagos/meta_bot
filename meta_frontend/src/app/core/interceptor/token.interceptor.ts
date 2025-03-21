import { HttpHeaders, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import Keycloak from 'keycloak-js';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  const keycloak = inject(Keycloak)

  if (keycloak.token) {
    const authReq = req.clone({
      headers: new HttpHeaders({
        Authorization: `Bearer ${keycloak.token}`
      })
    })
    return next(authReq)
  }
  return next(req);
};


