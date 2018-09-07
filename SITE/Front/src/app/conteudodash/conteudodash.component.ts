import { Component, OnInit, Input } from '@angular/core';
import { Http } from '@angular/http'
import { Pergunta } from '../model/Pergunta'
import { Cliente } from '../model/Cliente';


@Component({
  selector: 'app-conteudodash',
  templateUrl: './conteudodash.component.html',
  styleUrls: ['./conteudodash.component.css']
})
export class ConteudodashComponent implements OnInit {

  public pergunta: Pergunta = undefined
  public perguntas: Pergunta[] =  new Array()
  public pos: any = 0
  @Input() cliente: Cliente

  public status: any = 0 //0==video 1==leitura 2 ==pergunta 3== certo 4 ==errado
  constructor(private http: Http) { }
  ngOnInit() {
    
    
    this.getTodasPerguntas().then((pergunstas: Pergunta[]) => {
      this.perguntas = pergunstas
      this.pergunta = this.perguntas[0]
    })
      .catch((param: any) => {
        console.log("erro idiotaa")
      })
  }
  public getTodasPerguntas(): Promise<Pergunta[]> {
    return this.http.get('http://192.168.1.4:5000/perguntas').toPromise().then((resposta: any) => resposta.json())
  }

  public submeter (res: any){
    console.log(this.pergunta.alternativaCorreta)
    console.log(res)
    if(res== this.pergunta.alternativaCorreta){
        this.pos = this.pos + 1
        if(this.pos < this.perguntas.length){
          this.pergunta = this.perguntas[this.pos]
          this.status = 3
        }else{
          this.status = 5
        }

    }else{
      this.status = 4
      
    }
  }

  public irVideo(){
    this.status = 1
  }
  public irQuiz(){
    this.status = 2
  }
  public irPergunta(){
    this.status = 2
  }
}
