import { TestBed } from '@angular/core/testing';

import { CoinBehaviorService } from './coin-behavior.service';

describe('CoinBehaviorService', () => {
  let service: CoinBehaviorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CoinBehaviorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
