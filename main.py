from tkinter import *
from tkcalendar import Calendar
from tkinter import ttk , messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime ,timedelta , date
from sqlite3 import Error

from time import sleep
from fpdf import FPDF
import csv
import pandas as pd

import calendar
import sqlite3
import base64
import os





class App():
    def __init__(self,root):
        self.root = root
        self.banco = Banco()
        self.data_hora = Data_hora()
        self.banco.createdb()
        self.image_base64()
        

       
        #PRIMEIRO FRAME
        self.frames_registro_vnds = Frame(self.root,background='#CED5D6',width=950,height=650)
        self.frames_registro_vnds.place(x=1,y=1)
        self.frames_registro_vnds.bind("<Button-1>",self.fechar_frame_export)
    
        #FRAME: AREA DE TITULO
        self.frame_titulo = Frame(self.root,background='#172a38',width=950,height=50)
        self.frame_titulo.place(x=1,y=1)
        
        self.image_icon64 = PhotoImage(data=base64.b64decode(self.image_icon))
        self.image_icon64 = self.image_icon64.subsample(1, 1)
        self.labelImage_icon = Label(self.frame_titulo,image=self.image_icon64,height=45,width=45)
        self.labelImage_icon.place(x=10,y=1)
        self.text_vendas = Label(self.frame_titulo,text=f'VENDA DIÁRIA - REGISTRO DE CAIXA',foreground='white',background='#172a38', font=('Raleway',13))
        self.text_vendas.place(x=100,y=10)
        
        
        #LABEL E ENTRYS
        self.text_valor = Label(self.frames_registro_vnds,text=f'Valor *',foreground='#172a38',background='#CED5D6', font=('Raleway',13))
        self.text_valor.place(x=16,y=60)
        self.entry_valor = Entry(self.frames_registro_vnds,highlightbackground="black", highlightthickness=1, background="white",font=("arial",20),width=13)
        self.entry_valor.place(x=16,y=80)
        self.entry_valor.insert(0, "ex: 2,55")  # Default placeholder text
        self.entry_valor.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_valor.bind("<FocusOut>", self.on_entry_focus_out)
        self.text_frm_pagamento = Label(self.frames_registro_vnds,text=f'Forma de Pagamento *',foreground='#172a38',background='#CED5D6',padx=16, font=('Raleway',13))
        self.text_frm_pagamento.place(x=1,y=120)
        self.opcoes = ["Pix", "Cartão", "Dinheiro"]
        self.escolha = ''
        self.escolha = ttk.Combobox(self.frames_registro_vnds, values=self.opcoes,width=20)
        self.escolha.place(x=16, y=140)
        self.text_obs = Label(self.frames_registro_vnds,text=f'Observação',foreground='#172a38',background='#CED5D6', font=('Raleway',13))
        self.text_obs.place(x=16,y=170)
        self.entry_obs = Entry(self.frames_registro_vnds,highlightbackground="black", highlightthickness=1, background="white",font=("arial",20),width=18)
        self.entry_obs.place(x=16,y=190)
        
        
        #IMAGENS E BOTÕES
        self.image_add64 = PhotoImage(data=base64.b64decode(self.image_add))
        self.image_add64 = self.image_add64.subsample(2, 2)
        self.botao_com_imagem_e_texto = Button(self.frames_registro_vnds, text="ADICIONAR", image=self.image_add64, command=self.botao_add,highlightbackground="black", highlightthickness=1,background='white', compound=LEFT)
        self.botao_com_imagem_e_texto.place(x=20,y=240)
        self.image_export64 = PhotoImage(data=base64.b64decode(self.image_export))
        self.image_export64 = self.image_export64.subsample(2, 2)
        self.botao_com_imagem_e_texto = Button(self.frames_registro_vnds, text="EXPORTAR REGISTROS", image=self.image_export64, command=self.botao_exportar,highlightbackground="black", highlightthickness=1,background='white', compound=LEFT)
        self.botao_com_imagem_e_texto.place(x=340,y=240)
        self.image_graficos64 = PhotoImage(data=base64.b64decode(self.image_graficos))
        self.image_graficos64 = self.image_graficos64.subsample(2, 2)
        self.botao_grafico = Button(self.frames_registro_vnds, text="GRÁFICO", image=self.image_graficos64, command=self.frame_graficos,highlightbackground="black", highlightthickness=1,background='white', compound=LEFT)
        self.botao_grafico.place(x=600,y=240)
        
        #LABEL:Vendas FRAME: AREA DO QUANTIDADE DE VENDAS
        self.text_quant_vendas = Label(self.frames_registro_vnds,text=f'Vendas',foreground='white',background='#093A42',padx=16, font=('Raleway',13))
        self.text_quant_vendas.place(x=350,y=59)
        self.frames_quant_vendas = Frame(self.frames_registro_vnds,background='#AAC2C6',width=100,height=100)
        self.frames_quant_vendas.place(x=350,y=80)
        self.text_valor_vendas = Label(self.frames_quant_vendas,text=f'0',foreground='#093A42',background='#AAC2C6', font=('Raleway',25))
        self.text_valor_vendas.place(x=35,y=30)
        self.quantidade_vendas()  #INSERE A QUANTIDADE DE VENDAS
       
        #LABEL:Total Vendido FRAME: AREA DO VALOR DO TOTAL DE VENDAS
        self.text_valor_total = Label(self.frames_registro_vnds,text=f'Total Vendido',foreground='white',background='#093A42',padx=37, font=('Raleway',13))
        self.text_valor_total.place(x=480,y=59)
        self.frames_total_vendas = Frame(self.frames_registro_vnds,background='#AAC2C6',width=200,height=100)
        self.frames_total_vendas.place(x=480,y=80)
        self.text_valortotal_vendas= Label(self.frames_total_vendas,text=f'R$ 0,00',foreground='#093A42',background='#AAC2C6', font=('Raleway',25))
        self.text_valortotal_vendas.place(x=10,y=30)
        self.valor_total_vendas()   #INSERE O VALOR TOTAL DE VENDAS
        
        #AREA DE FORMA DE PAGAMENTO
        self.frames_forma_pagamento = Frame(self.frames_registro_vnds,background='#AAC2C6',width=220,height=123)
        self.frames_forma_pagamento.place(x=710,y=59)
        self.text_pix= Label(self.frames_forma_pagamento,text=f'Pix R$ 0,00',foreground='#093A42',background='#AAC2C6', font=('Raleway',13))
        self.text_pix.place(x=30,y=10)
        self.text_cartao = Label(self.frames_forma_pagamento,text=f'Cartão R$ 0,00',foreground='#093A42',background='#AAC2C6', font=('Raleway',13))
        self.text_cartao.place(x=30,y=50)
        self.text_dinheiro = Label(self.frames_forma_pagamento,text=f'Dinheiro R$ 0,00',foreground='#093A42',background='#AAC2C6', font=('Raleway',13))
        self.text_dinheiro.place(x=30,y=90)
        
        #LINHA HORIZONTAL
        self.canvas = Canvas(self.frames_registro_vnds,width=950, height=10,background='#CED5D6')
        self.canvas.create_line(950 ,10, 10, 10, width=3, fill='#093A42')
        self.canvas.place(x=1,y=285)
        self.canvas2 = Canvas(self.frames_registro_vnds,width=10, height=247,background='#CED5D6')
        self.canvas2.create_line(5,500, 6, 6, width=2, fill='#093A42')
        self.canvas2.place(x=320,y=45)
        
        #TREEVIEW
        self.tv_vendas = ttk.Treeview(self.frames_registro_vnds,height=15,columns= ('data','hora','valor','form_pag','obs'), show ='headings', selectmode='browse')
        self.tv_vendas.column('data',minwidth=0,width=150,anchor='center')
        self.tv_vendas.column('hora',minwidth=0,width=100,anchor='center')
        self.tv_vendas.column('valor',minwidth=0,width=100,anchor='center')
        self.tv_vendas.column('form_pag',minwidth=0,width=170,anchor='center')
        self.tv_vendas.column('obs',minwidth=0,width=190,anchor='center')
        self.tv_vendas.heading('data',text='Data')
        self.tv_vendas.heading('hora',text='Hora')
        self.tv_vendas.heading('valor',text='Valor')
        self.tv_vendas.heading('form_pag',text='Forma de Pagamento')
        self.tv_vendas.heading('obs',text='Observação')
        self.tv_vendas.place(x=120,y=300)
        self.tv_vendas.bind("<ButtonRelease-1>",self.frame_editor)
        
       
        #INSERE OS DADOS DENTRO DA TREEVIEW
        self.treeview_vendas()
        
        #INSERE OS VALORES NA AREA DE PAGAMENTO
        self.forma_pagamento()
       


    def on_entry_focus_in(self, event):
        if self.entry_valor.get() == "ex: 2,55":
            self.entry_valor.delete(0, END)
            self.entry_valor.config(fg="black")  # Change text color when focused
    def on_entry_focus_out(self, event):
        
        if not self.entry_valor.get():
            self.entry_valor.insert(0, "ex: 2,55")
            self.entry_valor.config(fg="grey")  # Change text color when not focused       
  
   

    def fechar_editor(self):
        self.frames_edt.destroy()
    def editar_registros(self):
        valortotal = self.valor_total_vendas()
        valortotal = valortotal.replace(',', '.')
        valor_tv = self.componentes_valor_tv[1]
        operacao = float(valortotal) - float(valor_tv)
        
        data = self.data_get
        hora = self.hora_get
        novo_valor = self.entry_valor2.get()
        frm_pagamento = self.escolhaedt.get()
        obs = self.entry_obs2.get()
        
        novo_valor_total = float(operacao) + float(novo_valor)
        self.banco.update_db(data,hora,novo_valor,novo_valor_total,frm_pagamento)
        messagebox.showinfo('registro de venda','Registro Alterado com Sucesso!')
        
        for i in self.tv_vendas.get_children():
           self.tv_vendas.delete(i)
           
        self.treeview_vendas()
        #INSERE OS VALORES NA AREA DE PAGAMENTO
        self.forma_pagamento()
        #self.quantidade_vendas()
        self.valor_total_vendas()
        self.fechar_editor()    
    def deletar_registros(self):
        valortotal = self.valor_total_vendas()
        quantidade = int(self.quantidade_vendas()) - 1
       
        valortotal = valortotal.replace(',', '.')
        valor_tv = self.componentes_valor_tv[1]
        novo_valor_total = float(valortotal) - float(valor_tv)
        
        data = self.data_get
        hora = self.hora_get
        self.banco.delete_db(data,hora,novo_valor_total,quantidade)
    
      
        messagebox.showinfo('registro de venda','Registro Excluido com Sucesso!')
       
        
        for i in self.tv_vendas.get_children():
           self.tv_vendas.delete(i)    
        self.treeview_vendas()
        self.forma_pagamento()
        self.quantidade_vendas()
        self.valor_total_vendas()
        self.fechar_editor()
    def frame_editor(self,event):
        try:
            itens_selecionados = self.tv_vendas.selection()

            if itens_selecionados != ():
            
                for item in itens_selecionados:
                    # Verifica se o item existe antes de tentar acessá-lo
                    if self.tv_vendas.exists(item):
                        valores_do_item = self.tv_vendas.item(item, 'values')
                        #print(valores_do_item)
                        
                    else:
                        print(f"Item {item} não encontrado na Treeview.")
                    
                    
                sleep(1.0)
                self.frames_edt = Frame(self.frames_registro_vnds,background='#CED5D6',width=950,height=330)
                self.frames_edt.place(x=1,y=300)
                
                self.btn_fechar = Button(self.frames_edt,text='FECHAR',command=self.fechar_editor,background='white',highlightbackground="black", highlightthickness=1,compound=LEFT)
                self.btn_fechar.place(x=10,y=1)
                self.text_valor = Label(self.frames_edt,text=f'Valor *',foreground='#172a38',background='#CED5D6', font=('Raleway',13))
                self.text_valor.place(x=30,y=80)
                self.entry_valor2 = Entry(self.frames_edt,highlightbackground="black", highlightthickness=1, background="white",font=("arial",20),width=13)
                self.entry_valor2.place(x=30,y=100)
                self.text_frm_pagamento = Label(self.frames_edt,text=f'Forma de Pagamento *',foreground='#172a38',background='#CED5D6',padx=16, font=('Raleway',13))
                self.text_frm_pagamento.place(x=300,y=80)
                self.opcoes = ["Pix", "Cartão", "Dinheiro"]
                self.escolhaedt = ''
                self.escolhaedt = ttk.Combobox(self.frames_edt, values=self.opcoes,width=20,font=('Raleway',13))
                self.escolhaedt.place(x=300, y=100)
                self.text_obs = Label(self.frames_edt,text=f'Observação',foreground='#172a38',background='#CED5D6', font=('Raleway',13))
                self.text_obs.place(x=590,y=80)
                self.entry_obs2 = Entry(self.frames_edt,highlightbackground="black", highlightthickness=1, background="white",font=("arial",20),width=18)
                self.entry_obs2.place(x=590,y=100)
                
                
                self.image_editar64 = PhotoImage(data=base64.b64decode(self.image_editar))
                self.image_editar64 = self.image_editar64.subsample(2, 2)
                self.btn_editar = Button(self.frames_edt,text='EDITAR',command=self.editar_registros,image=self.image_editar64,background='white',highlightbackground="black", highlightthickness=1,compound=LEFT)
                self.btn_editar.place(x=270,y=190)
                self.image_excluir64 = PhotoImage(data=base64.b64decode(self.image_excluir))
                self.image_excluir64 = self.image_excluir64.subsample(2, 2)
                self.btn_apagar = Button(self.frames_edt,text='EXCLUIR',command=self.deletar_registros,image=self.image_excluir64,background='white',highlightbackground="black", highlightthickness=1,compound=LEFT)
                self.btn_apagar.place(x=450,y=190)
                
                self.data_get = valores_do_item[0]
                self.hora_get = valores_do_item[1]
                self.valor_get = valores_do_item[2]
                self.componentes_valor_tv = self.valor_get.split(' ')
                
              
                self.entry_valor2.insert(0,self.componentes_valor_tv[1])
                self.escolhaedt.insert(0,valores_do_item[3])
                self.entry_obs2.insert(0,valores_do_item[4])
            else: messagebox.showerror('registro de venda','Selecione a Linha Especifica para Editar.')
        except UnboundLocalError as erro:
            messagebox.showerror('registro de venda','Selecione a Linha Especifica para Editar.')
            
            
   
    def fechar_grafico(self):

        try:
           sleep(0.5)
           self.frames_grfcos.destroy()
           self.botao_grafico2.destroy()
           self.image_graficos64 = PhotoImage(data=base64.b64decode(self.image_graficos))
           self.image_graficos64 = self.image_graficos64.subsample(2, 2)
           self.botao_grafico = Button(self.frames_registro_vnds, text="GRÁFICO", image=self.image_graficos64, command=self.frame_graficos,highlightbackground="black", highlightthickness=1,background='white', compound=LEFT)
           self.botao_grafico.place(x=600,y=240)
          
        except:
            print('o frame não está ativo')
    def abrir_calendario_dt_inicial(self):
        self.escolha1.config(state='normal')
        self.frames_calendario_inicial = Frame(self.frames_grfcos, background='#CED5D6', height=500, width=200)
        self.frames_calendario_inicial.place(x=1, y=28)
        # Cria o widget de calendário e o exibe
        self.calendario = Calendar(self.frames_calendario_inicial)
        self.calendario.pack(padx=10, pady=10)
        self.botao = Button(self.frames_calendario_inicial, text='OK', height=1, command=self.obter_data_inicial)
        self.botao.pack(padx=10,pady=10)  
    def abrir_calendario_dt_final(self):
        self.escolha2.config(state='normal')
        self.frames_calendario_final = Frame(self.frames_grfcos, background='#CED5D6', height=500, width=200)
        self.frames_calendario_final.place(x=1, y=89)
        # Cria o widget de calendário e o exibe
        self.calendario = Calendar(self.frames_calendario_final)
        self.calendario.pack(padx=10, pady=10)
        self.botao = Button(self.frames_calendario_final, text='OK', height=1, command=self.obter_data_final)
        self.botao.pack(padx=10,pady=10)
    def obter_data_inicial(self):
        self.frames_calendario_inicial.destroy()
        self.escolha1.delete(0,END)
        data_selecionada = self.calendario.selection_get()
    
        
        original_string = str(data_selecionada)
        componentes = original_string.split('-')
        data_invertida = '-'.join(componentes[::-1])
        self.escolha1.insert(0,data_invertida)      
    def obter_data_final(self):
        self.frames_calendario_final.destroy()
        self.escolha2.delete(0,END)
        data_selecionada = self.calendario.selection_get()
    
        
        original_string = str(data_selecionada)
        componentes = original_string.split('-')
        data_invertida = '-'.join(componentes[::-1])
        self.escolha2.insert(0,data_invertida)
    def limpar_grafico_anterior(self):
        self.frames_gerado.destroy()
        self.gerar_novo_grafico()    
    def gerar_novo_grafico(self):
    
        self.frames_novo_grd = Frame(self.frames_grfcos,background='#AAC2C6',width=600,height=285)
        self.frames_novo_grd.place(x=330,y=1)
        self.dados = self.banco.obter_dados_do_banco_de_dados(self.escolha1.get(),self.escolha2.get())
          # Extrair datas e valores para o gráfico
        self.datas = [str(row[0]) for row in self.dados]
        self.vendas = [int(row[1]) for row in self.dados]

        # Criar figura do matplotlib
        fig, ax = plt.subplots(figsize=(6, 3))  # Ajuste a largura e a altura conforme necessário
        ax.bar(self.datas, self.vendas, color='#7E92A8', label='Vendas')
        ax.scatter(self.datas, self.vendas, color='#093A42', marker='o', label='Vendas')  
        ax.set_xlabel('Data', fontsize=10)  # Ajuste o tamanho da fonte conforme necessário
        ax.set_ylabel('Vendas', fontsize=10)  # Ajuste o tamanho da fonte conforme necessário
        ax.set_title('Vendas por Dia', fontsize=10)  # Ajuste o tamanho da fonte conforme necessário
        plt.xticks(rotation=45, ha='right')
        ax.invert_xaxis()
        ax.legend()
        # Formatando o eixo y para exibir inteiros
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        # Ajuste de layout
        plt.tight_layout()
                    
        # Incorporar o gráfico em um Frame do Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.frames_novo_grd)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(x=1,y=1) 
        
       
    def gerar_grafico(self):
        
        self.frames_gerado = Frame(self.frames_grfcos,background='#AAC2C6',width=600,height=300)
        self.frames_gerado.place(x=330,y=1)
        self.dados = self.banco.obter_dados_do_banco_de_dados()

        # Extrair datas e valores para o gráfico
        self.datas = [str(row[0]) for row in self.dados]
        self.vendas = [int(row[1]) for row in self.dados]

        # Criar figura do matplotlib
        fig, ax = plt.subplots(figsize=(6, 3))  # Ajuste a largura e a altura conforme necessário
        ax.bar(self.datas, self.vendas, color='#7E92A8', label='Vendas')
        ax.scatter(self.datas, self.vendas, color='#093A42', marker=f'.', label='Vendas')  
        ax.set_xlabel('Data', fontsize=10)  # Ajuste o tamanho da fonte conforme necessário
        ax.set_ylabel('Vendas', fontsize=10)  # Ajuste o tamanho da fonte conforme necessário
        ax.set_title('Vendas por Dia', fontsize=10)  # Ajuste o tamanho da fonte conforme necessário
        plt.xticks(rotation=45, ha='right')
        ax.invert_xaxis()
        ax.legend()
        # Formatando o eixo y para exibir inteiros
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        # Ajuste de layout
        plt.tight_layout()
                    
        # Incorporar o gráfico em um Frame do Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.frames_gerado)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(x=1,y=1)
        
        
    def frame_graficos(self):    
        self.image_graficos64 = PhotoImage(data=base64.b64decode(self.image_graficos))
        self.image_graficos64 = self.image_graficos64.subsample(2, 2)
        self.botao_grafico2 = Button(self.frames_registro_vnds, text="FECHAR GRÁFICO", image=self.image_graficos64, command=self.fechar_grafico,highlightbackground="black", highlightthickness=1,background='white', compound=LEFT)
        self.botao_grafico2.place(x=600,y=240)
        
        self.frames_grfcos = Frame(self.frames_registro_vnds,background='#CED5D6',width=950,height=330)
        self.frames_grfcos.place(x=1,y=300)
        
      
        self.text_data_inicio = Label(self.frames_grfcos,text=f'Data Inicial',foreground='#172a38',background='#CED5D6', font=('Raleway',13))
        self.text_data_inicio.place(x=16,y=1)
        self.escolha1 = Entry(self.frames_grfcos,state='disabled', width=15,font=('Raleway',13),background='white',highlightbackground="black", highlightthickness=1)
        self.escolha1.place(x=16, y=26)
        self.botao1 = Button(self.frames_grfcos, text='⇩', height=1, command=self.abrir_calendario_dt_inicial,background='white',highlightbackground="black", highlightthickness=1)
        self.botao1.place(x=185, y=25)
        
        
        self.text_data_final = Label(self.frames_grfcos, text='Data Final', foreground='#172a38', background='#CED5D6', font=('Raleway', 13))
        self.text_data_final.place(x=16, y=70)
        self.escolha2 = Entry(self.frames_grfcos,state='disabled', width=15,font=('Raleway',13),background='white',highlightbackground="black", highlightthickness=1)
        self.escolha2.place(x=16, y=90)
        self.botao2 = Button(self.frames_grfcos, text='⇩', height=1, command=self.abrir_calendario_dt_final,background='white',highlightbackground="black", highlightthickness=1)
        self.botao2.place(x=186, y=89)
        
        self.gerar_grafico()
         
        self.btn_gerar_grafico = Button(self.frames_grfcos,command=self.gerar_novo_grafico,text='GERAR GRÁFICO',image=self.image_graficos64,background='white',highlightbackground="black", highlightthickness=1,compound=LEFT)
        self.btn_gerar_grafico.place(x=18,y=140)
        
       
       
       
    def fechar_frame_export(self,event):
        try:
           self.frame_export.destroy()
        except:
            print('o frame não está ativo')         
    def frame_op_export(self):
        self.frame_export = Frame(self.frames_registro_vnds,background='#CED5D6',width=240,height=50)
        self.frame_export.place(x=340,y=240)
       
    
        self.image_export64_excel = PhotoImage(data=base64.b64decode(self.image_export_excel))
        self.image_export64_excel = self.image_export64_excel.subsample(1, 1)
       
        self.image_export64_pdf = PhotoImage(data=base64.b64decode(self.image_export_pdf))
        self.image_export64_pdf = self.image_export64_pdf.subsample(1, 1)
        
        self.image_export64_csv = PhotoImage(data=base64.b64decode(self.image_export_csv))
        self.image_export64_csv = self.image_export64_csv.subsample(1, 1)
        
        self.opcao1_excel = Button(self.frame_export, image=self.image_export64_excel, background='white', height=39, compound=LEFT, highlightbackground="black", highlightthickness=2,command=self.botao_export_excel)
        self.opcao2_pdf = Button(self.frame_export, image=self.image_export64_pdf, background='white', height=39, compound=LEFT, highlightbackground="black", highlightthickness=2,command=self.botao_export_pdf)
        self.opcao3_csv = Button(self.frame_export, image=self.image_export64_csv, background='white', height=39, compound=LEFT, highlightbackground="black", highlightthickness=2,command=self.botao_export_csv)
          
        self.opcao1_excel.place(x=1,y=1)
        self.opcao2_pdf.place(x=75,y=1)
        self.opcao3_csv.place(x=150,y=1)
    def botao_add(self):
        try:
            valor = self.entry_valor.get()
            forma_pagamento = self.escolha.get()
            obs = self.entry_obs.get()
            
            if valor == '' or forma_pagamento == '' or valor == 'ex: 2,55':
                messagebox.showerror('registro de venda','Alguns Campos estão em Branco.')
            else:
                if forma_pagamento != 'Pix' and  forma_pagamento != 'Cartão' and  forma_pagamento != 'Dinheiro':
                    messagebox.showerror('registro de venda','Forma de Pagamento não Encontrada.')
                    self.clear_entrys()
                else:
                    data = self.data_hora.data()
                    hora = self.data_hora.hora()
                
                    if self.banco.get_valor_total() == None:
                      
                        print('se o valor total for igual a None,então entra aqui, primeira venda do banco')
                        quantidade_vendas = 1
                        valor = str(valor).replace(',','.')
                        valor_total = float(valor)
                    else:
                        #depois que for feita a primera venda sempre vai entrar aqui, enquanto a data for igual
                        if self.banco.get_data() == self.data_hora.data():
                            print('Se a data for igual a data, então entra aqui...')
                            quantidade_vendas = int(self.quantidade_vendas()) + 1
                            valor = str(valor).replace(',','.') 
                            get_valor_total = self.banco.get_valor_total()
                            valor_total = float(get_valor_total) + float(valor)
                            valor_total = str(valor_total)
                       
                    
                
                    self.banco.insert_table_vendas_diarias(data,hora,quantidade_vendas,valor,valor_total,forma_pagamento)
                    messagebox.showinfo('Registro de Venda','Adicionado com Sucesso!')
                
                    self.quantidade_vendas()
                    self.valor_total_vendas()
                    self.limpar_treeview()
                    self.treeview_vendas()
                    self.forma_pagamento()
                    self.clear_entrys()
        except Exception as e:
            print(e)
            messagebox.showinfo('Registro de Venda','O Valor está no Formato Incorreto.')
            self.clear_entrys()
                
            print('houve um erro')
    def botao_exportar(self):
        self.frame_op_export()
    def botao_export_excel(self):
        self.banco.get_registros_for_excel()
        messagebox.showinfo('excel','Exportado com Sucesso!')
        self.frame_export.destroy()
    def botao_export_pdf(self):
        self.banco.get_registros_for_pdf()
        messagebox.showinfo('pdf','Exportado com Sucesso!')
        self.frame_export.destroy()
    def botao_export_csv(self):
        self.banco.get_registros_for_csv()
        messagebox.showinfo('csv','Exportado com Sucesso!')
        self.frame_export.destroy()


    def quantidade_vendas(self):
        result = self.banco.get_vendas_diarias()
        for quant in result:
            if quant[0] != None:
               self.text_valor_vendas.configure(text=f'{quant[0]}')
               return quant[0]
            else:
                return 0             
    def valor_total_vendas(self):
        result = self.banco.get_valor_total()
        valor = result
        if valor != None:
            valor =  "{:.2f}".format(float(valor)).replace('.', ',')
            valor2 = valor.replace(',', '.')
            valor_format = float(valor2)
            if valor_format >= 1000.0:
                self.text_valortotal_vendas.configure(text=f'R$ {valor}',font=('Raleway',21))
            self.text_valortotal_vendas.configure(text=f'R$ {valor}')
            return valor
        else:
            return 0   
    def forma_pagamento(self):
        
        pix = self.banco.get_soma_total_pix()
        cartao =  self.banco.get_soma_total_cartao()
        dinheiro = self.banco.get_soma_total_dinheiro()
       
        if pix == None:
            pix = '0,00'
            self.text_pix.configure(text=f'Pix R$ {pix}')
        else:
            pix = self.banco.get_soma_total_pix()
            #pix = str(pix).replace('.',',')
            pix =  "{:.2f}".format(float(pix)).replace('.', ',')
            self.text_pix.configure(text=f'Pix R$ {pix}')
            
        if cartao == None:
            cartao = '0,00'
            self.text_cartao.configure(text=f'Cartão R$ {cartao}')
            
        else:
            cartao =  self.banco.get_soma_total_cartao()
            #cartao = str(cartao).replace('.',',')
            cartao =  "{:.2f}".format(float(cartao)).replace('.', ',')
            self.text_cartao.configure(text=f'Cartão R$ {cartao}')
            
        if dinheiro == None:
            dinheiro = '0,00'
            self.text_dinheiro.configure(text=f'Dinheiro R$ {dinheiro}') 
        else:
           dinheiro = self.banco.get_soma_total_dinheiro()
           #dinheiro = str(dinheiro).replace('.',',')
           dinheiro =  "{:.2f}".format(float(dinheiro)).replace('.', ',')
           self.text_dinheiro.configure(text=f'Dinheiro R$ {dinheiro}') 
    def treeview_vendas(self):
        for (id,data,hora,valor,frm_pagamento) in self.banco.get_table_vendas_diarias():
            self.tv_vendas.insert("","end",values = (data,hora,f'R$ {valor}',frm_pagamento,'xxx'))          
    def limpar_treeview(self):
        # Obtem todas as linhas da treeview e as remove
        tree = self.tv_vendas
        for item in tree.get_children():
             tree.delete(item)
    def clear_entrys(self):
        self.entry_valor.delete(0,END)
        self.escolha.delete(0,END)
        self.entry_obs.delete(0,END) 
    def image_base64(self):
        self.image_add = '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'
        
        self.image_icon = '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'
      
        self.image_export = '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'
        
        self.image_export_excel = 'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAL6UExURfj5+fv8/P////7+/vf6+PT59vT49vn8+vj7+nCtiz+QYkKSZUCRY12hetzr4vb6+EWTZwRuMghwNQZvNCaCSzeMVkuXa9/s5EeVaQdwNQtyOAhwNkKSXrfXsD2PW+Dt5UCRXdjqxrzatDuOWk2YbNXpxN/vy7vZszmNWE+YbuPu59ztyd7uy7nYsjiMWFGaceTv6dfqxuHwzLrZszmNWVSbc+Tv6AhxNjaLVq3RqrPUr7PUrrXWsI2+lR19RZK/pQpyOAlxNwpyNw1zORd5QRl6Qhl6Qxp7Qw1zOom6nhR3PyaBTSWBTSOATA91PApxN4u7nwlxNjCHVcXdz3+1lQxyOIO3meHt5q3Puxx8RYq7no+9o+Dt5DiLXOXw6fz9/GSlgIm7niuEUdbn3Yy8nw50OpzFrRV3P2+sif3+/t/t5G+riOz07+fx6z6PYYq7nxt7Rb/ZyvH38oa5m2WlgN3r4iqEUBJ2PaPJs/r8+/P49VygeV6ievj7+Njo3469of3+/c3i1iSATApxOCeCT9Dk2Huykg91OSOHPiaKPySJPZbGopC+o9Ll2SWBTGCjfOvz7kWTZhN5OzydRUKaSkGVSpG7muHk5+3v8EqWavz9/XGsihh6QrrWxrbVwhN4OjucRUJ4WERfYkxkalFlb56qrzyOX2engl6iezWKWmamgV+jex19RkJ1WURYZUNZZEBWYZaiqBJ4OkJ1WkRZZERaZEFXYpajqBp+PSeKQCaKQCuNQT6fRkF1WkFXYZekqSmLQUOhR0KVTEKTTEGTTEJwW0JYYoaVm9vh4dnf4ODl5R+DPz+eR0J7V0ReYkRcY0lfaE9lbZ+tr0GaSkJsXXiKj+/y8hB2OjOVQ0KTTUNjYGF2fN3j40WUZxN5OTeZQj+ITkJdYUNZY1Job8bQz2+riT6PYEGQY0CQY0CQYkGRY1KeaGixb2OPdkddZ0heZ6u4ufX59vH39PL39PT49e3z74aYmkJZYo6dofj6+eXq6Zioqent7fv9/E0PJFAAAAABYktHRAJmC3xkAAAAB3RJTUUH6AIIEBUx8/oNngAAAhhJREFUSMdjYGAkFTAwMpEKBqsWZvprYWFFBmzshP3CwcnFjQR4ePkIauEXEBRCAGERUTFxQlpYJCSlEEBaRlZOTJ40LQqKSsoq8qRpUVVT19DUIk2Lto6unr4BKVoM1dSMjE1MzYjWYm5haWVtbWNrZ09Yi4OjowOQcnJ2cXVzc3P38CSsxcvbx8tJysnLx9fPHwikAwhqCQwKlg+RkgoNC4+I9Afxowjb4hHNFBMkHBsXnxAI9lMiYS2BSclMKalpTBHpTmAuYYcBFWVkZmXn5OZJQ3j5RGjxLyhkKmIuhgU2EQ6TkpIsiWcqLQuEaiHGFqfyCqbKqmqIu4hzmHRNbV19Q2OTI5Dd3CxNRFQGtrQytRUEM0WFSkm1d3R2dRPW4tzD1Nsn3F85YaK01KTJU6ZOmz6DUOzPzJk129x/zlymeW7+8xcsXLR4yVJCtixbvgKYUhxXrlq9xnH+grXr1m/YSNAvkpL+UKp504LNW7Zu2044XqBgx85du/fs3bJ1335itTQfOHjo8JGjW7YeO37i5ClGorScPnP23LnzW7duvXDx4qV4ohzmvPvylS1bQWDb1WvE+UXq+o2bt0B6jt2+g8Mv/HeRC1ggkLx3/8HDLVsfPX6Cy/scT589f/78BRA/fwkmXz1//ebtu0fvP+AMMaaPnz6jgy9fv33/8RO3Fqzg1+8/TCRqYfrLRLIWplEtQ0MLAAtA8OEOCAOwAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI0LTAyLTA4VDE2OjIxOjEyKzAwOjAwhuuRrwAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wMi0wOFQxNjoyMToxMiswMDowMPe2KRMAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjQtMDItMDhUMTY6MjE6NDkrMDA6MDDqRFJSAAAAAElFTkSuQmCC'
        
        self.image_export_pdf = 'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAJkUExURfn5+vz8/Pv8/Pv7/P////7+/v39/v39/f74+P309P77+/75+fKxsOdwbuVkYuVkYeRkYuicnPvz8/Gsq99APd04Nd44Nd05N9ddXuSfoPvy8v3y8t47ON48OdddX9Vsb+Ocnvvx8fvo6OJTUN45NtheX9VtcNVrbuOanPvw8Pvo5+JSUOKYmvvu7+KXmPrt7thdX+GVl/rs7dlVVeGTlfrr691CQNdhY9VscNVrb+CSlPnq6t1BP9hSUdRYWdNYWdNWV+CDg/zz8946N9o5NtQ3NNE1MtE0MdZMSvnn5t06N9c4NdI1MtEzMNZNSvrn59s5NtU3NN07ONg3NNhOS+BRT/vn599CP99EQd9BPt9DQeFLSeFLSOJST+BEQfKwr/fS0ffPzvGtq+NaV++fnffR0PbLy+Zrae2WlPne3fnd3fne3vnf3ul6eOFPTeBHRPnZ2P739/O8uv78/PXExPTAv/S/vvO7uvzu7uh4dvGrqvO4t+2Xlu6ZmORfXeJRTvjY1/vl5eFOS/rj4/vm5uJUUfS+veh5d/bLyt9DQPGpqP/+/uZqZ+ZpZ/jX1v319PGsqv/8/PXFxOVlYt03NOFMSvri4fCop/3z8+ViYOJQTfjW1vfPz949OuVjYN00MeNcWvzt7fna2uBIRu2Vk+VmZONYVd4+O/76+uuKiOh2dPXGxfGqqf/9/edzcd01MvjV1Prj4uFPTPO6ufzw8Pvn5u+kouBJRvCmpf329edzcN8/POZtaudxb+RdWudubOZta+VnZeBKR/3x8eRiX+RhX/3x8PClo/CpqONbWONbWf329gSByKoAAAABYktHRASPaNlRAAAAB3RJTUUH6AIIEQ4cHtHwRgAAAgBJREFUSMdjYGBkIg0wMjCzkApI18JKuhY20rWw00ULGQ5D8z4HJzLgIqyFm4eXDwH4BQSFsOpB1iIsIiqGBMQlJKUIaJHmE5NBBrJy8gqK+LUoKaugalFVU9fQxKtFSxtDi7y6ji6pWuTV9fRJ0WIA1CKvbmhEvBYZY5AWeXUTU+K1mJlbqAGBpZU10VpkbGzt7IHAwdGJaC0yzi6ubm5u7h6exGuRkfHy9nHz9fMnRYuMTEAgyVpkgoJD8Gtxdob4AkYBgUpoGB4tsuEREeGyKjKREVGRMkATIqJjYmJEYrVwa3GOi09ISExKlk1JSE2LT5d1zsjMys7JzcOnJb+gULiouCS/lKWsvKKiUqWKpbqmtq4er5aGxpim5pbWtkI+lXaOjs6u7pqe3ji8Dsvv659QPnFSflnh5ClTpzU3TWeZUdE4cxZeLbO5GuYIJ88tK5w3f8HCRYu7upcsXRqB35YGrWWRsirLy1asXLWaJUVmzdp168VUtPFq2bBxEzBsl29esWXL1m3bVXbs3CUmg1eLzO49e8NBuWvf/gMHW+c6yyw7cMiZgBYZFUgpowIslFTANDAVENCCDQy0FiXcWpRwaDl8RAy7FrGjx3BoYdmxXEwFCxBbfpwFl5bCE0tPnjyFBk6eXDr9NE4tLCycC7EAThYWPFqIAqNa6KAFAPw16PZORtxeAAAAJnRFWHRDcmVhdGlvbiBUaW1lAHF1aSAwOCBmZXYgMjAyNCAxMjo1OTo0MfEzSQYAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjQtMDItMDhUMTc6MTQ6MjErMDA6MDCb0fgRAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDI0LTAyLTA4VDE3OjE0OjIxKzAwOjAw6oxArQAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyNC0wMi0wOFQxNzoxNDoyOCswMDowMCgBJKEAAAAZdEVYdFNvZnR3YXJlAGdub21lLXNjcmVlbnNob3TvA78+AAAAAElFTkSuQmCC'
        
        self.image_export_csv = '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'
        
        
        self.image_graficos = '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'
        
        self.image_editar =   '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'
        
        self.image_excluir = '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'




