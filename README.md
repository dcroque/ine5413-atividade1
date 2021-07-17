# INE5413 - Atividade1

## Introdução

Este projeto foi desenvolvido como parte da disciplina de Grafos do Curso de Ciências da Computação na Universidade Federal de Santa Catarina do semestre 2021/1.

Essa pequena aplicação permite a leitura de um grafo e em seguida fazer algumas operações com ele, como busca em largura a partir de um vértice específico ou checagem da existência de um Ciclo Eulerano, por exemplo. Não espere ver as melhores práticas de programação e não se surpreenda com algum erro inesperado mas tentamos resolver as principais possíveis causas de falha de execução, manter o código organizado e com seus métodos documentados documentados.

## Requisitos

- Python 3 (Versão utilizada 3.9.6, mas versões menos atualizadas possivelmente devem funcionar)

## Modo de uso

Após baixar ou clonar o repositório, dentro da pasta **src**, você pode executar o seguinte comando para testar se tudo está funcionando corretamente:

> python3 main.py -file test_data.txt -i -s 1

O projeto inclui um pequeno modelo de arquivo de entrada, após a execução você deve ter impresso na tela uma lista com vértices e arestas do vértices e resultados de uma busca em largura a partir do elemento de índice 1.

O formato do arquivo de entrada deve possuir  uma lista de vertices com índice e rótulo em cada linha separada e uma lista de arestas, possuindo o vertice de origim, destino e o peso da transição, como no seguinte modelo:

```
#Linhas começando com # serão desconsideradas durante a leitura 
*vertices n
1 rotulo1
2 rotulo2
...
n rotulon
*edges
1 2 1
1 3 2
2 3 3
```

O projeto possui algumas flags de execução, que você pode conferir com a flag **-h**, mas vale mencionar que a flag **-file CAMINHO** é obrigatória para a execução da aplicação e caso a aplicação falhe em ler ou achar o arquivo no caminho indicado a execução é encerrada. Você pode usar a flag **-i** para conferir se o seu arquivo foi lido corretamente durante a execução.