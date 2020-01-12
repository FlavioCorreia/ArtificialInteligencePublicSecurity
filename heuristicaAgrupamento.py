import pandas as pd

data = pd.read_excel (r'distanciaCarroCidades.xlsx')
df = pd.DataFrame(data)

cidades = list(df['Cidades'][:])
hsDist = {}
for i in range(len(cidades)):
    for j in range(len(cidades)):
        hsDist[cidades[i],cidades[j]] = df[cidades[i]][j]

#--------------------------------------------------------------------------------------------------PEGANDO COORDENADAS
cidades = ["Chaval","Barroquinha","Jijoca de Jericoacoara","Acaraú","Itarema","Marco","Morrinhos", "Tururu", "Massapê", "Tianguá","São Benedito", "Crateús", "Piquet Carneiro", "Sobral", "Forquilha", "Umirim", "Maranguape", "Pacatuba", "Caucaia", "Maracanaú", "Reriutaba", "Varjota", "Pacoti", "Guaiúba", "São Gonçalo do Amarante","Paracuru", "Fortaleza", "Aquiraz", "Eusébio", "Horizonte", "Pindoretama", "Pacajus", "Chorozinho", "Baturité", "Canindé", "Itatira", "Aracoiaba", "Aracati", "Ibaretama", "Jaguaruana", "Quixadá", "Morada Nova", "Tabuleiro do Norte", "Limoeiro do Norte", "Icapuí", "Saboeiro", "Iguatu", "Icó", "Juazeiro do Norte"]

f = open('coordenadas.txt', 'r') #TXT QUE CONTEM AS COORDENADAS DAS CIDADES
conteudo = f.readlines()
f.close()

coordenadas = {}; ind = 0
for linha in conteudo: #MAPEANDO CIDADE -> (Xi, Yi) EM UMA HASH
    cidade, coordenada = linha.split("=")
    coordenadas[cidades[ind]] = [int(i) for i in coordenada.split(',')]
    ind += 1

#--------------------------------------------------------------------------------------------------TELA
def melhorDistribuicao(centroides1, centroides2): #VER QUAL COMPOSICAO DOS CENTOIDES TEM MELHOR DISTRIBUICAO DE CIDADES
    media = sum(centroides1)/len(centroides1)
    erro1 = sum([(valor - media)**2 for valor in centroides1])
    erro2 = sum([(valor - media)**2 for valor in centroides2])
    if erro1 < erro2:
        return 1
    return 2

def dtEuc(x1,y1,x2,y2): #DISTANCIA EUCLIDIANA ENTRE DOIS PONTOS
    return ((x1-x2)**2 + (y1-y2)**2)**(1/2)

import pygame
from pygame.locals import *
from random import randint

pygame.init()
infoObject = pygame.display.Info() #PEGAR INFORMACOES P/ USAR NO TAMANHO DA TELA
gameDisplay = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), RESIZABLE) #CRIANDO JANELA
pygame.display.set_caption("TRABALHO DE SEGURANÇA PUBLICA") #TITULO JANELA
clock = pygame.time.Clock() #USADO NO FPS
ativo = False #NAO MOSTRO OS CENTROIDES INICIALMENTE  (BTN ESQ. DO MOUSE)
calculando = False #NAO FACO OS CENTROIDES CAMINHAREM (BTN DIR. DO MOUSE)
ligarCidades = False #NAO LIGAR AS CIDADES (APOS OS CENTROIDES OBTEREM SUAS CIDADES)
centroides = [] #COORDENADAS DOS CENTROIDES COMUNS
cidadeUnidade = {} # PASSA A CIDADE -> RETORNA A UNIDADE RESPONSAVEL
distCidades = [[], [], [], [], []] # CIDADES DE INDICE i PERTENCEM A UNIDADE i+1
printarOrdemCidades = False #IMPRIMIR NO CONSOLE A ORDEM DE ROTA DA UNIDADE i PELAS CIDADES DE SEU TRAJETO

for cidade in cidades:
    cidadeUnidade[cidade] = 0