class Banco():
    def __init__(self):
        self.nomebanco  = "vendas_diarias.db"
        self.data_hora = Data_hora()
     
    def createdb(self):
        conexao = self.ConexãoBanco()
        if conexao:
            self.cursor = conexao.cursor()
            sql1 = """CREATE TABLE IF NOT EXISTS vendas_diarias (
                    id          INTEGER   PRIMARY KEY,
                    data        DATE      NOT NULL,
                    hora        TIME      NOT NULL,
                    quant_venda INT       NOT NULL,
                    valor       TEXT     NOT NULL,
                    valortotal  TEXT     NOT NULL,
                    frm_pagamento   CHAR   NOT NULL
                    );"""
            self.cursor.execute(sql1)
            conexao.commit()
        else:
            print("Erro na obtenção da conexão com o banco de dados.")
    def ConexãoBanco(self):
        Con = None
        try:
            Con = sqlite3.connect(self.nomebanco)
            print("Conectado com o", self.nomebanco)
        except Error as ex:
            print(ex)
        return Con
    def dql(self,query): #select
        try:
            Vcon = self.ConexãoBanco()
            c = Vcon.cursor()
            c.execute(query)
            res = c.fetchall()
            Vcon.close()
            return res
        except Error as ex:
            print(ex)
    def dml(self,query): #insert, update, delete
        try:
            Vcon = self.ConexãoBanco()
            c = Vcon.cursor()
            c.execute(query)
            Vcon.commit()
            Vcon.close()
        except Error as ex:
            print(ex)
    def insert_table_vendas_diarias(self,data,hora,quan_venda,valor,valortotal,frm_pagamento):
        sql = f'INSERT INTO vendas_diarias (data,hora,quant_venda,valor,valortotal,frm_pagamento) VALUES ("{data}","{hora}","{quan_venda}","{valor}","{valortotal}","{frm_pagamento}")'
        self.dml(sql)
    def get_vendas_diarias(self):
        #pega as vendas diarias no banco
        sql = f'SELECT MAX(quant_venda) FROM vendas_diarias WHERE  data="{self.data_hora.data()}"'
        result = self.dql(sql)
        return result 
    def get_valor_total(self):
        sql = f'SELECT valortotal FROM vendas_diarias WHERE data="{self.data_hora.data()}" ORDER BY id DESC LIMIT 1;'
        result = self.dql(sql)
       
        for valor in result:
         return valor[0]
        
    def get_soma_total_pix(self):
        sql = f'SELECT SUM(valor) FROM vendas_diarias WHERE frm_pagamento="Pix" and data="{self.data_hora.data()}"'
        result = self.dql(sql)
        return result[0][0]
    def get_soma_total_cartao(self):
        sql = f'SELECT SUM(valor) FROM vendas_diarias WHERE frm_pagamento="Cartão" and data="{self.data_hora.data()}"'
        result = self.dql(sql)
        return result[0][0] 
    def get_soma_total_dinheiro(self):
        sql = f'SELECT SUM(valor) FROM vendas_diarias WHERE frm_pagamento="Dinheiro" and data="{self.data_hora.data()}"'
        result = self.dql(sql)
        return result[0][0]
        
    def get_table_vendas_diarias(self):
        sql = f'SELECT id,data,hora,valor,frm_pagamento FROM vendas_diarias WHERE data="{self.data_hora.data()}"'
        result = self.dql(sql)
        return result  
    def get_data(self):
        sql = f'SELECT data FROM vendas_diarias ORDER BY id DESC LIMIT 1;'
        result = self.dql(sql)
        
        for data in result:
            return data[0]  
  
  
    def get_registros_for_excel(self):
        #consulta_sql = f"SELECT * FROM vendas_diarias WHERE data='{self.data_hora.data()}' "
        inicio_mes , final_mes, ano_atual, mes_atual = self.data_hora.primeiro_e_ultimo_dia_do_mes()
    
        data = datetime(ano_atual, mes_atual, 1)
        mes_ano = data.strftime('%m-%Y')
      
        consulta_sql = (
            f"SELECT * FROM vendas_diarias WHERE "
            f"SUBSTRING(data, 4, 2) || '-' || SUBSTRING(data, 7, 4) = '{mes_ano}'")
        
        df = pd.read_sql_query(consulta_sql, self.ConexãoBanco())
        df.to_excel(f'{self.data_hora.data()}.xlsx', index=False)
        
    def get_registros_for_pdf(self):
        inicio_mes , final_mes, ano_atual, mes_atual = self.data_hora.primeiro_e_ultimo_dia_do_mes()
    
        data = datetime(ano_atual, mes_atual, 1)
        mes_ano = data.strftime('%m-%Y')
      
        consulta_sql = (
            f"SELECT * FROM vendas_diarias WHERE "
            f"SUBSTRING(data, 4, 2) || '-' || SUBSTRING(data, 7, 4) = '{mes_ano}'")
        
        retorno = self.dql(consulta_sql)
        
        if os.path.exists('arq.txt'):
          os.remove('arq.txt')
        
        for dados in retorno:
            with open('arq.txt', 'a') as arquivo:
               #print('ID - DATA - HORA - QUANTIDADE - VALOR - V_TOTAL - FORMA DE PAGAMENTO', file=arquivo)
               print(dados,file=arquivo)
            arquivo.close()  
           
         # Create PDF
        pdf = FPDF()
        pdf.add_font("LiberationSans", style="", fname="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", uni=True)
        
        # Set paper size to A4 (210x297 mm)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set font and size
        pdf.set_font("LiberationSans", size=12)

        # Open the text file in read mode
        with open("arq.txt", "r") as f:
            # Insert the texts in the pdf
            for x in f:
                pdf.cell(200, 10, txt=x, ln=1, align='C')  # align='C'

        # Save the pdf with name .pdf
        pdf.output(f"{self.data_hora.data()}.pdf")

        # Close the file
        os.remove('arq.txt')  # Optionally remove the file after creating the PDF
    
    def get_registros_for_csv(self):
        inicio_mes , final_mes, ano_atual, mes_atual = self.data_hora.primeiro_e_ultimo_dia_do_mes()
         
        data = datetime(ano_atual, mes_atual, 1)
        mes_ano = data.strftime('%m-%Y')
      
        consulta_sql = (
            f"SELECT * FROM vendas_diarias WHERE "
            f"SUBSTRING(data, 4, 2) || '-' || SUBSTRING(data, 7, 4) = '{mes_ano}'"
        )
        retorno = self.dql(consulta_sql)
      
        # Escrever os dados para o arquivo CSV
        with open(f"{self.data_hora.data()}.csv", 'w', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)
            #Escrever os cabeçalhos das colunas
            headers = ['ID','DATA','HORA','QUANTIDADE','VALOR','V_TOTAL','FORMA DE PAGAMENTO'] 
            escritor_csv.writerow(headers)
            #Escrever os dados
            escritor_csv.writerows(retorno)
    
    
  
  


  
    def obter_dados_do_banco_de_dados(self, datainicial=None, datafinal=None):
        if datainicial is None or datafinal is None:
            # Se as datas não forem fornecidas, obter os dados dos últimos cinco dias
            data_final = datetime.now().strftime('%d-%m-%Y')
            data_inicial = (datetime.now() - timedelta(days=4)).strftime('%d-%m-%Y')
        else:
            data_inicial = datainicial
            data_final = datafinal
        
        consulta_sql = f"SELECT data, quant_venda FROM vendas_diarias WHERE data BETWEEN '{data_inicial}' AND '{data_final}' ORDER BY id DESC;"
        self.cursor.execute(consulta_sql)
        dados = self.cursor.fetchall()
       
        return dados

    
    def update_db(self,data,hora,valor,valortotal,frm_pagamento):
        sql = f'UPDATE vendas_diarias SET valor="{valor}",frm_pagamento="{frm_pagamento}" WHERE data="{data}" and hora="{hora}";'
        
        self.dml(sql)
        
        
        sql = f'UPDATE vendas_diarias SET valortotal="{valortotal}"WHERE data="{self.data_hora.data()}" ORDER BY id DESC LIMIT 1'

        self.dml(sql)
        
    def delete_db(self,data,hora,novo_valor_total,quantidade):
        sql = f'DELETE FROM vendas_diarias WHERE data="{data}" and hora="{hora}"'
        self.dml(sql)
        
        
        sql = f'UPDATE vendas_diarias SET quant_vendas="{quantidade}, "valortotal="{novo_valor_total}"WHERE data="{self.data_hora.data()}" ORDER BY id DESC LIMIT 1'
        self.dml(sql)
        
        
        
        
 
        
