import requests
from bs4 import BeautifulSoup
import csv

# URL de busca no site Receiteria para receitas que usam leite condensado
search_url = 'https://www.receiteria.com.br/?s=leite+condensado+&post_type=receita'

# Definir um cabeçalho User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Enviar uma solicitação GET ao site com o cabeçalho definido
response = requests.get(search_url, headers=headers)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Parsear o conteúdo HTML da página de busca
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar os links das receitas na página de busca
    receita_links = soup.find_all('a', class_='entry-title-link', limit=100)
    
    # Preparar a lista para armazenar os dados das receitas
    receitas = []
    
    # Iterar sobre os links das receitas e extrair os dados desejados
    for link in receita_links:
        receita_url = link['href']
        
        # Enviar uma solicitação GET para cada URL de receita com o cabeçalho definido
        receita_response = requests.get(receita_url, headers=headers)
        
        if receita_response.status_code == 200:
            receita_soup = BeautifulSoup(receita_response.content, 'html.parser')
            
            # Extrair o título da receita
            titulo = receita_soup.find('h1', class_='title-video').get_text(strip=True)
            
            # Extrair os ingredientes
            ingredientes = receita_soup.find('div', class_='ingredients-card').get_text(separator=', ', strip=True)
            
            # Extrair o modo de preparo
            modo_preparo = receita_soup.find('div', class_='instructions-card').get_text(separator=' ', strip=True)
            
            # Adicionar os dados extraídos à lista de receitas
            receitas.append([titulo, ingredientes, modo_preparo])
            
            # Printar os dados coletados
            print(f'Título: {titulo}\nIngredientes: {ingredientes}\nModo de Preparo: {modo_preparo}\n')
    
    # Salvar os dados em um arquivo CSV
    with open('C://Users//pc//Desktop//cr_doces//receitas_leite_condensado.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Ingredientes', 'Modo de Preparo'])  # Cabeçalho do CSV
        writer.writerows(receitas)  # Escrever os dados
    
    print('Dados salvos em receitas_leite_condensado.csv')
else:
    print('Falha ao acessar o site:', response.status_code)
