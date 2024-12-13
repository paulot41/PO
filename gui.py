import tkinter as tk
from tkinter import messagebox, filedialog
from gestor import GestorDeTarefas
from excel_manager import ExcelManager
from datetime import datetime

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Tarefas")
        self.geometry("600x500")
        self.gestor = GestorDeTarefas()
        self.excel_manager = ExcelManager()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.create_frames()
        self.show_frame("MenuPrincipal")

    def create_frames(self):
        frame_menu = tk.Frame(self)
        self.frames["MenuPrincipal"] = frame_menu
        self.create_menu(frame_menu)

        frame_adicionar = tk.Frame(self)
        self.frames["AdicionarTarefa"] = frame_adicionar
        self.create_adicionar_tarefa(frame_adicionar)

        frame_listar = tk.Frame(self)
        self.frames["ListarTarefas"] = frame_listar
        self.create_listar_tarefas(frame_listar)

        frame_atualizar = tk.Frame(self)
        self.frames["AtualizarPrioridade"] = frame_atualizar
        self.create_atualizar_prioridade(frame_atualizar)

        frame_remover = tk.Frame(self)
        self.frames["RemoverTarefa"] = frame_remover
        self.create_remover_tarefa(frame_remover)

        frame_escalonar = tk.Frame(self)
        self.frames["EscalonarTarefas"] = frame_escalonar
        self.create_escalonar_tarefas(frame_escalonar)

        frame_excel = tk.Frame(self)
        self.frames["ExcelManager"] = frame_excel
        self.create_excel_manager(frame_excel)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def create_menu(self, frame):
        tk.Label(frame, text="Menu Principal", font=("Helvetica", 16)).pack(pady=20)

        btn_add = tk.Button(frame, text="Adicionar Tarefa", width=25, command=lambda: self.show_frame("AdicionarTarefa"))
        btn_add.pack(pady=10)

        btn_list = tk.Button(frame, text="Listar Tarefas", width=25, command=lambda: self.show_frame("ListarTarefas"))
        btn_list.pack(pady=10)

        btn_update = tk.Button(frame, text="Atualizar Prioridade", width=25, command=lambda: self.show_frame("AtualizarPrioridade"))
        btn_update.pack(pady=10)

        btn_remove = tk.Button(frame, text="Remover Tarefa", width=25, command=lambda: self.show_frame("RemoverTarefa"))
        btn_remove.pack(pady=10)

        btn_escalonar = tk.Button(frame, text="Escalonar Tarefas", width=25, command=lambda: self.show_frame("EscalonarTarefas"))
        btn_escalonar.pack(pady=10)

        btn_excel = tk.Button(frame, text="Importar/Exportar Excel", width=25, command=lambda: self.show_frame("ExcelManager"))
        btn_excel.pack(pady=10)

        btn_exit = tk.Button(frame, text="Sair", width=25, command=self.quit)
        btn_exit.pack(pady=10)

    def create_adicionar_tarefa(self, frame):
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        inner_frame = tk.Frame(frame)
        inner_frame.pack(pady=10)

        tk.Label(inner_frame, text="ID da Tarefa:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_id = tk.Entry(inner_frame)
        entry_id.grid(row=0, column=1, pady=5)

        tk.Label(inner_frame, text="Nome:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_nome = tk.Entry(inner_frame)
        entry_nome.grid(row=1, column=1, pady=5)

        tk.Label(inner_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_email = tk.Entry(inner_frame)
        entry_email.grid(row=2, column=1, pady=5)

        tk.Label(inner_frame, text="Telefone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_telefone = tk.Entry(inner_frame)
        entry_telefone.grid(row=3, column=1, pady=5)

        tk.Label(inner_frame, text="Morada:").grid(row=4, column=0, sticky=tk.W, pady=5)
        entry_morada = tk.Entry(inner_frame)
        entry_morada.grid(row=4, column=1, pady=5)

        tk.Label(inner_frame, text="Prioridade:").grid(row=5, column=0, sticky=tk.W, pady=5)
        listbox_prioridade = tk.Listbox(inner_frame, height=3, exportselection=False)
        listbox_prioridade.grid(row=5, column=1, pady=5)
        prioridades = ["1-Alta", "2-Média", "3-Baixa"]
        for prioridade in prioridades:
            listbox_prioridade.insert(tk.END, prioridade)
        listbox_prioridade.config(selectmode=tk.SINGLE)

        tk.Label(inner_frame, text="Descrição:").grid(row=6, column=0, sticky=tk.W, pady=5)
        text_descricao = tk.Text(inner_frame, height=5, width=30)
        text_descricao.grid(row=6, column=1, pady=5)

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
                prioridade = int(prioridade_str.split("-")[0])
            else:
                messagebox.showerror("Erro", "Por favor, selecione uma prioridade.")
                return

            if not id_tarefa or not nome or not email or not telefone or not morada or not descricao:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
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
                messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso.")
                # Limpar os campos
                entry_id.delete(0, tk.END)
                entry_nome.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                entry_telefone.delete(0, tk.END)
                entry_morada.delete(0, tk.END)
                text_descricao.delete("1.0", tk.END)
                listbox_prioridade.selection_clear(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao adicionar tarefa: {e}")

        btn_salvar = tk.Button(frame, text="Salvar Tarefa", command=salvar_tarefa)
        btn_salvar.pack(pady=10)

    def create_listar_tarefas(self, frame):
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        criterio = tk.StringVar(value="prioridade")
        tk.Radiobutton(frame, text="Prioridade", variable=criterio, value="prioridade").pack(anchor=tk.W)
        tk.Radiobutton(frame, text="Tempo no Sistema", variable=criterio, value="tempo").pack(anchor=tk.W)

        list_frame = tk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar_v = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar_v.set)
        listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar_v.config(command=listbox.yview)

        def atualizar_lista():
            listbox.delete(0, tk.END)
            ordem = criterio.get()
            tarefas = self.gestor.listar_tarefas(ordenacao=ordem)
            for tarefa in tarefas:
                status = "[Escalonada]" if tarefa.escalonada else ""
                listbox.insert(tk.END, f"{tarefa.id} - {tarefa.nome} {status}")

        btn_atualizar = tk.Button(frame, text="Atualizar Lista", command=atualizar_lista)
        btn_atualizar.pack(pady=5)

        atualizar_lista()

    def create_atualizar_prioridade(self, frame):
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        inner_frame = tk.Frame(frame)
        inner_frame.pack(pady=10)

        tk.Label(inner_frame, text="ID da Tarefa:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_id = tk.Entry(inner_frame)
        entry_id.grid(row=0, column=1, pady=5)

        tk.Label(inner_frame, text="Nova Prioridade (1-Alta, 2-Média, 3-Baixa):").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_prioridade = tk.Entry(inner_frame)
        entry_prioridade.grid(row=1, column=1, pady=5)

        def atualizar():
            id_tarefa = entry_id.get().strip()
            prioridade_str = entry_prioridade.get().strip()

            if not id_tarefa or not prioridade_str:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return

            try:
                nova_prioridade = int(prioridade_str)
                if nova_prioridade not in [1, 2, 3]:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Prioridade deve ser 1, 2 ou 3.")
                return

            tarefa = self.gestor.procurar_tarefa(id_tarefa)
            if tarefa:
                tarefa.prioridade = nova_prioridade
                self.gestor.atualizar_tarefa(tarefa)
                messagebox.showinfo("Sucesso", "Prioridade atualizada com sucesso.")
                entry_id.delete(0, tk.END)
                entry_prioridade.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Tarefa não encontrada.")

        btn_atualizar = tk.Button(frame, text="Atualizar", command=atualizar)
        btn_atualizar.pack(pady=10)

    def create_remover_tarefa(self, frame):
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        inner_frame = tk.Frame(frame)
        inner_frame.pack(pady=10)

        tk.Label(inner_frame, text="ID da Tarefa:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_id = tk.Entry(inner_frame)
        entry_id.grid(row=0, column=1, pady=5)

        def remover():
            id_tarefa = entry_id.get().strip()
            if not id_tarefa:
                messagebox.showerror("Erro", "O ID da tarefa deve ser fornecido.")
                return

            sucesso = self.gestor.remover_tarefa(id_tarefa)
            if sucesso:
                messagebox.showinfo("Sucesso", "Tarefa removida com sucesso.")
                entry_id.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Tarefa não encontrada.")

        btn_remover = tk.Button(frame, text="Remover", command=remover)
        btn_remover.pack(pady=10)

    def create_escalonar_tarefas(self, frame):
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        tk.Label(frame, text="Escalonar Tarefas", font=("Helvetica", 14)).pack(pady=20)
        tk.Label(frame, text="Esta ação escalona todas as tarefas com mais de 15 dias no sistema.").pack(pady=10)

        def escalonar():
            sucesso = self.gestor.escalonar_tarefas()
            if sucesso:
                messagebox.showinfo("Sucesso", "Escalonamento concluído.")
            else:
                messagebox.showinfo("Informação", "Nenhuma tarefa foi escalonada.")

        btn_escalonar = tk.Button(frame, text="Escalonar Agora", command=escalonar)
        btn_escalonar.pack(pady=10)

    def create_excel_manager(self, frame):
        btn_voltar = tk.Button(frame, text="Voltar", command=lambda: self.show_frame("MenuPrincipal"))
        btn_voltar.pack(pady=5)

        tk.Label(frame, text="Importar/Exportar Tarefas", font=("Helvetica", 14)).pack(pady=20)

        def importar():
            ficheiro = filedialog.askopenfilename(
                title="Selecionar Ficheiro Excel",
                filetypes=(("Excel Files", "*.xlsx"),)
            )
            if ficheiro:
                try:
                    tarefas = self.excel_manager.importar_tarefas(ficheiro)
                    for tarefa in tarefas:
                        self.gestor.adicionar_tarefa(tarefa)
                    messagebox.showinfo("Sucesso", "Tarefas importadas com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao importar tarefas: {e}")

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

        btn_importar = tk.Button(frame, text="Importar Tarefas de Excel", command=importar)
        btn_importar.pack(pady=10)

        btn_exportar = tk.Button(frame, text="Exportar Tarefas para Excel", command=exportar)
        btn_exportar.pack(pady=10)

if __name__ == "__main__":
    app = Application()