class Data_hora():
    
    def data(self):
        agora_datetime = datetime.now()
        sql_formatted_date = agora_datetime.strftime("%d-%m-%Y")
        return sql_formatted_date
    
    def hora(self):
        agora_datetime = datetime.now()
        sql_formatted_time = agora_datetime.strftime(" %H:%M:%S")
        return sql_formatted_time
    
    
    
    def primeiro_e_ultimo_dia_do_mes(self):
        data = date.today()
        ano = data.year
        mes = data.month
        
        primeiro_dia = datetime(ano, mes, 1)
        ultimo_dia = datetime(ano, mes, calendar.monthrange(ano, mes)[1])
        
        inicio_mes_str = primeiro_dia.strftime('%d-%m-%Y') 
        fim_mes_str = ultimo_dia.strftime('%d-%m-%Y')


        return inicio_mes_str , fim_mes_str,ano, mes
        #print(f'Início do mês: {inicio_mes_str}')
        #print(f'Final do mês: {fim_mes_str}')
        
        
if __name__ == '__main__':
    gui = Tk()
    gui.title('Registro de Vendas')
    gui.geometry('950x630+300+30')
    gui.config(background='#895E5E')   
    
    img = 'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEcWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRhLyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRyaWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgogICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxBdHRyaWI6Q3JlYXRlZD4yMDI0LTAyLTA2PC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkV4dElkPjlmNTMzNzdkLWZmNjQtNDhjZC1iODE0LTdlZTlmYzUzZjE4MDwvQXR0cmliOkV4dElkPgogICAgIDxBdHRyaWI6RmJJZD41MjUyNjU5MTQxNzk1ODA8L0F0dHJpYjpGYklkPgogICAgIDxBdHRyaWI6VG91Y2hUeXBlPjI8L0F0dHJpYjpUb3VjaFR5cGU+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvQXR0cmliOkFkcz4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvJz4KICA8ZGM6dGl0bGU+CiAgIDxyZGY6QWx0PgogICAgPHJkZjpsaSB4bWw6bGFuZz0neC1kZWZhdWx0Jz5EZXNpZ24gc2VtIG5vbWUgLSAxPC9yZGY6bGk+CiAgIDwvcmRmOkFsdD4KICA8L2RjOnRpdGxlPgogPC9yZGY6RGVzY3JpcHRpb24+CgogPHJkZjpEZXNjcmlwdGlv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'
    gui.call('wm', 'iconphoto', gui._w, PhotoImage(data=base64.b64decode(img)))
    gui.iconname('Registro de Venda')
    gui.resizable(0,0)
    spk = App(gui)
    gui.mainloop()
    