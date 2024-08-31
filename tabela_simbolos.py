class TabelaDeSimbolos:
    
    def __init__(self, nome_tab):
        self.nome = nome_tab
        self.tipo_retorno = None
        self.elementos = {}

           
        
    def novo_elemento(self,chave, lexema, tipo, pos_param, eh_chamada=False, num_args=0, args=[]):
        
        if lexema not in self.elementos:
        
            self.elementos[chave] ={
                'nome': lexema,
                'tipo_de_dado': tipo,
                'pos_param':pos_param,
                'eh_chamada': eh_chamada,
                'num_args': num_args,
                'args':args,
                'chave': chave
            }
            
        # elif -> se tiver duas chamadas de função iguais?
        
        else:
            print('Erro semântico: redeclaração de identificador')
    
    def get_elemento(self,lexema):
        
        if self.elementos[lexema]:
            
            return self.elementos[lexema]
        
        else:
            print('Erro: elemento não existe na tabela')
            
    def print_tab(self):
        print(f"Tabela {self.nome}")
        for e in self.elementos.values():
            print(f"chave:{e['chave']} nome: {e['nome']} tipo_de_dado: {e['tipo_de_dado']} pos_param: {e['pos_param']} eh_chamada: {e['eh_chamada']} num_args: {e['num_args']} args: {e['args']}")
        
        
        