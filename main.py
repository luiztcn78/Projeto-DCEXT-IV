import requests
from bs4 import BeautifulSoup
import pyttsx3

def ler_pagina(url):
    try:
        # Baixando o conteúdo da página
        response = requests.get(url)
        response.raise_for_status()
        
        # extraindo texto da página
        soup = BeautifulSoup(response.text, 'html.parser')
        paragrafos = soup.find_all('p')
        
        texto = " ".join([p.get_text() for p in paragrafos if p.get_text()])
        return texto if texto else "Não foi possível encontrar conteúdo legível na página."
    except Exception as e:
        return f"Erro ao acessar a página: {e}"

def falar_texto(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Configuração de velocidade da fala
    engine.say(texto)
    engine.runAndWait()

if __name__ == "__main__":
    url = input("Digite a URL da página que deseja ouvir: ")
    conteudo = ler_pagina(url)
    print("\n--- Texto extraído ---\n")
    print(conteudo[:1000])  # mostra só os 1000 primeiros caracteres
    print("\n--- Fim do texto ---\n")
    
    print("Lendo em voz alta...")
    falar_texto(conteudo[:1000])

#TODO: botão de parar de ler 
#TODO: ajuste de volume