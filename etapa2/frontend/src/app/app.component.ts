import { Component } from '@angular/core';
import { FakeNewsService } from './fake-news.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  inputText = '';
  resultado: any = null;
  cargando = false;

  constructor(private fakeNewsService: FakeNewsService) {}

  predecir() {
    if (!this.inputText.trim()) {
      alert('Por favor ingresa una noticia.');
      return;
    }

    this.cargando = true;

    this.fakeNewsService.predict(this.inputText).subscribe({
      next: (res) => {
        this.resultado = res;
        this.cargando = false;
      },
      error: (err) => {
        alert('Error al conectar con el modelo.');
        this.cargando = false;
      }
    });
  }
}
