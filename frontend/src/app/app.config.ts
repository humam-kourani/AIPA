import { ApplicationConfig } from '@angular/core';
import {importProvidersFrom} from '@angular/core';
import { provideRouter } from '@angular/router';
import {provideAnimations} from '@angular/platform-browser/animations';
import {provideHttpClient, withFetch} from '@angular/common/http';
import { routes } from './app.routes';
import {MatNativeDateModule} from '@angular/material/core';
import {provideHttpClientTesting} from "@angular/common/http/testing";
import {provideClientHydration} from "@angular/platform-browser";
import {NbThemeModule} from "@nebular/theme";

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideAnimations(),
    provideHttpClient(withFetch()),
    provideHttpClientTesting(),
    provideClientHydration(),
    importProvidersFrom(MatNativeDateModule),
    importProvidersFrom(
      NbThemeModule.forRoot({ name: 'corporate' }),
    )
  ]
};
