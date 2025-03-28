import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReentrenamientoComponent } from './reentrenamiento.component';

describe('ReentrenamientoComponent', () => {
  let component: ReentrenamientoComponent;
  let fixture: ComponentFixture<ReentrenamientoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ReentrenamientoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReentrenamientoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
