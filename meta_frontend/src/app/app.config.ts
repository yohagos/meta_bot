import { ApplicationConfig, importProvidersFrom, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { includeBearerTokenInterceptor } from "keycloak-angular";
import { provideKeycloakAngular } from './keycloak.config';
import { tokenInterceptor } from './core/interceptor/token.interceptor';



const providers = [
  FormsModule,
  ReactiveFormsModule,
  CommonModule,
  BrowserModule,
  BrowserAnimationsModule,
]

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideKeycloakAngular(),
    provideHttpClient(withInterceptors([includeBearerTokenInterceptor, tokenInterceptor])),
    importProvidersFrom(providers),
  ]
};
