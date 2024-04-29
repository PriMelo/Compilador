#Compilador
- No arquivo analisador_lexico.py acrescentar o nome do arquivo de extensão .p na variável arquivo_entrada.
- Executar python3 analisador_lexico.py. Será criado dois arquivos um com extensão .pkl que é a entrada do arquivo analisador_sintatico.py e 
outro com a extesão .json com os tokens, lexemas e linhas referente ao analisador léxico.

- No arquivo analisador_sintatico.py acrescentar o nome do arquivo de extensão .pkl na variável arquivo_entrada.
- Executar python3 analisador_sintatico.py. Será criado um arquivos com extensão .json com os tokens correspondentes ou erros sintáticos, caso houver, referentes a análise sintática.
 python3 analisador_lexico.py
 
Exemplo:

 Em analisador_lexico.py :
 arquivo_entrada = 'media.p'
 
 Cria 'media.pkl' e 'media_tokens.json'

 Em analisador_sintatico.py :
 arquivo_entrada = 'media.pkl'
 
 Cria 'media._sintatico.json'
