import { Component } from '@angular/core';

@Component({
  selector: 'app-usuario',
  templateUrl: './usuario.component.html',
  styleUrls: ['./usuario.component.css']
})
export class UsuarioComponent {
  seccion: 'inicio' | 'clasificaciones' | 'prediccion' = 'inicio';

  irAClasificaciones() {
    this.seccion = 'clasificaciones';
  }

  irAPrediccion() {
    this.seccion = 'prediccion';
  }

  volverAInicio() {
    this.seccion = 'inicio';
  }
}
