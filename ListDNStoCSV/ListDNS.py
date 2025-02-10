from azure.identity import InteractiveBrowserCredential
from azure.mgmt.dns import DnsManagementClient
import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm  # Barra de progresso

# Configurações iniciais
subscription_id = "seu-subscription-id"  # Substitua pelo seu Subscription ID
resource_group = "XXXX"  # Substitua pelo nome do seu Resource Group

# Autenticação no Azure usando login interativo
credential = InteractiveBrowserCredential()
dns_client = DnsManagementClient(credential, subscription_id)

# Criar diretório para salvar o CSV
os.makedirs("C:\\temp", exist_ok=True)

# Nome do CSV com data e hora
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_filename = f"C:\\temp\\dns_hml_types_{timestamp}.csv"

# Obter todas as zonas de DNS no Resource Group
print("🔍 Buscando zonas de DNS...")
zones = list(dns_client.zones.list_by_resource_group(resource_group))

# Lista para armazenar os registros encontrados
filtered_records = []

# Lista cada zona com barra de progresso
print(f"🔍 Processando {len(zones)} zonas de DNS...")
for zone in tqdm(zones, desc="Processando Zonas", unit="zona"):
    # Obter todos os tipos de registros para a zona atual
    record_sets = dns_client.record_sets.list_by_dns_zone(resource_group, zone.name)

    for record in record_sets:
        # Filtrar registros cujo nome contém "hml"
        if "hml" in record.name.lower():
            # Determinar o tipo do registro
            record_type = record.type.split('/')[-1]  # Exemplo: 'Microsoft.Network/dnszones/A' -> 'A'

            # Capturar valores conforme o tipo de registro
            if record_type == "A":
                record_values = ", ".join([ip.ipv4_address for ip in record.a_records]) if record.a_records else "N/A"
            elif record_type == "CNAME":
                record_values = record.cname_record.cname if record.cname_record else "N/A"
            elif record_type == "TXT":
                record_values = ", ".join(["".join(txt.value) for txt in record.txt_records]) if record.txt_records else "N/A"
            elif record_type == "MX":
                record_values = ", ".join([f"{mx.preference} {mx.exchange}" for mx in record.mx_records]) if record.mx_records else "N/A"
            elif record_type == "NS":
                record_values = ", ".join([ns.nsdname for ns in record.ns_records]) if record.ns_records else "N/A"
            else:
                record_values = "N/A"

            # Adicionar ao array de registros
            filtered_records.append({
                "ZoneName": zone.name,
                "ResourceGroup": resource_group,
                "RecordType": record_type,
                "RecordName": record.name,
                "RecordValue": record_values,
                "GenerationTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            print(f"✅ Encontrado {record_type} HML na zona {zone.name}: {record_values}")

# Se encontrou registros, exporta para CSV
if filtered_records:
    df = pd.DataFrame(filtered_records)
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"\n📄 CSV gerado com sucesso: {csv_filename}")
else:
    print("\n⚠️ Nenhum registro contendo 'HML' foi encontrado.")

