import subprocess
import csv

def nslookup(domain):
    """Executa o nslookup para um domínio e retorna o status e a saída do comando"""
    try:
        # Executa o comando nslookup simples para o domínio
        result = subprocess.run(
            ['nslookup', domain],
            capture_output=True, text=True, check=True
        )
        
        # Se o nslookup for bem-sucedido, retornamos a saída completa
        return 'Sucesso', result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Em caso de erro, retornamos a mensagem de erro
        return 'Erro', e.stdout.strip() + "\n" + e.stderr.strip()

def validate_domains(domains):
    """Valida uma lista de domínios e gera um arquivo CSV com os resultados"""
    results = []

    for domain in domains:
        print(f"Validando domínio: {domain}")
        status, output = nslookup(domain)
        # Organiza os resultados em colunas
        results.append([domain, status, output])

    # Gera o arquivo CSV com os resultados
    with open('domain_nslookup_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Domain', 'Status', 'Output'])  # Cabeçalhos das colunas
        writer.writerows(results)  # Dados dos domínios

    print("Arquivo CSV gerado com sucesso: domain_nslookup_results.csv")

if __name__ == "__main__":
    # Lista de domínios fornecida por você
    domains = [
        'google.com.br', 'g1.globo.com', 'uol.com.br',
        'terra.com.br', 'microsoft.com', 'amazon.com.br', 'sbt.com.br',
        'estadao.com.br'
    ]
    
    # Valida os domínios e gera o CSV
    validate_domains(domains)
