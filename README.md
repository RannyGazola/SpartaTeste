# SpartaTeste

# Instruções para usar o programa:
Este programa está dividido em duas partes principais: app.py e atualizar.py.\
O app.py é responsável pela interface gráfica, onde você pode pesquisar dados em um banco de dados SQLite.\
O atualizar.py é responsável por carregar dados do arquivo CSV para o banco de dados.

# Requisitos:
Python 3 instalado.

# Passos:
1 - Execute app.py para abrir a interface gráfica.\
2 - Clique no botão "Atualizar" na interface. Este botão acionará o script que irá carregar os dados dos arquivos CSV presentes na pasta data para o banco de dados SQLite. Só é necessário fazê-lo na primeira vez que utilizar\
2 - Digite a pesquisa e clique em pesquisar.

# Atualizando banco de dados:
Se quiser atualizar a base de dados, o arquivo cad_cia_aberta.csv deve ser colocado na pasta data do diretório para que o banco de dados seja atualizado, após isso, é só clicar no botão "Atualizar" novamente (ou acionar o script).\
Os arquivos CSV não precisam de formatação após serem baixados do Portal de Dados Abertos. Certifique-se de que os dados estejam disponíveis na pasta data antes de executar o script de atualização.\

# Cometários
Utilizei SQLite para a leitura e manipulação dos dados pela sua facilidade de integração. Os critérios foram os mesmos para a escolha do Tkinter.\
A princípio, eu escolhi MySQL e Flask por já ter mais familiaridade, mas no decorrer do projeto mudei a perspectiva.\
Usei como referência de pesquisa a coluna DT_INI_SIT.\
\
\
\
Sugestão de pesquisa para as datas que mais possuem resultados:\
30/06/2022\
20/07/1977\
04/01/2010\
09/08/2005\
22/03/2005
