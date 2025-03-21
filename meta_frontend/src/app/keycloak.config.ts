import {
  AutoRefreshTokenService,
  createInterceptorCondition,
  IncludeBearerTokenCondition,
  UserActivityService,
  provideKeycloak,
  withAutoRefreshToken,
  INCLUDE_BEARER_TOKEN_INTERCEPTOR_CONFIG
} from "keycloak-angular";
import { KeycloakConfig } from "keycloak-js";

const keycloakConfig: KeycloakConfig = {
  url: 'http://localhost:9090',
  realm: 'meta',
  clientId: 'meta-ui'
}

const localhostCondition = createInterceptorCondition<IncludeBearerTokenCondition>({
  urlPattern: /^(http:\/\/localhost:8000)(\/.*)?$/i
});

export const provideKeycloakAngular = () =>
  provideKeycloak({
    config: keycloakConfig,
    initOptions: {
      onLoad: 'check-sso',
      silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
      redirectUri: window.location.origin + '/',
      pkceMethod: 'S256',
    },
    features: [
      withAutoRefreshToken({
        onInactivityTimeout: 'logout',
        sessionTimeout: 60000,
      })
    ],
    providers: [
      AutoRefreshTokenService,
      UserActivityService,
      {
        provide: INCLUDE_BEARER_TOKEN_INTERCEPTOR_CONFIG,
        useValue: [localhostCondition]
      }
    ]
  })


