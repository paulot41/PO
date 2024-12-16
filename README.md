# PO
Projeto Programação por Objetos

Este projeto é um Sistema de Gestão de Tarefas, desenvolvido em Python, que inclui:
Persistência de Dados em SQLite (armazenamento anexos em BLOB).
Interface Gráfica com Tkinter, onde o utilizador pode adicionar, listar e pesquisar tarefas, consultar e anexar ficheiros, alterar prioridades e remover tarefas.
Estrutura Orientada a Objetos, separando a lógica de negócio (gestor.py), a gestão de dados (database_manager.py) e a interface (gui.py).
Importação/Exportação de tarefas em formato Excel (via excel_manager.py).
O sistema gere automaticamente os IDs das tarefas (ex.: “1/2024”), permite anexar ficheiros (docx, xlsx ou pdf), e oferece funcionalidades de pesquisa parcial, escalonamento de tarefas com mais de 15 dias e outras operações gerais de manutenção (CRUD). 
Foi desenvolvido de forma a evoluir, onde se poderá introduzir herança (por ex.: diferentes tipos de tarefas) e uma GUI mais avançada, para além da ciração de utilixadores com diferentes niveis de permissões.