while True:
    gameDisplay.fill((197,197,197))# TELA DE FUNDO
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #SE CLICOU NO X
            pygame.quit()
            quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: #CLICOU COM O MOUSE
            if event.button == 1: # BTN ESQ
                ligarCidades = False
                printarOrdemCidades = False
                centroides = [] # ELIMINO OS CENROIDES ANTIGOS
                for i in range(5): # ATIBUO ALEATORIAMENTE NO MAPA                    
                    centroides += [[randint(0,540), randint(0,690)]]
                    
                #centroides = [[80,80], [284,151], [382,200], [425,360], [123,230]] #ATRIBUIR CENTROIDES 0MANUALMENTE
                ativo = True # MOSTRAR OS CENTROIDES
                
            elif event.button == 3: # BTN DIR
                calculando = True # MANDO OS CENTROIDES CAMINHAREM
                for cidade in cidades: # INICIALMENTE DIGO QUE AS CIDADES NAO PERTENCEM A NENHUM CENTROIDE
                    cidadeUnidade[cidade] = 0 

    gameDisplay.blit( pygame.image.load("mapaCidades.png") , (300, 0)) #IMAGEM DE FUNDO
    for cidade in cidades:
        img = "nivelVertices/semClasse.png"
        if cidadeUnidade[cidade] != 0:
            img = "nivelVertices/unidade"+str(cidadeUnidade[cidade])+".png"
            
        gameDisplay.blit( pygame.image.load(img) , (coordenadas[cidade][0]+300-10, coordenadas[cidade][1]-7))

    if ativo: #PRINTAR OS CENTROIDES
        for i in range(5):
            gameDisplay.blit( pygame.image.load(str("nivelVertices/unidadeC"+str(1+i)+".png")) , (300+centroides[i][0], centroides[i][1]))

    if calculando: #LIGAR AS CIDADES AOS CENTROIDES
        for cidade in cidades:
            cidadeUnidade[cidade] = 1
            dMin = dtEuc(coordenadas[cidade][0], coordenadas[cidade][1], centroides[0][0], centroides[0][1])
            for i in range(1,5):
                dNova = dtEuc(coordenadas[cidade][0], coordenadas[cidade][1], centroides[i][0], centroides[i][1])
                if  dNova < dMin:
                    cidadeUnidade[cidade] = i+1
                    dMin = dNova

        c = [0,0,0,0,0] #PARA CONTAR QUANTAS CIDADES CADA CENTROIDE TEM
        centroidesN = [[0,0],[0,0],[0,0],[0,0],[0,0]]
        for cidade in cidades: #ADICIONO A DISTANCIA DE CADA CENTROIDE A CIDADE QUE PERTENCE A ELE
            c[cidadeUnidade[cidade]-1] +=1
            centroidesN[cidadeUnidade[cidade]-1][0] += coordenadas[cidade][0]
            centroidesN[cidadeUnidade[cidade]-1][1] += coordenadas[cidade][1]
            
        for i in range(len(c)): #DIVIDO A DISTANCIA TOTAL PELO NUMERO DE CIDADES PARA PEGAR O PONTO MEDIO
            if c[i] != 0:
                centroidesN[i][0] /= c[i]
                centroidesN[i][1] /= c[i]
            
        if centroidesN == centroides: #SE O CENTROIDE NAO SE DESLOCAR, ELE JÁ ENCONTROU SEU PONTO DE ESTABILIDADE
            calculando = False # PARO DE CALCULAR
            ligarCidades = True #INICIO A LIGACAO DAS CIDADES
            printarOrdemCidades = True
            distCidades = [[], [], [], [], []] #ZERO VALORES ANTIGOS
            for cidade in cidades: 
                distCidades[cidadeUnidade[cidade]-1] += [cidade]

            print("#######################################################################")
            for i in range(5):
                print("Unidade ",i+1,"|",distCidades[i])
            
        else: #SE NAO, ATUALIZO OS CENTROIDES E RECALCULO
            centroides = centroidesN.copy()

    if ligarCidades: #LIGO AS CIDADES COM O GULOSO DA CIDADE MAIS PROXIMA
        ativo = False #DESABILITO OS CENTROIDES
        cor = [(61,7,242), (237,28,36), (34,177,76), (0,162,232), (163,73,164)]
        for i in range(5):
            distCidadesAux = distCidades[i].copy()
            if printarOrdemCidades:
                print("----------------------Ordem da Unidade",i+1,"----------------------")
            while len(distCidadesAux) > 0:
                cidadeAtual = distCidadesAux.pop(0)
                idMenor = -10; menorValor = 99999999
                for j in range(len(distCidadesAux)): #OLHO QUAL A CIDADE MAIS PROXIMA
                    if hsDist[cidadeAtual,distCidadesAux[j]] < menorValor:
                        idMenor = j; menorValor = hsDist[cidadeAtual,distCidadesAux[j]]

                if idMenor != -10: #SE ESCOLHEU
                    if printarOrdemCidades:
                        print(cidadeAtual,"->",distCidadesAux[idMenor])
                    pygame.draw.line(gameDisplay, cor[i], [coordenadas[cidadeAtual][0]+300,coordenadas[cidadeAtual][1]], [coordenadas[distCidadesAux[idMenor]][0]+300, coordenadas[distCidadesAux[idMenor]][1]], 4)
                    cidadeAtual = distCidadesAux.pop(idMenor)
                    distCidadesAux = [cidadeAtual] + distCidadesAux
        printarOrdemCidades = False #SO IMPRIMO NO CONSOLE UMA VEZ, PARA N FICAR UM LOOP PRINTANDO A MESMA COISA
    pygame.display.update()
    clock.tick(5)

pygame.quit()
quit()





































                

