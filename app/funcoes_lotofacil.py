def lotofacil(BeautifulSoup, get, URL):
    """
    """
    colunas = [
        "CONC","DATA","DEZ01","DEZ02","DEZ03","DEZ04","DEZ05","DEZ06","DEZ07","DEZ08","DEZ09","DEZ10","DEZ11","DEZ12","DEZ13","DEZ14","DEZ15"
    ]
    resultado = list()
    
    page = get(URL)
    #
    soup = BeautifulSoup(page.content, 'html.parser')
    #
    texto = soup.find("h1").text
    
    # concurso
    resultado.append(texto.split()[-3])
    
    # data
    resultado.append(texto.split()[-1])
    #
    dezenas = soup.find_all("span", class_="circle")
    for tag in range(len(dezenas[:15])):
        resultado.append(dezenas[tag].text)
            
    return dict(zip(colunas, resultado))
    
def lotofacil_by_conc(BeautifulSoup, get, URL, conc):
    """
    """
    colunas = [
        "CONC","DATA","DEZ01","DEZ02","DEZ03","DEZ04","DEZ05","DEZ06","DEZ07","DEZ08","DEZ09","DEZ10","DEZ11","DEZ12","DEZ13","DEZ14","DEZ15"
    ]
    resultado = list()
    
    page = get(URL+"?concurso={}".format(conc))
    #
    soup = BeautifulSoup(page.content, 'html.parser')
    
    if not soup.find("div", class_="res-acu"):
        #
        texto = soup.find("h1").text
        
        # concurso
        resultado.append(texto.split()[-3])
        
        # data
        resultado.append(texto.split()[-1])
        #
        dezenas = soup.find_all("span", class_="circle")
        for tag in range(len(dezenas[:15])):
            resultado.append(dezenas[tag].text)
                
        return dict(zip(colunas, resultado))
        
    else:
        return "erro"


if __name__ == "__main__":
    main()
