import pygame as pyg
import os

pyg.font.init()
font1 = 'Karantina-Regular.ttf'


# BOTÕES_____________________________________________________________________:
class Button(pyg.sprite.Sprite):
    def __init__(self, screen, name, font_size, x, y, style):
        pyg.sprite.Sprite.__init__(self)
        self.font_size = font_size
        self.font = pyg.font.Font(os.path.join('data', font1), self.font_size)
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.style = style

        # LOAD DOS ARQUIVOS__________________________________________________:
        self.imagens = []
        if self.style == 1:
            self.imagens.append(pyg.image.load(os.path.join('images', 'button.png')).convert())
            self.imagens.append(pyg.image.load(os.path.join('images', 'button_pressed.png')).convert())

        elif self.style == 2:
            self.imagens.append(
                pyg.transform.scale(pyg.image.load(os.path.join('images', 'menu.png')).convert(), (180, 64)))

        # VARIÁVEIS DE ANIMAÇÃO______________________________________________:
        self.count = 0
        self.pressed = False
        self.start_count = False
        self.resp = False

        # CRIAÇÃO DE SPRITE__________________________________________________:

        self.image = self.imagens[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # TEXTO _____________________________________________________________:
        self.text = self.font.render(self.name, True, (210, 210, 210))
        self.text_rect = self.text.get_rect()
        self.text_x = self.x - self.text_rect.width / 2
        self.text_y = self.y - self.text_rect.height / 2

    # ANIMAÇÃO_______________________________________________________________:
    def update(self):
        self.resp = False

        if self.pressed:
            self.start_count = True
            self.pressed = False

        # GARANTE QUE O SPRITE 2 DO BOTÃO NÃO PASSE MUITO RÁPIDO_______________:
        if self.start_count:
            self.image = self.imagens[1]
            if self.count >= 1:
                self.count = 0
                self.start_count = False
                self.resp = True
                print(f'Button {self.name} pressed')

            self.image.set_colorkey((0, 0, 0))
            self.count += 0.25

        else:
            self.image = self.imagens[0]
            self.image.set_colorkey((0, 0, 0))

        return self.resp

    # RENDER DO TEXTO________________________________________________________:
    def draw_txt(self):
        self.screen.blit(self.text, (self.text_x, self.text_y))


# GAME MESMO_________________________________________________________________:
class Fase:
    def __init__(self, caso, time, din, problema, ask, screen, group):
        self.caso = caso
        self.time = time
        self.din = din
        self.problema = problema
        self.screen = screen
        self.ask = ask
        self.testes = []
        self.group = group

        # Tela_______________________________________________________________:
        self.din_avaliable = Button(self.screen, f'Fundos: {self.din}', 25, 1150, 50, 1)
        self.time_till = Button(self.screen, f'Tempo: {self.time}', 25, 1150, 70, 1)
        self.problem = Button(self.screen, 'Problema', 25, 1150, 150, 2)
        self.asks = Button(self.screen, 'Pergunta', 25, 1150, 230, 2)
        self.infos = Info(self.screen)
        self.do = Button(self.screen, 'Realizar análise', 25, 720, 600, 2)

        # PRIMEIRA LINHA DOS TESTES____________________________________________________________________________________:
        self.teste1 = Testes(self.screen, 'História natural', 200, 100, 2, 3,
                             f'inf: Fisionomia do bicho, tamanho médio, estilo de vida, etc.',
                             'Mamífero de pequeno porte (média de 4kg), se alimenta de pequenas frutas e alguns fungos',
                             self)
        self.teste2 = Testes(self.screen, 'Dados públicos do gov', 200, 180, 1, 2,
                             f'inf: Qualquer tipo de dado público sobre o animal',
                             'Alta taxa de morte desse animal por atropelamentos nessa região',
                             self)
        self.teste3 = Testes(self.screen, 'Análise geográfica', 200, 260, 1, 2,
                             f'inf: Análise geográfica da área, distribuição de habitáts, urbanismo, etc',
                             'Pequenos fragmentos de mata fechada divididos por área urbana comum (casas, ruas, etc.)',
                             self)
        self.teste4 = Testes(self.screen, 'Taxa de cruzamento', 200, 340, 1, 2,
                             f'inf: Avaliação da quantidade média de cruzamentos realizados por indivíduos que passaram '
                             'por lutas, vencedores e derrotados',
                             '[taxa dos vencedores é consideravelmente maior]',
                             self)
        self.teste5 = Testes(self.screen, 'Análise de tamanho', 200, 420, 1, 2,
                             f'inf: Coleta de indivíduos (vencedores e derrotados) para obtenção de dados de tamanho '
                             'corporal e tamanho das garras',
                             '[tamanho das garras em média menor dos derrotados] * [tamanho do corpo de vencedores é '
                             'consideravelmente maior]',
                             self)
        self.teste6 = Testes(self.screen, 'Expect. de vida padrão', 200, 500, 1, 2,
                             f'inf: Averígua a expectativa de vida padrão da espécie (em média)',
                             'A expectativa de vida média dessa espécie é 3 anos',
                             self)
        self.teste7 = Testes(self.screen, 'Expect. de vida derrot', 200, 580, 1, 2,
                             f'inf: Observação continuada para avaliação da expectativa de vida média de derrotados',
                             '1 ano e meio',
                             self)

        # SEGUNDA LINHA DOS TESTES_____________________________________________________________________________________:
        self.teste8 = Testes(self.screen, 'Observação de luta', 400, 100, 1, 2,
                             f'inf: Observação de lutas entre indivíduos. * Obtem dados de como é a luta.',
                             'Lutas se assemelham a judo, sumo sla fodac * é no jogo de corpo',
                             self)
        self.teste9 = Testes(self.screen, 'Número de filhotes', 400, 180, 1, 2,
                             f'inf: O Ratinho realiza testes de parternidade com os indivíduos jovens para descobrir'
                             'quantos filhotes tiveram os vencedores e os derrotados',
                             '[o número de filhotes é estastisticamente igual para ambos]',
                             self)
        self.teste10 = Testes(self.screen, 'Demanda de alimento', 400, 260, 1, 2,
                              f'inf: Necessidade de alimento (em kg/dia) que cada indivíduo precisa',
                              '0,2kg/dia para cada indivíduo adulto',
                              self)
        self.teste11 = Testes(self.screen, 'Dados populacionais', 400, 340, 1, 2,
                              f'inf: Contagem de quantos indivíduos de cada sexo e faixa etária existem em cada área * '
                              ' * * "Análise geográfica" é um requerimento para esta análise.',
                              '1 macho adulto * '
                              '3 fêmeas adultas * '
                              '6 filhotes * '
                              '(em média)',
                              self)
        self.teste12 = Testes(self.screen, 'Quantidade de alimento', 400, 420, 2, 3,
                              f'inf: Coleta de dados para estimar a quantidade de alimento disponível presente em uma '
                              'área * '
                              ' * * "Análise geográfica" é um requerimento para esta análise.',
                              '2,5kg/dia de alimento disponível em média',
                              self)
        self.teste13 = Testes(self.screen, 'Quantidade de ferimentos', 400, 500, 1, 2,
                              f'inf: Avaliação da gravidade dos ferimentos de cada indivíduo após a luta',
                              '[diferença não significativa]',
                              self)

        self.group.add(self.problem, self.infos, self.asks, self.teste1, self.teste2, self.teste3, self.teste4,
                       self.teste5, self.teste6, self.teste7, self.teste8, self.teste9, self.teste10, self.teste11,
                       self.teste12, self.teste13)
        self.testes.append(self.teste1)
        self.testes.append(self.teste2)
        self.testes.append(self.teste3)
        self.testes.append(self.teste4)
        self.testes.append(self.teste5)
        self.testes.append(self.teste6)
        self.testes.append(self.teste7)
        self.testes.append(self.teste8)
        self.testes.append(self.teste9)
        self.testes.append(self.teste10)
        self.testes.append(self.teste11)
        self.testes.append(self.teste12)
        self.testes.append(self.teste13)

    # Desenha os recursos na tela____________________________________________:
    def resources_update(self):
        self.din_avaliable.text = self.din_avaliable.font.render(f'Fundos: {str(self.din)}', True, (210, 210, 210))
        self.time_till.text = self.time_till.font.render(f'Tempo: {str(self.time)}', True, (210, 210, 210))
        #  meio gambiarra usar isso acima com o fill, eu acho
        self.din_avaliable.draw_txt()
        self.time_till.draw_txt()

        for teste in self.testes:
            teste.draw_txt()

    def is_opened(self, is_, opened):
        if is_:
            for teste in self.testes:
                if not teste == opened:
                    teste.opened = False

                else:
                    teste.opened = True


# PROBLEMA___________________________________________________________________:
class Info(pyg.sprite.Sprite):
    def __init__(self, screen):
        pyg.sprite.Sprite.__init__(self)
        self.x = 800
        self.y = 400
        self.texto = str
        self.open = True
        self.screen = screen
        self.image = pyg.transform.scale(
            pyg.image.load(os.path.join('images', 'notes_open.png')).convert(), (460, 590))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        #  self.font = pyg.font.SysFont('Times New Roman', 20)
        self.font = pyg.font.Font(os.path.join('data', font1), 25)

    # render do texto
    def txt(self, texto):
        self.texto = texto
        if self.open:
            words = [word.split(' ') for word in self.texto.splitlines()]  # 2D array where each row is a list of words.
            space = self.font.size(' ')[0]  # The width of a space.
            w, h = self.image.get_size()
            max_width, max_height = self.x + w / 2 - 43, self.y + h - 40
            pos = self.x - w / 2 + 43, self.y - h / 2 + 40
            x, y = pos[0], pos[1]
            # print(texto)
            for line in words:
                for word in line:
                    if word == '*':
                        x = pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    else:
                        word_surface = self.font.render(word, True, (0, 0, 0))
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = pos[0]  # Reset the x.
                            y += word_height  # Start on new row.
                        self.screen.blit(word_surface, (x, y))
                        x += word_width + space
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.


class Testes(Button):
    def __init__(self, screen, name, x, y, time_cost, money_cost, inf1, inf2, fase):
        Button.__init__(self, screen, name, 25, x, y, 1)
        self.time_cost = time_cost
        self.money_cost = money_cost
        self.inf1 = inf1
        self.inf2 = inf2
        self.fase = fase
        self.current_txt = self.inf1 + f' * * * Custo: R$ {self.money_cost},00' \
                                       f' * Tempo necessário: {self.time_cost} semanas'
        self.feito = False
        self.opened = False

    def done(self):
        if not self.feito:
            self.fase.time -= self.time_cost
            self.fase.din -= self.money_cost
            self.feito = True
            self.current_txt = self.inf2


class Notification(Button):
    def __init__(self, screen, name, x, y, group, botoes):
        Button.__init__(self, screen, name, 25, x, y, 2)
        self.gamma = 0
        self.i = 225
        self.group = group
        self.botoes = botoes

    def gamma_lowing(self):
        self.i -= 1
        self.image.set_alpha(self.i)
        self.text.set_alpha(self.i)
        #  print(self.i, 1)

        if self.i == 0:
            self.group.remove(self)
            self.botoes.remove(self)
