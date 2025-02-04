# Importando as bibliotecas necessárias
from azure.identity import AzureCliCredential
from azure.mgmt.dns import DnsManagementClient
import os

# Definir a assinatura do Azure
subscription_id = 'ID-DA-ASSINATURA-Azure'  #Coloque aqui sua assinatura do azure

# Obter credenciais via Azure CLI
credential = AzureCliCredential()
# Importando as bibliotecas
from azure.identity import AzureCliCredential
from azure.mgmt.dns import DnsManagementClient
import os

# Definir a assinatura do Azure
subscription_id = 'ID-DA-ASSINATURA-Azure' #Coloque aqui sua assinatura do azure  

# Usar Azure CLI para autenticação
credential = AzureCliCredential()

# Criar o cliente de gerenciamento DNS
dns_client = DnsManagementClient(credential, subscription_id)

# Obter todas as zonas DNS no grupo de recursos
resource_group_name = 'nome-do-grupo-de-recursos'  # Substitua pelo nome do seu grupo de recursos
zones = dns_client.zones.list_by_resource_group(resource_group_name)

# Gerar o conteúdo para o terraform.tfvars
domains_and_zones = []
for zone in zones:
    zone_name = zone.name
    zone_id = zone.id
    
    # A zona DNS no Azure está associada com a raiz do domínio
    # Aqui estamos assumindo que o nome da zona DNS é o domínio.
    domains_and_zones.append({
        "domain_name": zone_name,
        "dns_zone_id": zone_id
    })

# Caminho completo para o arquivo terraform.tfvars
output_file_path = r'C:\temp\terraform.tfvars'

# Verifique se o diretório C:\temp existe, se não, crie-o
if not os.path.exists(os.path.dirname(output_file_path)):
    os.makedirs(os.path.dirname(output_file_path))

# Escrever os dados no arquivo terraform.tfvars
with open(output_file_path, 'w') as f:
    f.write('domains_and_zones = [\n')
    for entry in domains_and_zones:
        f.write(f'  {{\n    domain_name = "{entry["domain_name"]}"\n    dns_zone_id = "{entry["dns_zone_id"]}"\n  }},\n')
    f.write(']\n')

print(f"Arquivo terraform.tfvars gerado com sucesso em {output_file_path}!")

# Criar o cliente de gerenciamento DNS
dns_client = DnsManagementClient(credential, subscription_id)

# Obter todas as zonas DNS no grupo de recursos (ou em toda a assinatura)
resource_group_name = 'NOME DO RG AQUI'  # Substitua pelo nome do seu grupo de recursos, se necessário
zones = dns_client.zones.list_by_resource_group(resource_group_name)

# Gerar o conteúdo para o terraform.tfvars
domains_and_zones = []
for zone in zones:
    zone_name = zone.name
    zone_id = zone.id
    
    # A zona DNS no Azure está associada com a raiz do domínio
    # Aqui estamos assumindo que o nome da zona DNS é o domínio.
    domains_and_zones.append({
        "domain_name": zone_name,
        "dns_zone_id": zone_id
    })

# Caminho completo para o arquivo terraform.tfvars
output_file_path = r'C:\temp\terraform.tfvars'

# Verifique se o diretório C:\temp existe, se não, crie-o
if not os.path.exists(os.path.dirname(output_file_path)):
    os.makedirs(os.path.dirname(output_file_path))

# Escrever os dados no arquivo terraform.tfvars
with open(output_file_path, 'w') as f:
    f.write('domains_and_zones = [\n')
    for entry in domains_and_zones:
        f.write(f'  {{\n    domain_name = "{entry["domain_name"]}"\n    dns_zone_id = "{entry["dns_zone_id"]}"\n  }},\n')
    f.write(']\n')

print(f"Arquivo terraform.tfvars gerado com sucesso em {output_file_path}!")
