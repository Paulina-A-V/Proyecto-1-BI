import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-prediccion',
  templateUrl: './prediccion.component.html',
  styleUrls: ['./prediccion.component.css']
})
export class PrediccionComponent {
  textoNoticia = '';
  resultado: string | null = null;
  probabilidad: number | null = null;
  cargando = false;

  constructor(private http: HttpClient) {}

  predecir() {
    if (!this.textoNoticia.trim()) {
      alert('Por favor ingrese una noticia.');
      return;
    }

    this.cargando = true;

    const payload = {
      Descripcion: [this.textoNoticia]
    };

    this.http.post<any>('http://localhost:8000/predict', payload).subscribe({
      next: (res) => {
        const pred = res.predictions[0];
        const prob = res.probabilities[0][pred];
        this.resultado = pred === 1 ? 'VERDADERO' : 'FALSO';
        this.probabilidad = prob;
        this.cargando = false;
      },
      error: () => {
        alert('Error al conectar con el servidor.');
        this.cargando = false;
      }
    });
  }
}
