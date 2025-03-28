import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InicioComponent } from './pages/inicio/inicio.component';
import { UsuarioComponent } from './pages/usuario/usuario.component';
import { ExpertoComponent } from './pages/experto/experto.component';

const routes: Routes = [
  { path: '', component: InicioComponent },
  { path: 'usuario', component: UsuarioComponent },
  { path: 'experto', component: ExpertoComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
