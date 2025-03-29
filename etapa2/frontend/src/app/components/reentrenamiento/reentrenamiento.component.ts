import { Component } from '@angular/core';
import { FakeNewsService } from '../../fake-news.service';

@Component({
  selector: 'app-reentrenamiento',
  templateUrl: './reentrenamiento.component.html',
  styleUrls: ['./reentrenamiento.component.css']
})
export class ReentrenamientoComponent {
  titulo: string = '';
  descripcion: string = '';
  clasificacion: number = 0; 
  mensaje: string = '';
  cargando: boolean = false; 

  precision: number | null = null;
  recall: number | null = null;
  f1Score: number | null = null;

  constructor(private fakeNewsService: FakeNewsService) {}

  reentrenar(event: Event) {
    event.preventDefault(); 

    if (!this.titulo.trim() || !this.descripcion.trim()) {
      this.mensaje = 'Por favor, ingresa un título y una descripción válida.';
      return;
    }

    this.cargando = true; 

    this.fakeNewsService.reentrenarModelo([this.titulo], [this.descripcion], [this.clasificacion])
      .subscribe(
        (response) => {
          console.log('Reentrenamiento exitoso:', response);
          this.precision = response.metrics.precision;
          this.recall = response.metrics.recall;
          this.f1Score = response.metrics.f1_score;

          this.mensaje = 'Modelo reentrenado correctamente. Métricas actualizadas.';
          this.titulo = '';
          this.descripcion = ''; 
          this.clasificacion = 0;
          this.cargando = false; 
        },
        (error) => {
          console.error('Error en el reentrenamiento:', error);
          this.mensaje = 'Error al reentrenar el modelo. Intenta de nuevo.';
          this.cargando = false; 
        }
      );
  }
}
