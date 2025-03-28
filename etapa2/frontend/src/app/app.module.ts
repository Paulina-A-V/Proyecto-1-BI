import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';  // ⬅️ IMPORTANTE

import { AppComponent } from './app.component';
import { InicioComponent } from './pages/inicio/inicio.component';
import { UsuarioComponent } from './pages/usuario/usuario.component';
import { ExpertoComponent } from './pages/experto/experto.component';
import { ClasificacionesComponent } from './components/clasificaciones/clasificaciones.component';
import { PrediccionComponent } from './components/prediccion/prediccion.component';
import { ReentrenamientoComponent } from './components/reentrenamiento/reentrenamiento.component';

@NgModule({
  declarations: [
    AppComponent,
    InicioComponent,
    UsuarioComponent,
    ExpertoComponent,
    ClasificacionesComponent,
    PrediccionComponent,
    ReentrenamientoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule, 
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
