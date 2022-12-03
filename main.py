import AFD
import xml.etree.ElementTree as et
import pygame

pygame.init()
window = pygame.display.set_mode((1200, 673))
pygame.display.set_caption("CupHeadFA")

background = pygame.image.load('data/CupHead_backgrounds_03.jpg')
intro = pygame.image.load('data/intro.png')
duck = pygame.image.load('data/duck.png')

Aim1 = pygame.image.load('data/Aim/01.png')
Aim2 = pygame.image.load('data/Aim/02.png')
Aim3 = pygame.image.load('data/Aim/03.png')
Aim4 = pygame.image.load('data/Aim/04.png')
Aim5 = pygame.image.load('data/Aim/05.png')

RunR1 = pygame.image.load('data/RunR/01.png')
RunR2 = pygame.image.load('data/RunR/02.png')
RunR3 = pygame.image.load('data/RunR/03.png')
RunR4 = pygame.image.load('data/RunR/04.png')
RunR5 = pygame.image.load('data/RunR/05.png')

RunL1 = pygame.image.load('data/RunR/01L.png')
RunL2 = pygame.image.load('data/RunR/02L.png')
RunL3 = pygame.image.load('data/RunR/03L.png')
RunL4 = pygame.image.load('data/RunR/04L.png')
RunL5 = pygame.image.load('data/RunR/05L.png')

JumpR1 = pygame.image.load('data/Jump/cuphead_jump_0001.png')
JumpR2 = pygame.image.load('data/Jump/cuphead_jump_0002.png')
JumpR3 = pygame.image.load('data/Jump/cuphead_jump_0003.png')
JumpR4 = pygame.image.load('data/Jump/cuphead_jump_0004.png')
JumpR5 = pygame.image.load('data/Jump/cuphead_jump_0005.png')
JumpR6 = pygame.image.load('data/Jump/cuphead_jump_0006.png')
JumpR7 = pygame.image.load('data/Jump/cuphead_jump_0007.png')
JumpR8 = pygame.image.load('data/Jump/cuphead_jump_0008.png')

# Music
pygame.mixer.music.load('awesomeness.wav')
pygame.mixer.music.play(-1)

"""
" Função responsável por criar o autômato.
" @:param None.
" @:return retorna o autômato criado.
"""


def setWay():
    way = "AutomatoCUP.jff"
    content = et.parse(way)
    root = content.getroot()
    afd = AFD.AutomatoFD('usrlad')
    # desmonta a árvore e monta o AFD.
    for child in root.findall('automaton'):
        for subchild in child.findall('state'):
            stateFinal, stateInitial = False, False
            if subchild.find('initial') is None:
                pass
            else:
                stateInitial = True
            if subchild.find('final') is None:
                pass
            else:
                stateFinal = True
            args = subchild.attrib
            afd.criarEstado(args['id'], stateInitial, stateFinal)
        for subchild in child.findall('transition'):
            firstState = subchild.find('from').text
            secondState = subchild.find('to').text
            letter = subchild.find('read').text
            afd.criarTransicao(firstState, secondState, letter)
    afd.limpaAFD()
    return afd


"""
" Função responsável por atualizar a imagem na tela.
" @:param Vetor de imagens, posição X, posição Y e um contador para a próxima imagem do vetor.
" @:return None.
"""


def action(vector, x, y, posImage):
    image = vector[posImage]
    window.blit(image, (x, y))


"""
" Função responsável por fazer a manipulação de todo o programa e funções.
" @:param None
" @:return None.
"""


def main():
    """Criação das coordenadas do personagem."""
    x = 50
    y = 300
    speed = 50

    """Criação dos elementos para a função de pular."""
    isjump = False
    v = 5
    m = 1

    """Ciração da variável para axuliar na manipulção dos vetores."""
    configTime = 1

    """Criação dos vetores com as imagens/sprites."""
    listAim = [Aim1, Aim2, Aim3, Aim4, Aim5]
    posImage6 = 0
    listImage2 = [RunR1, RunR2, RunR3, RunR4, RunR5]
    posImageRR = 0
    listImage3 = [RunL1, RunL2, RunL3, RunL4, RunL5]
    posImageRL = 0
    listImage4 = [JumpR1, JumpR2, JumpR3, JumpR4, JumpR5, JumpR6, JumpR7, JumpR8]
    posImageJR = 0

    window_open = True

    """Criação do autômato."""
    afd1 = setWay()
    print(afd1)

    """Inicialização do loop que controla a Janela."""
    while window_open:
        time = int(pygame.time.get_ticks() / 1000)
        # pygame.mixer.music.stop()
        """Variável que representará o estado do autômato."""
        state = 0
        pygame.time.delay(50)
        for event in pygame.event.get():
            commands = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                window_open = False

        """Etapa para realizar o pulo do personagem."""
        if isjump == False:
            if commands[pygame.K_SPACE] and y >= 50:
                isjump = True
        if isjump:
            F = 3 * ((1 / 2) * m * (v ** 2))
            y -= F
            v -= 1
            if v < 0:
                m = -1
            if v == -6:
                isjump = False
                v = 5
                m = 1

        if commands[pygame.K_SPACE]:
            if configTime < time:
                state = 1
                posImageJR += 1
                configTime += 1
                if posImageJR > len(listImage4) - 1:
                    posImageJR = 0
                    configTime = 1

        """Etapa para realizar o down do personagem."""
        if commands[pygame.K_DOWN] and y <= 300:
            state = 4
        """Etapa para fazer o personagem correr para a direita."""
        if commands[pygame.K_RIGHT] and x <= 1050:
            if configTime < time:
                posImageRR += 1
                configTime += 1
                if posImageRR > len(listImage2) - 1:
                    posImageRR = 0
                    configTime = 1
            state = 5
            x += speed
        """Etapa para fazer o personagem correr para a esquerda."""
        if commands[pygame.K_LEFT] and x >= 50:
            if configTime < time:
                posImageRL += 1
                configTime += 1
                if posImageRL > len(listImage3) - 1:
                    posImageRL = 0
                    configTime = 1
            state = 6
            x -= speed
        """Etapa para fazer o personagem mirar."""
        if commands[pygame.K_CAPSLOCK] and y == 300:
            if configTime < time:
                posImage6 += 1
                configTime += 1
                if posImage6 > len(listAim) - 1:
                    posImage6 = 0
                    configTime = 1
            state = 3

        """Imprime o plano de fundo."""
        window.blit(background, (0, 0))

        """Define a ação do personagem de acordo com o estado (no autômato)."""
        if state == 0:
            window.blit(intro, (x, y))
        elif isjump:  # Equivalente a estar no estado 1 (Pular/Pulando).
            action(listImage4, x, y, posImageJR)
        elif state == 3:
            action(listAim, x, y, posImage6)
        elif state == 4:
            window.blit(duck, (x, 400))
        elif state == 5:
            action(listImage2, x, y, posImageRR)
        elif state == 6:
            action(listImage3, x, y, posImageRL)
        """Atualiza a janela."""
        pygame.display.update()


"""Chamada da função main()."""
main()
"""Encerra o programa."""
pygame.quit()
