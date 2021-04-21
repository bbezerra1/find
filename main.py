import pygame as pyg
from adds import *

# INICIADORES PADRÕES..............................................:
pyg.init()
font_30 = pyg.font.Font(os.path.join('data', font1), 30)

# TELA_____________________________________________________________:
larg = 1280
alt = 720
screen = pyg.display.set_mode((larg, alt))
pyg.display.set_caption('Research_io')
clock = pyg.time.Clock()
screen.fill((40, 40, 40))


# MAIN MENU________________________________________________________:
def main_menu():
    menu_run = True

    # Cria o sprite group e os botões______________________________:
    all_main = pyg.sprite.Group()
    b1 = Button(screen, 'Jogar', 25, larg/2, 400, 1)
    print(b1.image)
    b2 = Button(screen, 'Opcoes', 25, larg/2, 500, 1)
    b3 = Button(screen, 'Sair', 25, larg/2, 600, 1)
    all_main.add(b1, b2, b3)

    # Desenhar apenas o texto desses______________________________:
    name = Button(screen, 'no lo se', 100, larg/2, 260, 1)
    version = Button(screen, 'Alpha v0.1', 15, 50, 710, 1)

    # MENU MAIN LOOP______________________________________________:
    while menu_run:
        clock.tick(60)
        click = False
        mx, my = pyg.mouse.get_pos()

        # GET DE EVENTOS__________________________________________:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

        if click:
            print(f'click {mx, my}')
            pass

        # CHECK DE COLISÂO DO MOUSE_______________________________:
        if click:
            if b1.rect.collidepoint((mx, my)):
                b1.pressed = True
            if b2.rect.collidepoint((mx, my)):
                b2.pressed = True
            if b3.rect.collidepoint((mx, my)):
                b3.pressed = True

        # AÇÃO DOS BOTÕES_________________________________________:
        if b1.update():
            menu_run = False
            screen.fill((40, 40, 40))
            game()

        if b2.update():
            pass
        if b3.update():
            menu_run = False

        # DESENHA OS BOTÕES_______________________________________:
        all_main.update()
        all_main.draw(screen)

        # DESENHA O TEXTO DOS BOTÕES______________________________:
        b1.draw_txt()
        b2.draw_txt()
        b3.draw_txt()
        name.draw_txt()
        version.draw_txt()

        # UPDATE DA TELA__________________________________________:
        pyg.display.update()
        pyg.display.flip()


# LOAD DA FASE____________________________________________________:
# atualmente totalmente desativado, uma vez que não é necessário com apenas um caso papaoY
def load_data(caso):
    data = open(os.path.join('data', f'{caso}.txt'), 'r')
    b = data.readlines()
    dados = []
    for line in b:
        dados.append(line.strip('\n'))

    # Transcreve os dados do arq em variáveis_____________________:
    tempo = int(dados[0])
    funding = int(dados[1])
    problema = dados[2]
    asks = dados[3]

    return tempo, funding, problema, asks


def do_off(load, botoes):
    load.group.remove(load.do)
    botoes.remove(load.do)


