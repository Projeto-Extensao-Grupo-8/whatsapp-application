import pywhatkit as kit
import mysql.connector as mysql
import streamlit as st

import time

st.set_page_config(page_title="Consultas", layout="centered")

st.markdown("""
    <style>
        .stApp {
            background-color: #F9FAFB !important;
        }
        .main {
            background-color: transparent !important;
        }
        .block-container {
            background-color: transparent !important;
        }

        .card {
            background-color: #FDE9EC;
            padding: 18px;
            border-radius: 14px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .nome {
            font-size: 18px;
            font-weight: 600;
            color: #E46A84;
        }

        .infos {
            font-size: 14px;
            color: #666;
        }

        .botao {
            background-color: #E46A84 !important;
            color: white !important;
            padding: 10px 20px !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .icone {
            color: #E46A84;
            font-size: 26px;
            margin-right: 10px;
        }
            
        .stButton>button {
            background-color: #E46A84;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
        }
            
        .stButton>button:hover {
            background-color: #d25573;
            color: white;
        }
            
        .status {
            width: 200px;
            justify-content: center;
            display: flex;
            background-color: #FFD8B5;
            color: #FF7A00;
            margin-left: 300px;
            padding: 10px;
            border-radius: 20px;
            border: solid #FF7A00 2px 
        }
            
        .status-ok {
            width: 100%;
            justify-content: center;
            display: flex;
            background-color: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 20px;
            border: solid #28a745 2px 
        }
            
        .stAlert.stAlert-success {
            background-color: #d4edda !important;  /* verde mais forte */
            color: #155724 !important;               /* texto branco */
        }
    </style>
""", unsafe_allow_html=True)

con = mysql.connect(
    host="localhost",
    user="pythonuser",
    password="SenhaForte123",
    database="flor_de_lotus",
    auth_plugin='mysql_native_password'
)

cursor = con.cursor()
cursor.execute("SELECT nome, telefone FROM usuario")
dados = cursor.fetchall()
colunas = [desc[0] for desc in cursor.description]

lista_dict = [dict(zip(colunas, linha)) for linha in dados]

def enviar_whatsapp(nome, telefone):
    numero = "+55" + str(telefone)
    msg = f"Consulta agendada com sucesso {nome}!!!"
    try:
        kit.sendwhatmsg_instantly(numero, msg)
        return True
    except:
        return False

st.markdown(
    "<h3 style='color:#E46A84;'>Próximos Agendamentos</h3>",
    unsafe_allow_html=True
)

st.markdown(f"""
    <div class="card">
        <div style="display:flex; align-items:center;">
            <span style='color=#E46A84;' class="icone">🌸</span>
            <div>
                <div class="nome">{lista_dict[-1]['nome']}</div>
                <div class="infos">Telefone: {lista_dict[-1]['telefone']} <br> Dia: 04/12 <br> Horário: 19:00 </div>
            </div>
            <div class='status'> Confirmação pendente </div>"
        </div>
    </div>
""", unsafe_allow_html=True)

ultimo = lista_dict[-1]
nome = ultimo['nome']
telefone = ultimo['telefone']

if "confirmado" not in st.session_state:
    st.session_state.confirmado = False

def confirmar():
    st.session_state.confirmado = True

if st.button("Confirmar Consulta", on_click=confirmar):
    st.markdown(f"""<span class="status-ok"> Consulta agendada com sucesso, redirecionando para o whatsapp... </span>""", unsafe_allow_html=True)
    time.sleep(3)
    enviar_whatsapp(nome, telefone)
