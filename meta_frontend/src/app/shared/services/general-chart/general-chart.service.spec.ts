import { TestBed } from '@angular/core/testing';

import { GeneralChartService } from './general-chart.service';

describe('GeneralChartService', () => {
  let service: GeneralChartService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GeneralChartService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
