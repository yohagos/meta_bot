import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransactionBoardComponent } from './transaction-board.component';

describe('TransactionBoardComponent', () => {
  let component: TransactionBoardComponent;
  let fixture: ComponentFixture<TransactionBoardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TransactionBoardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TransactionBoardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
