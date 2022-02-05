import pandas as pd
import PySimpleGUI as sg

#primeiro app descente finalizado em 26/11/2021! Continue dando duro, e lembre-se, não é necessário decorar
#é necessário compreender.

#leia o about

df = pd.read_excel("dados.xlsx") #leitura da planilha
user=df['users'] #definindo a planilha com apenas o usuarios
user_list = df['users'].tolist() #criando uma lista com todos os usuarrios

def janela_painel(): #janela principal
    sg.theme('dark')
    layout = [
       [sg.Text('Usuário', size=(8,1)), sg.Input(key='user', size=(12,1), do_not_clear=False)],
        [sg.Text('Senha', size=(8,1)), sg.Input(key='pass', size=(12,1), do_not_clear=False)],
        [sg.Button('Entrar', size=(10,1), button_color='green'), sg.Button('Cancelar', size=(10,1), button_color='red')]
    ]
    return sg.Window('Painel', layout=layout, finalize=True,  icon='logo.ico')

def janela_banco(): #janela de escolha sacar/depositar
    sg.theme('dark')
    layout = [
        [sg.Button('Sacar', button_color='black',size=(10,1)),sg.Button('Depositar', button_color='orange', size=(10,1))],
        [sg.Button('Voltar', button_color='blue',size=(10,1)),
        sg.Button('Cancelar', button_color='red',size=(10,1))],
    ]
    return sg.Window('Painel', layout=layout, finalize=True,  icon='logo.ico')

def janela_deposito(): #janela de deposito
    sg.theme('dark')
    layout=[[sg.Text('Valor', size=(8,1)), sg.Input(key='deposito', size=(12,1), do_not_clear=False)],
        [sg.Button('Confirmar', button_color='green'), sg.Button('Voltar', button_color='blue'),
        sg.Button('Cancelar', button_color='red')],
    ]
    return sg.Window('Painel', layout=layout, finalize=True,  icon='logo.ico')

def janela_saque(): #jnaela de saque
    sg.theme('dark')
    layout = [[sg.Text('Valor', size=(8, 1)), sg.Input(key='saque', size=(12, 1), do_not_clear=False)],
              [sg.Button('Confirmar', button_color='green'), sg.Button('Voltar', button_color='blue'),
               sg.Button('Cancelar', button_color='red')],
              ]
    return sg.Window('Painel', layout=layout, finalize=True,  icon='logo.ico')

def janela_confirmada(): #janela final
    sg.theme('dark')
    layout = [
        [sg.Text('Operação realizada com sucesso!')],
        [sg.Button('Voltar', button_color='green', size=(12, 1)), sg.Button('Finalizar', button_color='red', size=(12, 1))]
    ]
    return sg.Window('Confirmado', layout=layout, finalize=True,  icon='logo.ico')

#definindo o estado das janelas
janela1, janela2, janela3, janela4, janela5 = janela_painel(), None, None, None, None
while True: #iniciando o loop da janela
    window, event, values = sg.read_all_windows() #lendo tudo que você realizar
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break
    if window == janela1: #importante1
        if event == 'Entrar':
            if values['user'] not in user_list:
                sg.popup('Os valores não batem!, Tente novamente, por favor!')
            if values['user'] in user_list:
                usuario = df.loc[user == values['user']]
                senha = int(usuario['pass'])
                user_escolhido=values['user']
                if int(values['pass']) != senha:
                    sg.popup('Os valores não batem!, Tente novamente, por favor!')
                if int(values['pass']) == senha:
                    sg.popup('Seus dados foram reconhecidos!')
                    janela1.hide()
                    janela2 = janela_banco()
                    window = janela2

    if window == janela2:
        if event == 'Voltar':
            janela2.hide()
            janela1.un_hide()
        if event == 'Sacar':
            janela2.hide()
            janela3 = janela_saque()
            window = janela3
        if event=='Depositar':
            janela2.hide()
            janela4 = janela_deposito()
            window = janela4

    if window == janela3:
        if event == 'Voltar':
            janela3.hide()
            janela2.un_hide()
        if event == 'Confirmar':
            usuario = df.loc[user == user_escolhido]
            credit = int(usuario['credit'])
            if int(values['saque']) > credit:
                sg.popup(f'Você não tem essa renda!, você só tem {credit} R$.')
            if int(values['saque']) <= credit: #importante2
                m = int(values['saque'])
                usuario = df.loc[user == user_escolhido]
                credit = int(usuario['credit'])
                new_credit = usuario['credit'].replace(credit, credit - m)
                df.loc[df['users']==user_escolhido, 'credit'] = new_credit
                df.to_excel('dados.xlsx')
                sg.popup(f'Você acabou de sacar {m} R$!\n'
                         f'Seu valor restante é de {int(new_credit)} R$!')
                janela3.hide()
                janela5=janela_confirmada()
                window=janela5

    if window == janela4:
        if event == 'Voltar':
            janela4.hide()
            janela2.un_hide()
        if event == 'Confirmar': #importante3
            m = int(values['deposito'])
            usuario = df.loc[user == user_escolhido]
            credit = int(usuario['credit'])
            new_credit=usuario['credit'].replace(credit,credit+m)
            df.loc[df['users'] == user_escolhido, 'credit'] = new_credit
            df.to_excel('dados.xlsx')
            sg.popup(f'Você acabou de depositar {m} R$!\n'
                     f'Seu valor agora é de {int(new_credit)} R$!')
            janela4.hide()
            janela5=janela_confirmada()
            window=janela5

    if window == janela5:
        if event =='Finalizar':
            break
        if event == 'Voltar':
            janela5.hide()
            janela2.un_hide()