import { TestBed } from '@angular/core/testing';

import { ColumnChartService } from './column-chart.service';

describe('ColumnChartService', () => {
  let service: ColumnChartService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ColumnChartService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
