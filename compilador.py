from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico

an_lexico = AnalisadorLexico()
an_sintatico = AnalisadorSintatico()
arquivo = 'calculadora.p'
saida_an_lexico = an_lexico.analisar(arquivo)
saida_an_sintatico = an_sintatico.analisar(saida_an_lexico) 
an_sintatico.representacao_ASA()

