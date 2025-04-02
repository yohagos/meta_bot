import { ApplicationConfig, importProvidersFrom, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { CommonModule, DATE_PIPE_DEFAULT_OPTIONS, DatePipe } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { includeBearerTokenInterceptor } from "keycloak-angular";
import { provideKeycloakAngular } from './keycloak.config';
import { tokenInterceptor } from './core/interceptor/token.interceptor';
import { NgxEchartsModule } from 'ngx-echarts';

import * as echarts from 'echarts';
import {
  LineChart,
  LineSeriesOption,
  BarChart,
  BarSeriesOption,
  LinesChart,
  LinesSeriesOption,
} from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from "echarts/components";
import {
  CanvasRenderer
} from "echarts/renderers";
import { provideNativeDateAdapter } from '@angular/material/core';





const providers = [
  FormsModule,
  ReactiveFormsModule,
  CommonModule,
  BrowserModule,
  BrowserAnimationsModule,
  NgxEchartsModule.forRoot({
    echarts: () => Promise.resolve(echarts)
  }),
]

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideKeycloakAngular(),
    provideHttpClient(withInterceptors([includeBearerTokenInterceptor, tokenInterceptor])),
    {
      provide: DATE_PIPE_DEFAULT_OPTIONS,
      useValue: { timezone: 'UTC' }
    },
    importProvidersFrom(providers),
  ]
};