# GAME_WINDOW_____________________________________________________:
def game():
    game_run = True
    caso = 'agressividade'
    botoes = []
    # tempo, funding, problema, asks = load_data(caso)
    tempo = 64
    funding = 25000
    problema = "Segundo relatos de moradores de uma cidade do interior de São Paulo, os indivíduos de uma espécie " \
               "animal muito comum na região demonstram comportamento agressivo com frequência, brigando entre si. " \
               "Seu grupo de pesquisa resolveu investigar esse comportamento."
    asks = "Por que eles brigam? * " \
           "- Territorialismo * " \
           "- Disputa sexual * * " \
           "Como brigam? Qual fator influencia a briga? * " \
           "- Com garras, chifres, etc * " \
           "- Tamanho corporal * * " \
           "A briga gera ferimentos? Eles afetam a sobrevivência dos feridos? * " \
           "- A briga pode causar morte ou ferimentos graves * " \
           "- Os ferimentos não causam impacto na sobrevivência do indivíduo"
    hipoteses = ""
    premissas = ""
    previsoes = ""

    # Botões______________________________________________________:
    all_game_wind = pyg.sprite.RenderPlain()

    a = Notification(screen, 'Analise geo porra', 640, 100, all_game_wind, botoes)
    load = Fase(caso, tempo, funding, problema, asks, screen, all_game_wind)
    botoes.append(load.problem)
    botoes.append(load.asks)
    current_inf = ''
    do_on = False

    # MAIN LOOP___________________________________________________:
    while game_run:
        clock.tick(60)
        click = False
        mx, my = pyg.mouse.get_pos()

        # GET DE EVENTOS__________________________________________:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                game_run = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pyg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

        if click:
            if do_on:
                if load.do.rect.collidepoint((mx, my)):
                    for teste in load.testes:
                        if teste.opened:
                            # Para o teste que precisa da análise geográfica
                            if teste == load.teste11 or teste == load.teste12:
                                if load.teste3.feito and not teste.feito:
                                    if load.time - teste.time_cost >= 0 and load.din - teste.money_cost >= 0:
                                        teste.done()
                                        current_inf = teste.current_txt

                                        # tira o botão de fazer a análise
                                        do_off(load, botoes)
                                        do_on = False
                                    else:
                                        # cria a notificação dos recursos faltando
                                        all_game_wind.add(a)
                                        a.i = 225
                                        a.text = a.font.render('Recursos insuficientes', True, (210, 0, 0))
                                        a.text_rect = a.text.get_rect()
                                        a.text_x = a.x - a.text_rect.width / 2
                                        a.text_y = a.y - a.text_rect.height / 2

                                else:
                                    current_inf = (teste.current_txt + ' * * * * * * * * * '
                                                                       '"Análise geográfica" é necessária para esta '
                                                                       'análise!')
                                    all_game_wind.add(a)
                                    a.i = 225

                                    # tira o botão de fazer a análise
                                    do_off(load, botoes)
                                    do_on = False

                            # Testes normais
                            elif not teste.feito:
                                if load.time - teste.time_cost >= 0 and load.din - teste.money_cost >= 0:
                                    teste.done()
                                    current_inf = teste.current_txt
                                    do_off(load, botoes)
                                    do_on = False

                                else:
                                    # cria a notificação dos recursos faltando
                                    all_game_wind.add(a)
                                    a.i = 225
                                    a.text = a.font.render('Recursos insuficientes', True, (210, 0, 0))
                                    a.text_rect = a.text.get_rect()
                                    a.text_x = a.x - a.text_rect.width / 2
                                    a.text_y = a.y - a.text_rect.height / 2

            if load.problem.rect.collidepoint((mx, my)):
                current_inf = load.problema
                for teste in load.testes:
                    if teste.opened:
                        if load.do in all_game_wind:
                            do_off(load, botoes)
                            do_on = False

                        teste.opened = False

            if load.asks.rect.collidepoint((mx, my)):
                current_inf = load.ask
                for teste in load.testes:
                    if teste.opened:
                        if load.do in all_game_wind:
                            do_off(load, botoes)
                            do_on = False
                        teste.opened = False

            for teste in load.testes:
                if teste.rect.collidepoint((mx, my)):
                    teste.opened = True
                    if not teste.feito:
                        if not do_on:
                            load.group.add(load.do)
                            botoes.append(load.do)
                            do_on = True
                    elif teste.feito:
                        if do_on:
                            do_off(load, botoes)
                            do_on = False

                    load.is_opened(True, teste)
                    current_inf = teste.current_txt

        # UPDATE DA TELA__________________________________________:
        screen.fill((40, 40, 40))  # acho que é meio gambiarra usar esse fill para atualizar a tela

        if a in all_game_wind:
            if a not in botoes:
                botoes.append(a)
            a.gamma_lowing()
            # print(f'lowering the alpha...{a.i}')

        print(botoes)
        all_game_wind.update()
        all_game_wind.draw(screen)

        # text
        for botao in botoes:
            botao.update()
            botao.draw_txt()

        # recursos
        load.resources_update()
        load.infos.txt(current_inf)

        # final
        pyg.display.update()
        pyg.display.flip()


main_menu()
pyg.quit()

