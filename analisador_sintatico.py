from first_follow import first, follow
import sys
from asa import *

        


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
        
        
        
    
class AnalisadorSintatico:
        
    token_resposta = []
    token_saida = []

    i =0
    token_atual = None
    tabelas = {}
    
    tipo_de_dado = None
    tabela_atual = None
    posicao_param = 0
    
    vec_ast = []
    
    tipo_de_dado = {
            'VOID': -1,
            'CHAR': 0,
            'INT': 1,
            'FLOAT': 2       
        }
    
    def r_cria_tabela(cls, lexema):
        
        
        if lexema not in cls.tabelas:
            
            nova_tabela = TabelaDeSimbolos(lexema)
            cls.tabelas[lexema] = nova_tabela
            cls.tabela_atual = nova_tabela
            
        else:
            print('Erro: Função redeclarada')
    
   
    
    def nova_tabela(cls,nome_tab):
        cls.tabelas[nome_tab] = None
    
    def analisar(cls, saida_an_lexico):
        cls.token_resposta = saida_an_lexico.copy()
        cls.token_atual = cls.token_resposta[cls.i][0]
        cls.programa()
        
        saida = {'saida':[]}   

        for r in cls.token_saida:    
            
                saida['saida'].append(
                    {
                        'token': r
                    }
                )
                
        for k in cls.tabelas:
            print(cls.tabelas[k].print_tab())
        
        return saida
                
        

    def erro(cls,*args):       
        
        token_esperado = args[1]
        cls.token_saida.append(f'Erro sintatico - encontrado: {cls.token_resposta[cls.i][1]} esperado: {token_esperado} na linha: {cls.token_resposta[cls.i][2]}')
       # print('Erro sintático - esperado:', token_esperado, 'na linha:', cls.token_resposta[cls.i][2])
        if cls.i < len(cls.token_resposta)-1:
                       
            if args[0] and  not cls.token_atual in follow[args[0].__name__]:
              
                cls.i += 1
            
            cls.token_atual = cls.token_resposta[cls.i][0]
        
        if args[0] != None:
            args[0]()

    def match(cls,token_esperado):
                
        cls.token_saida.append(cls.token_atual)
            
        if token_esperado == cls.token_atual:
            if cls.i < len(cls.token_resposta)-1:
                cls.i += 1
                cls.token_atual = cls.token_resposta[cls.i][0]
            
        else:
            cls.erro(None,token_esperado)

    def type_(cls):
            
        if cls.token_atual == 'INT':
            cls.match('INT')
            return cls.tipo_de_dado[cls.token_resposta[cls.i-1][0]] 

        elif cls.token_atual == 'FLOAT':
            cls.match('FLOAT')
            return cls.tipo_de_dado[cls.token_resposta[cls.i-1][0]] 

        elif cls.token_atual == 'CHAR':
            cls.match('CHAR')
            return cls.tipo_de_dado[cls.token_resposta[cls.i-1][0]]
            
        else:
            cls.erro(cls.type_, 'INT | FLOAT | CHAR')
            return None
            
    def tipoRetornoFuncao(cls):
        
        if cls.token_atual == 'ARROW':
            cls.match('ARROW')
            tipo_retorno = cls.type_
            return tipo_retorno

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.tipoRetornoFuncao, 'ARROW')   

        else:
            return
        
    def atribuicaoOuChamada(cls, id_node):
        
        if cls.token_atual == 'ASSINGN':            
            cls.match('ASSINGN')
            rel_node = cls.expr()
            assign_node = Assign_node(id_node, rel_node)             
            cls.match('SEMICOLON')
            return assign_node

        elif cls.token_atual == 'LPAREN':
            cls.match('LPAREN')
            cls.listArgs()
            cls.match('RPAREN')

        else:
            cls.erro(cls.atribuicaoOuChamada, 'ASSIGN | LPAREN')

    def listArgs2(cls,argumentos, argumentos_nodes):

        if cls.token_atual == 'COMMA':
            cls.match('COMMA')
            arg, fator_node = cls.fator()
            argumentos.append(arg) 
            argumentos_nodes.append(fator_node) 
            cls.listArgs2(argumentos,argumentos_nodes)
        

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.listArgs2, 'COMMA')  

        else:
            return

    def listArgs(cls):

        argumentos = []
        argumentos_nodes = []
        
        if cls.token_atual in ['ID', 'INT_CONST', 'FLOAT_CONST', 'CHAR_LITERAL', 'LPAREN']:
            f,node_fator = cls.fator()
            argumentos.append(f)
            argumentos_nodes.append(node_fator)
    
            cls.listArgs2(argumentos, argumentos_nodes)
            return argumentos, argumentos_nodes
            
        
        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.listArgs, 'ID | INT_CONST | FLOAT_CONST | CHAR_LITERAL | LPAREN' )  
        
        else:
            return
        
            
    def chamadaFuncao(cls, call_node:Call_node):
        
        if cls.token_atual == 'LPAREN':
            cls.match('LPAREN')
            args, args_nodes = cls.listArgs()
            call_node.argumentos = args_nodes[:]
            cls.match('RPAREN')
            return args

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.chamadaFuncao, 'LPAREN')  

        else:
            return -1
            
    def fator(cls):

        if cls.token_atual == 'ID':
            cls.match('ID')
            lexema = cls.token_resposta[cls.i-1][1]
            call_node = Call_node()
            call_node.nome_funcao = lexema
            argumentos = cls.chamadaFuncao(call_node)
            if not argumentos == -1:
                tipo_tab_chamada = cls.tabelas[lexema].tipo_retorno
                cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=tipo_tab_chamada, pos_param=-1, eh_chamada=True,num_args=len(argumentos),args=argumentos)
            
            return lexema, call_node
        
        elif cls.token_atual == 'INT_CONST':
            cls.match('INT_CONST')
            lexema = cls.token_resposta[cls.i-1][1]
            node = Int_const_node(lexema)
            return cls.token_resposta[cls.i-1][1],node

        elif cls.token_atual == 'FLOAT_CONST':
            cls.match('FLOAT_CONST')
            lexema = cls.token_resposta[cls.i-1][1]
            node = Float_const_node(lexema)
            return cls.token_resposta[cls.i-1][1],node
            
        elif cls.token_atual == 'CHAR_LITERAL':
            cls.match('CHAR_LITERAL')
            lexema = cls.token_resposta[cls.i-1][1]
            node = Char_const_node(lexema)
            return cls.token_resposta[cls.i-1][1],node
            
        elif cls.token_atual == 'LPAREN':
            cls.match('LPAREN')
            cls.expr()
            cls.match('RPAREN')
            return cls.token_resposta[cls.i-2][1],None

        else:
            cls.erro(cls.fator, 'LPAREN | ID | INT_CONST | FLOAT_CONST | CHAR_LITERAL')
            return None,None
            
    def opMult(cls):    
        
        if cls.token_atual == 'MULT':
            cls.match('MULT')
            return cls.token_resposta[cls.i-1][1]
        
        elif cls.token_atual == 'DIV':
            cls.match('DIV')
            return cls.token_resposta[cls.i-1][1]

        else:
            cls.erro(cls.opMult, 'MULT | DIV')    
            
    def termoOpc(cls, no_fator_esq):

        if cls.token_atual in ['MULT', 'DIV']:
            op = cls.opMult()
            no_fator_dir = cls.fator()
            arith_node = ArithOp_node(no_fator_esq,no_fator_dir,op)
            arith_node = cls.termoOpc(arith_node)
            return arith_node        

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.termoOpc, 'MULT | DIV')   

        else:
            return arith_node
        
    def termo(cls):
        
        _, no_fator = cls.fator()
        arith_node = cls.termoOpc(no_fator) 
        return arith_node   
        
    def opAdicao(cls):
        
        if cls.token_atual == 'PLUS':
            cls.match('PLUS')
            return cls.token_resposta[cls.i-1][1]
        
        elif cls.token_atual == 'MINUS':
            cls.match('MINUS')
            return cls.token_resposta[cls.i-1][1]
        
        else:
            cls.erro(cls.opAdicao, 'PLUS | MINUS')

    def adicaoOpc(cls, no_adicao_esq):
        
        if cls.token_atual in ['PLUS', 'MINUS']:
            op = cls.opAdicao()
            no_adicao_dir = cls.termo()
            arith_node2 = ArithOp_node(no_adicao_esq, no_adicao_dir, op)
            arith_node2 = cls.adicaoOpc(arith_node2)
            return arith_node2

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.adicaoOpc, 'PLUS | MINUS')  

        else:
            return

    def adicao(cls):
        
        arith_node = cls.termo()
        arith_node = cls.adicaoOpc(arith_node) 
        return arith_node


    def opRel(cls):
        if cls.token_atual == 'LT':
            cls.match('LT')
            return cls.token_resposta[cls.i -1][1]
        
        elif cls.token_atual == 'LTE':
            cls.match('LTE')
            return cls.token_resposta[cls.i -1][1]
        
        elif cls.token_atual == 'GT':
            cls.match('GT')
            return cls.token_resposta[cls.i -1][1]
        
        elif cls.token_atual == 'GTE':
            cls.match('GTE')
            return cls.token_resposta[cls.i -1][1]
        
        else:
            cls.erro(cls.opRel, 'LT | GT | LTE | GTE')

    def relOpc(cls, no_rel_esq):
        
        if cls.token_atual in ['LT', 'GT', 'LTE', 'GTE']:
            op = cls.opRel()
            no_rel_dir = cls.adicao()
            rel_node = RelOp_node(no_rel_esq, no_rel_dir, op)
            rel_node = cls.relOpc(rel_node)
            return rel_node

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.relOpc, 'LT | GT | LTE | GTE')  

        else:
            return
            
    def rel(cls):
        
        arith_node = cls.adicao()
        arith_node = cls.relOpc(arith_node)
        return arith_node 

    def opIgual(cls):
        
        if cls.token_atual == 'EQUAL':
            cls.match('EQUAL')
            return cls.token_resposta[cls.i - 1][1]
        
        elif cls.token_atual == 'NOTEQUAL':
            cls.match('NOTEQUAL')
            return cls.token_resposta[cls.i - 1][1]
        
        else:
            cls.erro(cls.opIgual, 'EQUAL | NOTEQUAL')   

    def exprOpc(cls, no_esq):
        
        if cls.token_atual in ['EQUAL', 'NOTEQUAL']:
            op = cls.opIgual()
            no_dir = cls.rel()
            rel_node = RelOp_node(no_esq, no_dir, op)
            rel_node = cls.exprOpc(rel_node)
            return rel_node

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.exprOpc, 'EQUAL | NOTEQUAL')  

        else:
            return
            
    def expr(cls):
        
        rel_node = cls.rel()
        rel_node = cls.exprOpc(rel_node)
        return rel_node
    
    def comandoSenao(cls):
        
        if cls.token_atual == 'ELSE':
            cls.match('ELSE')
            if_node = cls.comandoIf()
            return if_node

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.comandoSenao, 'ELSE')  

        else:
            return
    
    def comandoIf(cls):
        
        if cls.token_atual == 'IF':
            cls.match('IF')
            expr_node = cls.expr()
            bloco_node = cls.bloco()
            if_node = If_node(expr_node, bloco_node)
            else_node = cls.comandoSenao()
            if else_node:
                if_node.parte_falsa = else_node
            return if_node
            
        elif cls.token_atual == 'LBRACE':
            cls.bloco()
        
        else:
            cls.erro(cls.comandoIf, 'IF | LBRACE')
        
        
    def comando(cls):

        if cls.token_atual == 'ID':
            id_node = Id_node(lexema = cls.token_resposta[cls.i][1])
            cls.match('ID')
            assign_node = cls.atribuicaoOuChamada(id_node)            
            return assign_node
            
        
        elif cls.token_atual == 'IF':
            
            if_node = cls.comandoIf()
            return if_node
        
        elif cls.token_atual == 'WHILE':
            cls.match('WHILE')
            expr_node = cls.expr()
            bloco_node = cls.bloco()
            while_node = While_node(expr_node, bloco_node) 
            return while_node
        
        elif cls.token_atual == 'PRINT':
            
            cls.match('PRINT')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('LPAREN')
            cls.match("FORMATTER_STRING")
            cls.match('COMMA')
            args, args_node = cls.listArgs()
            print_node = Print_node(args_node[0])
            if args == None:
                args = []
            argumentos = ["sys_call(print)"] + args
            cls.match('RPAREN')
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=-1, pos_param=-1, eh_chamada=True,num_args=len(argumentos),args=argumentos)
            cls.match('SEMICOLON')
            return print_node
        
        elif cls.token_atual == 'PRINTLN':
            cls.match('PRINTLN')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('LPAREN')
            cls.match("FORMATTER_STRING")
            cls.match('COMMA')
            args, args_node = cls.listArgs()
            print_node = Print_node(args_node[0], True)
            argumentos = ["sys_call(print)"] + args
            cls.match('RPAREN')
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=-1, pos_param=-1, eh_chamada=True,num_args=len(argumentos),args=argumentos)
            cls.match('SEMICOLON') 
            return print_node
        
        elif cls.token_atual == 'RETURN':
            cls.match('RETURN')
            expr_node = cls.expr()
            return_node = Return_node(expr_node)
            cls.match('SEMICOLON')
            return return_node
        
        else:
            cls.erro(cls.comando, 'RETURN')
            
        
            
    def varList2(cls,variaveis):

        if cls.token_atual == 'COMMA':
            cls.match('COMMA')
            cls.match('ID')
            variaveis.append(cls.token_resposta[cls.i-1][1])
            cls.varList2(variaveis)

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.varList2, 'COMMA')      

        elif cls.token_atual in follow[sys._getframe().f_code.co_name]:
            return
        else:
            cls.erro(getattr(cls, sys._getframe().f_code.co_name), 'COMMA | ' + ' | '.join(follow[sys._getframe().f_code.co_name]))
        

    def varList(cls):
        
        variaveis = []
        cls.match('ID')
        variaveis.append(cls.token_resposta[cls.i-1][1])
        cls.varList2(variaveis)  
        return variaveis
        
    def declaracao(cls):

        cls.match('LET')
        variaveis = cls.varList()
        cls.match('COLON')
        tipo = cls.type_()
        for v in variaveis:
            
            cls.tabela_atual.novo_elemento(chave=v, lexema=v,tipo=tipo, pos_param=-1)
        
        cls.match('SEMICOLON')
            
    def sequencia(cls,no_bloco, list_sequencia):
        if cls.token_atual == 'LET':
            cls.declaracao()
            cls.sequencia(no_bloco, list_sequencia)
        
        elif cls.token_atual in ['ID','IF', 'WHILE', 'PRINT', 'PRINTLN', 'RETURN']:
            no_comando = cls.comando()            
            no_comando = cls.sequencia(no_comando, list_sequencia)
            list_sequencia.append(no_comando)
        
        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.sequencia, 'LET | ID | IF | WHILE | PRINT | PRINTLN | RETURN ')    
        
        else:
            return    
         ## lista de sequencia   
    def bloco(cls):
        cls.match('LBRACE')  
        list_sequencia = []      
        cls.sequencia(no_bloco, list_sequencia)
        no_bloco = Bloco_node(list_sequencia)
        cls.match('RBRACE')
        return no_bloco       
        
            
    def listaParams2(cls):


        if cls.token_atual == 'COMMA':
            cls.match('COMMA')
            cls.posicao_param += 1
            cls.match('ID')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('COLON')
            tipo = cls.type_() 
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=tipo, pos_param=cls.posicao_param)
            cls.listaParams2()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.listaParams2, 'COMMA')  

        else:
            return

    def listaParams(cls):
        cls.posicao_param = 0

        if cls.token_atual == 'ID':
            cls.match('ID')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('COLON')
            tipo = cls.type_()
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=tipo, pos_param=cls.posicao_param)
            cls.listaParams2()
        
        elif cls.token_atual in follow[sys._getframe().f_code.co_name]:
            return
        else:
            cls.erro(getattr(cls, sys._getframe().f_code.co_name), 'ID | ' + ' | '.join(follow[sys._getframe().f_code.co_name]) )

        
        
    def funcaoSeq(cls):
        
        if cls.token_atual == 'FUNCTION':        
            cls.funcao()
            cls.funcaoSeq()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.funcaoSeq, 'FUNCTION')      
            
        else:
            return    
            
    def funcao(cls):
        cls.match('FUNCTION')        
        
        if cls.token_atual == 'MAIN':
            cls.r_cria_tabela(cls.token_resposta[cls.i][1])
            cls.match('MAIN')
        
        elif cls.token_atual == 'ID':
            cls.r_cria_tabela(cls.token_resposta[cls.i][1])
            cls.match('ID')
        
        elif cls.token_atual == 'simbolo invalido':
            cls.erro(None, 'ID | MAIN')  
        
        else:
            cls.erro(None, 'ID| MAIN')

        no_function = Function_node(cls.token_resposta[cls.i-1][1])
        
        cls.match('LPAREN')
        cls.listaParams()
        cls.match('RPAREN')
        tipo_retorno = cls.tipoRetornoFuncao()
        cls.tabela_atual.tipo_retorno = tipo_retorno
        no_bloco = cls.bloco()
        no_function.children.append(no_bloco)
        no_function.bloco = no_bloco
        cls.vec_ast.append(no_function)
            
    def programa(cls):
        
        if cls.token_atual == 'FUNCTION':
            cls.funcao()
            cls.funcaoSeq()
        
        else:
            cls.erro(cls.programa, 'FUNCTION')
            
    def representacao_ASA():
            
        

    

    