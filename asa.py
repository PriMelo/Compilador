class AstNode:
    
    def __init__(self):
        self.node_type = None
        self.children = []
        self.node_type = None
        self.data_type = None
        self.op = None

class Bloco_node(AstNode):
    def __init__(self,nome):
        super().__init__()
        self.children = None
        self.node_type = 'BLOCO'
        self.nome = nome
        
class Function_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'FUNCTION'
        self.data_type = None
        self.op = None
        self.bloco = None
        self.nome = lexema
        
        
class RelOp_node(AstNode):
    def __init__(self,filho_esq, filho_dir,op):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'RELOP'
        self.data_type = None
        self.op = op
        self.esq = filho_esq
        self.dir = filho_dir
        
   

class ArithOp_node(AstNode):
    def __init__(self,filho_esq, filho_dir,op):
        super().__init__()
        self.node_type = 'ARITHOP'
        self.data_type = None
        self.op = op
        self.esq = filho_esq
        self.dir = filho_dir
            
class Assign_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'ASSIGN'
        self.data_type = None
        self.op = '='
        self.esq = None
        self.dir = None
        
        
class If_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'IF'
        self.data_type = None
        self.op = None
        self.condicao = None
        self.parte_verdadeira = None
        self.parte_falsa = None

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
        
class Print_node(AstNode):
    def __init__(self, argumento, quebra_linha:False):
        super().__init__()
        self.children.append(argumento)
        self.node_type = 'PRINT'
        self.data_type = None
        self.op = None
        self.argumento = argumento
        self.quebra_linha = quebra_linha
        
class Return_node(AstNode):
    def __init__(self, expressao):
        super().__init__()
        self.children.append(expressao)
        self.node_type = 'RETURN'
        self.data_type = None
        self.op = None
        self.expressao = expressao
        

        
class Call_node(AstNode):
    def __init__(self,lex):
        super().__init__()
        self.node_type = 'CALL'
        self.argumentos = None
        self.nome_funcao = lex  

        
class Id_node(AstNode):
    def __init__(self, lexema):
        super().__init__()
        self.node_type = 'ID'
        self.nome = lexema
        

class Int_const_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'INT_CONST'
        self.data_type = 'int'
       
class Float_const_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'FLOAT_CONST'
        self.data_type = 'float'
        
class Char_const_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'CHAR_CONST'
        self.data_type = 'char'