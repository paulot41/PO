"""
Interface gráfica principal em Tkinter, com melhorias:
- Lista Tarefas com pesquisa parcial, mostra detalhes no mesmo frame
- Permite consultar e anexar ficheiros (corrigindo erro de ficheiro temporário)
- Adicionar Tarefa e Import/Export Excel funcionais
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from gestor import GestorDeTarefas
from excel_manager import ExcelManager
from datetime import datetime
import os
from tarefa import Tarefa

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Tarefas")
        self.geometry("900x600")

        # Instâncias do Gestor e ExcelManager
        self.gestor = GestorDeTarefas()
        self.excel_manager = ExcelManager()

        # Configura layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Cria dicionário de frames
        self.frames = {}

        # Cria todos os frames
        self.create_frames()
        # Abre menu principal inicialmente
        self.show_frame("MenuPrincipal")

    def create_frames(self):
        """
        Cria e configura cada frame da aplicação.
        """
        frame_menu = tk.Frame(self)
        self.frames["MenuPrincipal"] = frame_menu
        self.create_menu(frame_menu)

        frame_listar = tk.Frame(self)
        self.frames["ListarTarefas"] = frame_listar
        self.create_listar_tarefas(frame_listar)

        frame_adicionar = tk.Frame(self)
        self.frames["AdicionarTarefa"] = frame_adicionar
        self.create_adicionar_tarefa(frame_adicionar)

        frame_escalonar = tk.Frame(self)
        self.frames["EscalonarTarefas"] = frame_escalonar
        self.create_escalonar_tarefas(frame_escalonar)

        frame_excel = tk.Frame(self)
        self.frames["ExcelManager"] = frame_excel
        self.create_excel_manager(frame_excel)

        # Coloca todos os frames no grid
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, frame_name):
        """
        Exibe o frame solicitado. Se for 'ListarTarefas', atualiza a lista automaticamente.
        """
        frame = self.frames[frame_name]
        frame.tkraise()
        if frame_name == "ListarTarefas":
            # Atualiza a lista ao entrar no frame
            self.atualizar_lista_tarefas("")

    def create_menu(self, frame):
        """
        Menu Principal (simplificado) sem opções redundantes.
        """
        tk.Label(frame, text="Menu Principal", font=("Helvetica", 16)).pack(pady=20)

        # Botão para Listar Tarefas
        btn_list = tk.Button(frame, text="Listar Tarefas", width=25,
                             command=lambda: self.show_frame("ListarTarefas"))
        btn_list.pack(pady=10)

        # Botão para Adicionar Tarefa
        btn_add = tk.Button(frame, text="Adicionar Tarefa", width=25,
                            command=lambda: self.show_frame("AdicionarTarefa"))
        btn_add.pack(pady=10)

        # Botão para Escalonar Tarefas
        btn_escalonar = tk.Button(frame, text="Escalonar Tarefas", width=25,
                                  command=lambda: self.show_frame("EscalonarTarefas"))
        btn_escalonar.pack(pady=10)

        # Botão para Import/Export Excel
        btn_excel = tk.Button(frame, text="Importar/Exportar Excel", width=25,
                              command=lambda: self.show_frame("ExcelManager"))
        btn_excel.pack(pady=10)

        # Botão para sair da aplicação
        btn_exit = tk.Button(frame, text="Sair", width=25, command=self.quit)
        btn_exit.pack(pady=10)

    def create_listar_tarefas(self, frame):
        """
        Frame para Listar Tarefas com pesquisa parcial,
        e exibir detalhes (alterar prioridade, remover, anexar) no mesmo frame.
        """
        tk.Label(frame, text="Listar Tarefas", font=("Helvetica", 14)).pack(pady=5)

        # Secção de pesquisa
        search_frame = tk.Frame(frame)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Pesquisar:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        def pesquisar():
            texto = self.search_entry.get().strip()
            self.atualizar_lista_tarefas(texto)

        btn_search = tk.Button(search_frame, text="Procurar", command=pesquisar)
        btn_search.pack(side=tk.LEFT, padx=5)

        # Botão Voltar
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        # Dividimos em list_frame (tarefas) e detail_frame (detalhes)
        painel = tk.Frame(frame)
        painel.pack(fill=tk.BOTH, expand=True)

        self.list_frame = tk.Frame(painel)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_v = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_tarefas = tk.Listbox(self.list_frame, yscrollcommand=scrollbar_v.set, width=50)
        self.listbox_tarefas.pack(fill=tk.BOTH, expand=True)
        scrollbar_v.config(command=self.listbox_tarefas.yview)

        def selecionar_tarefa(event):
            selection = self.listbox_tarefas.curselection()
            if not selection:
                return
            index = selection[0]
            conteudo = self.listbox_tarefas.get(index)
            id_tarefa = conteudo.split("|")[0].strip()
            self.mostrar_detalhes_tarefa(id_tarefa)

        self.listbox_tarefas.bind("<<ListboxSelect>>", selecionar_tarefa)

        # Botão para atualizar manualmente a lista se o utilizador quiser
        btn_atualizar = tk.Button(self.list_frame, text="Atualizar Lista",
                                  command=lambda: self.atualizar_lista_tarefas(""))
        btn_atualizar.pack(pady=5)

        self.detail_frame = tk.Frame(painel)
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def atualizar_lista_tarefas(self, texto_pesquisa=""):
        """
        Atualiza a listbox com base na pesquisa parcial ou na listagem padrão.
        """
        self.listbox_tarefas.delete(0, tk.END)
        if texto_pesquisa:
            tarefas = self.gestor.pesquisar_tarefas(texto_pesquisa)
        else:
            tarefas = self.gestor.listar_tarefas(ordenacao='prioridade')

        for tarefa in tarefas:
            data_str = tarefa.data_criacao.strftime("%Y-%m-%d")
            status = "[Escalonada]" if tarefa.escalonada else ""
            self.listbox_tarefas.insert(
                tk.END,
                f"{tarefa.id} | {tarefa.nome} | {data_str} | P:{tarefa.prioridade} {status}"
            )

    def mostrar_detalhes_tarefa(self, id_tarefa):
        """
        Exibe detalhes no detail_frame, onde pode alterar prioridade, remover e anexar ficheiros.
        """
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        tarefa = self.gestor.procurar_tarefa(id_tarefa)
        if not tarefa:
            tk.Label(self.detail_frame, text="Tarefa não encontrada.").pack()
            return

        tk.Label(self.detail_frame, text=f"Detalhes da Tarefa {tarefa.id}", font=("Helvetica", 14)).pack(pady=5)

        info_frame = tk.Frame(self.detail_frame)
        info_frame.pack(pady=10)

        campos = [
            ("ID:", tarefa.id),
            ("Nome:", tarefa.nome),
            ("Email:", tarefa.email),
            ("Telefone:", tarefa.telefone),
            ("Morada:", tarefa.morada),
            ("Data Criação:", tarefa.data_criacao.strftime("%Y-%m-%d %H:%M:%S")),
            ("Escalonada:", "Sim" if tarefa.escalonada else "Não"),
            ("Descrição:", tarefa.descricao),
        ]

        row = 0
        for label_text, valor in campos:
            tk.Label(info_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
            tk.Label(info_frame, text=valor).grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
            row += 1

        # Secção para alterar prioridade
        tk.Label(info_frame, text="Prioridade (1,2,3):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        var_prioridade = tk.StringVar(value=str(tarefa.prioridade))
        entry_prio = tk.Entry(info_frame, textvariable=var_prioridade, width=5)
        entry_prio.grid(row=row, column=1, sticky=tk.W, padx=5)

        def atualizar_prioridade():
            try:
                nova_p = int(var_prioridade.get())
                if nova_p not in [1,2,3]:
                    raise ValueError
                tarefa.prioridade = nova_p
                self.gestor.atualizar_tarefa(tarefa)
                messagebox.showinfo("Sucesso", "Prioridade atualizada.")
                # Atualiza a lista
                self.atualizar_lista_tarefas("")
            except ValueError:
                messagebox.showerror("Erro", "Prioridade inválida (1,2,3).")

        btn_prio = tk.Button(info_frame, text="Alterar", command=atualizar_prioridade)
        btn_prio.grid(row=row, column=2, padx=5, pady=3)
        row += 1

        # Botão remover tarefa
        def remover_tarefa():
            confirm = messagebox.askyesno("Confirmar", "Deseja remover esta tarefa?")
            if confirm:
                sucesso = self.gestor.remover_tarefa(tarefa.id)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Tarefa removida.")
                    self.atualizar_lista_tarefas("")
                    for w in self.detail_frame.winfo_children():
                        w.destroy()
                else:
                    messagebox.showerror("Erro", "Não foi possível remover a tarefa.")

        btn_remover = tk.Button(info_frame, text="Remover Tarefa", fg="red", command=remover_tarefa)
        btn_remover.grid(row=row, column=1, pady=5)

        # Anexos
        anexos_frame = tk.LabelFrame(self.detail_frame, text="Anexos", padx=5, pady=5)
        anexos_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        anexos_listbox = tk.Listbox(anexos_frame, height=8)
        anexos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anexos_scroll = tk.Scrollbar(anexos_frame, orient=tk.VERTICAL, command=anexos_listbox.yview)
        anexos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        anexos_listbox.config(yscrollcommand=anexos_scroll.set)

        for anexo_dict in tarefa.anexos:
            file_name = os.path.basename(anexo_dict['caminho'])
            anexos_listbox.insert(tk.END, f"{anexo_dict['id']} - {file_name}")

        def adicionar_novo_anexo():
            caminho = filedialog.askopenfilename(
                title="Selecionar Ficheiro",
                filetypes=(("Ficheiros", "*.docx *.xlsx *.pdf"), ("All Files", "*.*"))
            )
            if caminho:
                self.gestor.adicionar_anexo(tarefa.id, caminho)
                anexos_listbox.insert(tk.END, f"Novo - {os.path.basename(caminho)}")
                tarefa.anexos = self.gestor.listar_anexos(tarefa.id)

        def consultar_anexo():
            selection = anexos_listbox.curselection()
            if not selection:
                return
            index = selection[0]
            conteudo = anexos_listbox.get(index)
            anexo_id = conteudo.split(" - ")[0].replace("Novo","").strip()
            for adic in tarefa.anexos:
                if str(adic['id']) == anexo_id:
                    data_bin = adic['data']
                    if not data_bin:
                        messagebox.showerror("Erro", "Ficheiro binário não encontrado na BD.")
                        return
                    extension = os.path.splitext(adic['caminho'])[1]
                    tmp_path = f"./tmp_file_{anexo_id}{extension}"
                    try:
                        with open(tmp_path, "wb") as f:
                            f.write(data_bin)
                        if os.path.exists(tmp_path):
                            os.startfile(tmp_path)  # Em Windows
                        else:
                            messagebox.showerror("Erro", "Não foi possível criar o ficheiro temporário.")
                    except Exception as e:
                        messagebox.showerror("Erro", f"Falha ao abrir anexo: {e}")
                    break

        btn_frame = tk.Frame(anexos_frame)
        btn_frame.pack()
        btn_add_anexo = tk.Button(btn_frame, text="Adicionar Anexo", command=adicionar_novo_anexo)
        btn_add_anexo.pack(side=tk.LEFT, padx=5)
        btn_consultar_anexo = tk.Button(btn_frame, text="Consultar Anexo", command=consultar_anexo)
        btn_consultar_anexo.pack(side=tk.LEFT, padx=5)

    def create_adicionar_tarefa(self, frame):
        """
        Frame para adicionar nova tarefa, incluindo anexos (restaurado).
        """
        tk.Label(frame, text="Adicionar Tarefa", font=("Helvetica", 14)).pack(pady=5)
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        inner_frame = tk.Frame(frame)
        inner_frame.pack(pady=10)

        tk.Label(inner_frame, text="(ID automático se vazio)").grid(row=0, column=1, sticky=tk.W)
        tk.Label(inner_frame, text="ID da Tarefa:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_id = tk.Entry(inner_frame)
        entry_id.grid(row=1, column=1, pady=5)

        tk.Label(inner_frame, text="Nome:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_nome = tk.Entry(inner_frame)
        entry_nome.grid(row=2, column=1, pady=5)

        tk.Label(inner_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_email = tk.Entry(inner_frame)
        entry_email.grid(row=3, column=1, pady=5)

        tk.Label(inner_frame, text="Telefone:").grid(row=4, column=0, sticky=tk.W, pady=5)
        entry_telefone = tk.Entry(inner_frame)
        entry_telefone.grid(row=4, column=1, pady=5)

        tk.Label(inner_frame, text="Morada:").grid(row=5, column=0, sticky=tk.W, pady=5)
        entry_morada = tk.Entry(inner_frame)
        entry_morada.grid(row=5, column=1, pady=5)

        tk.Label(inner_frame, text="Prioridade:").grid(row=6, column=0, sticky=tk.W, pady=5)
        listbox_prioridade = tk.Listbox(inner_frame, height=3, exportselection=False)
        listbox_prioridade.grid(row=6, column=1, pady=5)
        prioridades = ["1-Alta", "2-Média", "3-Baixa"]
        for p in prioridades:
            listbox_prioridade.insert(tk.END, p)
        listbox_prioridade.config(selectmode=tk.SINGLE)

        tk.Label(inner_frame, text="Descrição:").grid(row=7, column=0, sticky=tk.W, pady=5)
        text_descricao = tk.Text(inner_frame, height=5, width=30)
        text_descricao.grid(row=7, column=1, pady=5)

        # Frame para lista de anexos
        anexos_frame = tk.Frame(frame)
        anexos_frame.pack(pady=5)
        tk.Label(anexos_frame, text="Anexos a Adicionar:").pack(anchor=tk.W)
        anexos_listbox = tk.Listbox(anexos_frame, height=4, width=50)
        anexos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anexos_scroll = tk.Scrollbar(anexos_frame, orient=tk.VERTICAL, command=anexos_listbox.yview)
        anexos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        anexos_listbox.config(yscrollcommand=anexos_scroll.set)

        def adicionar_anexo():
            caminho = filedialog.askopenfilename(
                title="Selecionar Ficheiro",
                filetypes=(("Ficheiros", "*.docx *.xlsx *.pdf"), ("All Files", "*.*"))
            )
            if caminho:
                anexos_listbox.insert(tk.END, caminho)

        btn_adicionar_anexo = tk.Button(frame, text="Adicionar Anexo", command=adicionar_anexo)
        btn_adicionar_anexo.pack(pady=5)

        def salvar_tarefa():
            id_tarefa = entry_id.get().strip()
            nome = entry_nome.get().strip()
            email = entry_email.get().strip()
            telefone = entry_telefone.get().strip()
            morada = entry_morada.get().strip()
            descricao = text_descricao.get("1.0", tk.END).strip()

            selecionados = listbox_prioridade.curselection()
            if selecionados:
                indice = selecionados[0]
                prioridade_str = prioridades[indice]
                prioridade = int(prioridade_str.split("-")[0]) if "-" in prioridade_str else int(prioridade_str[0])
            else:
                messagebox.showerror("Erro", "Escolha uma prioridade.")
                return

            if not nome or not email or not telefone or not morada or not descricao:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
                return

            tarefa = Tarefa(
                id=id_tarefa,
                nome=nome,
                email=email,
                telefone=telefone,
                morada=morada,
                prioridade=prioridade,
                descricao=descricao,
                data_criacao=datetime.now(),
                escalonada=False
            )
            try:
                self.gestor.adicionar_tarefa(tarefa)
                # Gravar anexos na base
                for i in range(anexos_listbox.size()):
                    caminho_ficheiro = anexos_listbox.get(i)
                    self.gestor.adicionar_anexo(tarefa.id, caminho_ficheiro)
                messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso.")
                # Limpa campos
                entry_id.delete(0, tk.END)
                entry_nome.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_telefone.delete(0, tk.END)
                entry_morada.delete(0, tk.END)
                text_descricao.delete("1.0", tk.END)
                listbox_prioridade.selection_clear(0, tk.END)
                anexos_listbox.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao adicionar tarefa: {e}")

        btn_salvar = tk.Button(frame, text="Salvar Tarefa", command=salvar_tarefa)
        btn_salvar.pack(pady=10)

    def create_escalonar_tarefas(self, frame):
        """
        Frame para escalonar tarefas (mais de 15 dias sem escalonamento).
        """
        tk.Label(frame, text="Escalonar Tarefas", font=("Helvetica", 14)).pack(pady=5)
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        tk.Label(frame, text="Escalona tarefas com mais de 15 dias no sistema.").pack(pady=5)

        def escalonar():
            sucesso = self.gestor.escalonar_tarefas()
            if sucesso:
                messagebox.showinfo("Sucesso", "Tarefas escalonadas.")
            else:
                messagebox.showinfo("Informação", "Nenhuma tarefa foi escalonada.")
        btn_escalonar = tk.Button(frame, text="Escalonar Agora", command=escalonar)
        btn_escalonar.pack(pady=10)

    def create_excel_manager(self, frame):
        """
        Frame para Importar/Exportar Tarefas no formato Excel.
        """
        tk.Label(frame, text="Importar/Exportar Tarefas (Excel)", font=("Helvetica", 14)).pack(pady=5)
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        def importar():
            ficheiro = filedialog.askopenfilename(
                title="Selecionar Ficheiro Excel",
                filetypes=(("Excel Files", "*.xlsx"),)
            )
            if ficheiro:
                try:
                    tarefas = self.excel_manager.importar_tarefas(ficheiro)
                    for t in tarefas:
                        self.gestor.adicionar_tarefa(t)
                    messagebox.showinfo("Sucesso", "Tarefas importadas com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao importar: {e}")

        def exportar():
            ficheiro = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=(("Excel Files", "*.xlsx"),)
            )
            if ficheiro:
                try:
                    tarefas = self.gestor.listar_tarefas()
                    self.excel_manager.exportar_tarefas(ficheiro, tarefas)
                    messagebox.showinfo("Sucesso", "Tarefas exportadas com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar tarefas: {e}")

        btn_import = tk.Button(frame, text="Importar Excel", command=importar)
        btn_import.pack(pady=10)

        btn_export = tk.Button(frame, text="Exportar Excel", command=exportar)
        btn_export.pack(pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
