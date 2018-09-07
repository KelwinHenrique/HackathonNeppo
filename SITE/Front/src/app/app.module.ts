import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule} from '@angular/router'
import {ROUTES} from './app.routes'
import {HttpModule } from '@angular/http'

import { AppComponent } from './app.component';
import { CadastroComponent } from './cadastro/cadastro.component';
import { AcessoComponent } from './acesso/acesso.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { TopodashComponent } from './topodash/topodash.component';
import { LateraldashComponent } from './lateraldash/lateraldash.component';
import { ConteudodashComponent } from './conteudodash/conteudodash.component';


@NgModule({
  declarations: [
    AppComponent,
    CadastroComponent,
    AcessoComponent,
    LoginComponent,
    DashboardComponent,
    TopodashComponent,
    LateraldashComponent,
    ConteudodashComponent
  ],
  imports: [
    RouterModule.forRoot(ROUTES),
    BrowserModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
