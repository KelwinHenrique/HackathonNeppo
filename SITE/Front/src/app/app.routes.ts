import {Routes } from '@angular/router'

import {AcessoComponent} from './acesso/acesso.component'
import {CadastroComponent} from './cadastro/cadastro.component'
import {LoginComponent} from './login/login.component'
import {DashboardComponent} from './dashboard/dashboard.component'

export const ROUTES: Routes = [
    { path: '', component: AcessoComponent},
    { path: 'cadastrar', component: CadastroComponent},
    { path: 'dashboard/:id', component: DashboardComponent}

]





