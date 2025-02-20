import os
import pandas as pd
import whois
import tqdm
import requests
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.dns import DnsManagementClient
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Lista de Assinaturas do Azure
SUBSCRIPTION_IDS = {
    "ID-DA-SUA-ASSINATURA": "NOME-DA-SUA-ASSINATURA",
    "ID-DA-SUA-ASSINATURA": "NOME-DA-SUA-ASSINATURA",
    "ID-DA-SUA-ASSINATURA": "NOME-DA-SUA-ASSINATURA",
    "ID-DA-SUA-ASSINATURA": "NOME-DA-SUA-ASSINATURA"
     }

credential = DefaultAzureCredential()

# Função para buscar zonas DNS do Azure
def get_dns_zones(subscription_id):
    dns_client = DnsManagementClient(credential, subscription_id)
    zones = dns_client.zones.list()
    return [(subscription_id, zone.name) for zone in zones]

# Função para obter informações WHOIS + Registro.br
def get_whois_info(domain):
    try:
        w = whois.whois(domain)

        # Converter status para string se for lista
        status = (
            ', '.join(w.status) if isinstance(w.status, list) else 
            w.status if isinstance(w.status, str) else 
            "Desconhecido"
        )

        # Converter a data de expiração para string
        expiration_date = (
            w.expiration_date.strftime("%Y-%m-%d") if isinstance(w.expiration_date, datetime) else 
            w.expiration_date[0].strftime("%Y-%m-%d") if isinstance(w.expiration_date, list) and isinstance(w.expiration_date[0], datetime) else 
            str(w.expiration_date) if w.expiration_date else 
            "Desconhecido"
        )

        # Capturar os Name Servers e formatá-los corretamente
        name_servers = (
            ', '.join(w.name_servers) if isinstance(w.name_servers, list) else 
            w.name_servers if isinstance(w.name_servers, str) else 
            "Desconhecido"
        )

        # 🔹 Se for domínio .br e os NS forem "Desconhecido", buscar no Registro.br
        if domain.endswith(".br") and name_servers == "Desconhecido":
            registrobr_ns = get_registrobr_ns(domain)
            if registrobr_ns:
                name_servers = registrobr_ns

        return {
            "Registrar": w.registrar if w.registrar else "Desconhecido",
            "Status": status,
            "Data de Expiração": expiration_date,
            "Name Servers": name_servers
        }
    except Exception as e:
        return {
            "Registrar": "Erro",
            "Status": str(e),
            "Data de Expiração": "Desconhecido",
            "Name Servers": "Desconhecido"
        }

# Função para buscar NS no Registro.br
def get_registrobr_ns(domain):
    url = f"https://registro.br/cgi-bin/nicbr/whois?qr={domain}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            lines = response.text.split("\n")
            ns_list = [line.split(":")[1].strip() for line in lines if "nserver:" in line]
            return ', '.join(ns_list) if ns_list else None
    except Exception:
        return None
    return None

# Coleta de dados
data = []
for sub_id, sub_name in SUBSCRIPTION_IDS.items():
    domains = get_dns_zones(sub_id)
    for sub_id, domain in tqdm.tqdm(domains, desc=f"Processando domínios da assinatura {sub_name}"):
        whois_info = get_whois_info(domain)
        data.append({
            "Assinatura": sub_name,  # Nome da assinatura no lugar do ID
            "Dominio": domain,
            "Registrar": whois_info["Registrar"],
            "Status": whois_info["Status"],
            "Data de Expiração": whois_info["Data de Expiração"],
            "Name Servers": whois_info["Name Servers"]
        })

# Criar diretório e salvar CSV
os.makedirs("C:\\temp", exist_ok=True)
data_atual = datetime.now().strftime("%Y-%m-%d")
arquivo_csv = f"C:\\temp\\dns_whois_report_{data_atual}.csv"
df = pd.DataFrame(data)
df.to_csv(arquivo_csv, index=False)

# Criar o app Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Relatório de DNS e WHOIS"),
    
    # Filtro por Assinatura
    dcc.Dropdown(
        id="filtro-assinatura",
        options=[{"label": nome, "value": nome} for nome in SUBSCRIPTION_IDS.values()],
        placeholder="Selecione uma assinatura",
        multi=True,
    ),
    
    # Tabela de dados
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_table={"overflowX": "auto"},
        filter_action="native",
        sort_action="native",
        page_size=10
    )
])

# Callback para atualizar a tabela com base no filtro
@app.callback(
    Output("table", "data"),
    [Input("filtro-assinatura", "value")]
)
def atualizar_tabela(filtro):
    if not filtro:
        return df.to_dict("records")
    df_filtrado = df[df["Assinatura"].isin(filtro)]
    return df_filtrado.to_dict("records")

# Rodar o servidor Dash
if __name__ == "__main__":
    app.run_server(debug=True)
