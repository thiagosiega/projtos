import google.generativeai as genai
import os
import tkinter as tk
import re
import subprocess

# Constantes
FILE_COMANDOS = "comandos/"
COMANDOS_VALIDOS = ["olamundo", "janela", "infor_personagem"]

class GemineApp:
    def __init__(self):
        self.FILE_KEY = "KEY.txt"
        self.setup_api()
        
        self.root = tk.Tk()
        self.root.title("Gemine")
        
        self.create_widgets()
        self.root.mainloop()

    def setup_api(self):
        """Configura a API com a chave fornecida no arquivo KEY.txt."""
        if not os.path.exists(self.FILE_KEY):
            raise FileNotFoundError(f"Arquivo {self.FILE_KEY} não encontrado.")
        
        with open(self.FILE_KEY, "r") as file:
            key = file.read().strip()
        
        genai.configure(api_key=key)

    def create_widgets(self):
        """Cria os widgets da interface do usuário."""
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.entrada_texto = tk.Entry(input_frame, width=30)
        self.entrada_texto.pack(side=tk.LEFT, padx=(0, 10))

        self.botao_enviar = tk.Button(input_frame, text='Enviar', command=self.processar_comando)
        self.botao_enviar.pack(side=tk.LEFT)

        self.resultado = tk.Text(self.root, wrap=tk.WORD)
        self.resultado.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.resultado.tag_configure("comando", foreground="yellow")  # Configura a tag para comando

    def processar_comando(self):
        """Processa o comando inserido pelo usuário."""
        texto_usuario = self.entrada_texto.get()
        resultado = self.gerar_resposta(texto_usuario)
        
        self.resultado.delete(1.0, tk.END)  # Limpa o campo de texto
        texto_formatado = self.aplicar_filtros(resultado)
        self.resultado.insert(tk.END, texto_formatado)

    def gerar_resposta(self, texto):
        """Gera uma resposta usando a API generativa."""
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        instrucoes = (
            "Você imitará uma personalidade de um personagem de anime/vtuber\n"
            "Onde você tem alguns comandos pré-programados\n"
            "Instruções: todo comando deve ser precedido por $& e sucedido por $&\n"
            f"Comandos disponíveis: {COMANDOS_VALIDOS}\n"
            "Exemplo: $&olamundo$&\n"
            "Não execute comandos sem serem requisitados!\n"
            "Com isso, responda ao seguinte texto:\n"
            f"{texto}"
        )

        try:
            response = model.generate_content(instrucoes)
            return response.text if hasattr(response, 'text') else "A resposta não contém texto."
        except Exception as e:
            return f"Erro ao gerar conteúdo: {str(e)}"

    def executar_comando(self, comando):
        """Executa um comando se ele for válido."""
        if comando not in COMANDOS_VALIDOS:
            return f"Comando inválido: {comando}"

        try:
            subprocess.run(
                [f"python3 {FILE_COMANDOS}{comando}.py"], 
                shell=True, 
                capture_output=True, 
                text=True
            )
        except FileNotFoundError:
            return f"Arquivo para o comando não encontrado: {comando}"

    def aplicar_filtros(self, texto):
        """Aplica filtros no texto, substituindo comandos por seus resultados."""
        matches = re.findall(r'\$&(.*?)\$&', texto)
        for match in matches:
            resultado = self.executar_comando(match)
            texto = texto.replace(f"$&{match}$&", f"{match} (resultado: {resultado})")  # Mantém o comando
            # Adiciona o comando em amarelo
            self.resultado.insert(tk.END, f"{match} ", "comando")  # Insere o comando com a tag
        return texto

if __name__ == "__main__":
    try:
        GemineApp()
    except FileNotFoundError as e:
        print(e)
