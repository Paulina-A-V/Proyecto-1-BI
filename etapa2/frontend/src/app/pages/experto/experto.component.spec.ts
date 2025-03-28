import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpertoComponent } from './experto.component';

describe('ExpertoComponent', () => {
  let component: ExpertoComponent;
  let fixture: ComponentFixture<ExpertoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ExpertoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExpertoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
