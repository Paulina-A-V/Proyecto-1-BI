import { Component } from '@angular/core';
@Component({
  selector: 'app-experto',
  templateUrl: './experto.component.html',
  styleUrl: './experto.component.css'
})
export class ExpertoComponent {
  seccion: 'inicio' | 'clasificaciones' | 'reentrenamiento' = 'inicio';
  irAClasificaciones() {
    this.seccion = 'clasificaciones';
  }
  irAReentrenamiento() {
    this.seccion = 'reentrenamiento';
  }
  volverAInicio() {
    this.seccion = 'inicio';
  }
}