1. Pré-requisitos

    Python
    Biblioteca openpyxl: Necessária para a importação e exportação de tarefas em formato Excel.

2. Estrutura do Projeto

O projeto contém 5 ficheiros principais:

    tarefa.py – Define a classe Tarefa, encapsulando dados e métodos básicos de uma tarefa.
    database_manager.py – Gere a interação com a base de dados SQLite (criando tabelas, armazenando tarefas e anexos em BLOB).
    gestor.py – Camada de lógica de negócio, delegando a persistência ao DatabaseManager. É responsável por gerar IDs automáticos, escalonar tarefas e outras operações gerais.
    excel_manager.py – Responsável pela importação e exportação de tarefas em ficheiros Excel (.xlsx).
    gui.py – Interface gráfica principal em Tkinter, onde o utilizador pode:
        Adicionar tarefas (e anexos).
        Listar tarefas e pesquisá-las por texto.
        Alterar prioridade e remover tarefas.
        Anexar/consultar ficheiros associados às tarefas.
        Importar/Exportar tarefas via Excel.

3. Passos de Execução

    Colocar todos os ficheiros (tarefa.py, database_manager.py, gestor.py, excel_manager.py, gui.py) no mesmo diretório, por exemplo src/.
    Instalar dependências:
    openpyxl

Executar a Interface Gráfica:

   gui.py

Isto irá criar o ficheiro tarefas.db automaticamente (se não existir) e abrir a janela principal.

4. Interação com a Aplicação

    Menu Principal:
        Listar Tarefas: Abre o frame que apresenta a lista de tarefas, com campo de pesquisa parcial (ID ou nome). Selecionando uma tarefa, o utilizador pode alterar prioridade, remover, adicionar e consultar anexos.
        Adicionar Tarefa: Permite inserir os dados de uma nova tarefa. Se o ID for deixado em branco, o sistema gera automaticamente um ID no formato numero/ano (ex.: 1/2024). É possível anexar ficheiros (docx, xlsx, pdf) durante a criação.
        Escalonar Tarefas: Escalona automaticamente as tarefas com mais de 15 dias para prioridade 1.
        Importar/Exportar Excel: Lê/escreve as tarefas de/para ficheiros Excel (.xlsx).
        Sair: Encerra a aplicação.

    Listar Tarefas:
        A lista atualiza-se automaticamente quando o utilizador entra neste frame.
        Campo de Pesquisa: Insira uma sequência de texto para encontrar tarefas cujo nome ou id contenha esse texto.
        Botão “Atualizar Lista”: Recarrega manualmente a lista sem voltar ao menu.
        Detalhes da Tarefa: Ao clicar numa tarefa na lista, os dados aparecem na mesma janela (à direita).
            Alterar Prioridade: Digite 1, 2 ou 3 e clique no botão “Alterar”.
            Remover Tarefa: Elimina permanentemente a tarefa e seus anexos.
            Adicionar Anexo: Escolha um ficheiro do disco. O conteúdo binário é gravado na BD.
            Consultar Anexo: Cria um ficheiro temporário no diretório atual (tmp_file_<id>.ext) e abre com os.startfile.
                Caso não abra, verifique se o sistema tem permissão de escrita e se o programa para abrir esse tipo de ficheiro está associado.

    Adicionar Tarefa:
        Preencha os campos obrigatórios (Nome, Email, Telefone, Morada, Prioridade, Descrição).
        ID opcional (se vazio, o sistema gera ID).
        Adicionar Anexo: O ficheiro selecionado será armazenado como BLOB na base de dados depois de clicar em “Salvar Tarefa”.

    Importar/Exportar Excel:
        Importar: Escolha um ficheiro .xlsx que siga o cabeçalho esperado (ID, Nome, Email, Telefone, Morada, Prioridade, Descricao, DataCriacao, Escalonada). As tarefas serão inseridas na BD.
        Exportar: Guarda todas as tarefas existentes para um ficheiro .xlsx, permitindo compartilhar ou fazer backup.

5. Observações Importantes

    Permissões de Escrita: O programa grava ficheiros temporários (tmp_file_<id>.<ext>) ao consultar anexos.

6. Resolução de Problemas

    Erro ao Criar Tarefa:
        Verifique se preencheu todos os campos (exceto ID, caso seja para gerar automático).


    Erro ao Importar/Exportar Excel:
        Confirme se openpyxl está instalado.
        Verifique se o ficheiro .xlsx segue o formato esperado e se não está em uso por outro programa.

7. Notas finais:
    Não foi possível, à data da entrega, contruir uma versão onde fosse possível consultar os anexos depois de anexados à atividade.