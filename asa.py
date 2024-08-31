from tabela_simbolos import TabelaDeSimbolos

raiz = None



class AstNode:
    
    def __init__(self):
        self.node_type = None
        self.children = []
        self.node_type = None
        self.data_type = None
        self.op = None 
        self.nome = ''

    def dicionario(self):
        filho_dict = []
        for filho in self.children: 
            filho_dict.append(filho.dicionario())
        dicionario = {'node_type':self.node_type, 'children': filho_dict}
        return dicionario   
    
    def verifica_tipos(self):
       for filho in self.children:
           filho.verifica_tipos(); 

class Bloco_node(AstNode):
    def __init__(self,filhos):
        super().__init__()
        self.children = filhos.copy()
        self.node_type = 'BLOCO'
        self.nome = 'BLOCO'    

class Function_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'FUNCTION'
        self.data_type = None
        self.op = None
        self.bloco = None
        self.nome = lexema
        
    def verifica_tipos(self):
        
        raiz = self.nome

        for filho in self.children:
            filho.verifica_tipos(); 

        
class RelOp_node(AstNode):
    def __init__(self,filho_esq:AstNode, filho_dir,op):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'RELOP'
        self.data_type = filho_esq.data_type
        self.op = op
        self.esq = filho_esq
        self.dir = filho_dir        
   
    def dicionario(self):
        filho_dict = []
        for filho in self.children:
            filho_dict.append(filho.dicionario())
        dicionario = {'node_type':self.node_type, 'children': filho_dict, 'op':self.op }
        return dicionario
    
    def verifica_tipos(self):
        
        tipo_esq = self.children[0].verifica_tipos()
        tipo_dir = self.children[1].verifica_tipos()
        if tipo_dir != tipo_esq:
            
            print(f'Erro Semântico-> Tipos incopatíveis na expressão aritmética: tipo({tipo_esq}) {self.op} tipo({tipo_dir})')
            return None
            
        return self.data_type

class ArithOp_node(AstNode):
    def __init__(self,filho_esq:AstNode, filho_dir,op):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'ARITHOP'
        self.data_type = filho_dir.data_type
        self.op = op
        self.esq = filho_esq
        self.dir = filho_dir
        
    
    def dicionario(self):
        filho_dict = []
        for filho in self.children:
            filho_dict.append(filho.dicionario())
        dicionario = {'node_type':self.node_type, 'children': filho_dict, 'op':self.op }
        return dicionario      
    
    def verifica_tipos(self):
        
        tipo_esq = self.children[0].verifica_tipos()
        tipo_dir = self.children[1].verifica_tipos()
        if tipo_dir != tipo_esq:
            
            print(f'Erro Semântico-> Tipos incopatíveis na expressão aritmética: tipo({tipo_esq}) {self.op} tipo({tipo_dir})')
            return None
            
        return self.data_type
        
            
            
class Assign_node(AstNode):
    def __init__(self, filho_esq:AstNode, filho_dir:AstNode):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'ASSIGN'
        self.data_type = filho_esq.data_type
        self.op = '='
        self.esq = filho_esq
        self.dir = filho_dir
        

    def verifica_tipos(self):
        
        tipo_esq = self.children[0].verifica_tipos()
        tipo_dir = self.children[1].verifica_tipos()
        if tipo_dir != tipo_esq:
            
            print(f'Erro Semântico-> Tipos incopatíveis na expressão aritmética: tipo({tipo_esq}) {self.op} tipo({tipo_dir})')
        
        
class If_node(AstNode):
    def __init__(self, filho_condicao, filho_v, filho_f=None):
        super().__init__()
        self.children.append(filho_condicao)
        self.children.append(filho_v)
        if filho_f:
            self.children.append(filho_f)
        self.node_type = 'IF'
        self.data_type = None
        self.op = None
        self.condicao = filho_condicao
        self.parte_verdadeira = filho_v
        self.parte_falsa = filho_f
        
    def verifica_tipos(self):
        
        self.children[0].verifica_tipos()
        self.children[1].verifica_tipos()
        if len(self.children) > 2:
            self.children[2].verifica_tipos()
        
        

class While_node(AstNode):
    def __init__(self,  condicao, comando):
        super().__init__()
        self.children.append(condicao)
        self.children.append(comando)
        self.node_type = 'WHILE'
        self.data_type = None
        self.op = None
        self.condicao = condicao
        self.comando = comando
    
    def verifica_tipos(self):
        
        self.children[0].verifica_tipos()
        self.children[1].verifica_tipos()
        
class Print_node(AstNode):
    def __init__(self, argumento, quebra_linha=False):
        super().__init__()
        self.children.append(argumento)
        self.node_type = 'PRINT'
        self.data_type = None
        self.op = None
        self.argumento = argumento
        self.quebra_linha = quebra_linha
    
    def verifica_tipos(self):
        
        self.children[0].verifica_tipos()
        
class Return_node(AstNode):
    def __init__(self, expressao):
        super().__init__()
        self.children.append(expressao)
        self.node_type = 'RETURN'
        self.data_type = None
        self.op = None
        self.expressao = expressao  

    def verifica_tipos(self):
        
        self.children[0].verifica_tipos()     

        
class Call_node(AstNode):
    def __init__(self,lex):
        super().__init__()
        self.node_type = 'CALL'
        self.nome = lex  
    
    def verifica_tipos(self):
        
        return self.data_type

        
class Id_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'ID'
        self.nome = lexema

    def dicionario(self):
        dicionario = {'node_type':self.node_type, 'nome':self.nome }
        return dicionario       
    
    def verifica_tipos(self):
        
        return self.data_type

class Int_const_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'INT_CONST'
        self.nome = lexema
        self.data_type = 1
    
    def dicionario(self):
        dicionario = {'node_type':self.node_type, 'nome':self.nome }
        return dicionario  
    
    def verifica_tipos(self):
        
        return self.data_type
        
       
class Float_const_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'FLOAT_CONST'
        self.nome = lexema
        self.data_type = 2

    def dicionario(self):
        dicionario = {'node_type':self.node_type, 'nome':self.nome }
        return dicionario     
    
    def verifica_tipos(self):
        
        return self.data_type 
        
class Char_const_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'CHAR_CONST'
        self.nome = lexema
        self.data_type = 0
        
    def dicionario(self):
        dicionario = {'node_type':self.node_type, 'nome':self.nome }
        return dicionario  
    
    def verifica_tipos(self):
        
        return self.data_type
        
        