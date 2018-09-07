import { Component, OnInit } from '@angular/core';
import { Cliente } from '../model/Cliente'
import { Http } from '@angular/http'
import {ActivatedRoute } from '@angular/router'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  public cliente: Cliente
  
  

  constructor(private http: Http, private route: ActivatedRoute) { 
    
  }

  ngOnInit() {
    var id = this.route.snapshot.params['id']
    this.getCliente(id).then((cliente: Cliente) => {
      this.cliente = cliente
    })
      .catch((param: any) => {
        console.log("erro idiotaa2222")
      })
  }
  public getCliente(id: string): Promise<Cliente> {
    return this.http.get('http://192.168.1.4:5000/cliente/'+id).toPromise().then((resposta: any) => resposta.json())
  }

}
