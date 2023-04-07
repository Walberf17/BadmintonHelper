"""
This is a badminton points counter
"""
__version__ = "4.0.4"

import os
import random
from functools import partial

os.environ['KIVY_ORIENTATION'] = 'LandscapeLeft LandscapeRight'

# import kivy
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField
from kivy.animation import Animation
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable


# import other things
import datetime

PRAZO_MAXIMO = datetime.date(2023,3,18)

# Variables
TEAM_SIZE_HINT = [.5, .7]

class MyScreen(Screen):
    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(widget)


class TeamSets(StackLayout):
    def __init__(self, team_to_follow, team_number=2, *args, **kwargs):
        super().__init__(size_hint=[.3, .1], pos_hint={'center': [.5, .8]}, orientation='rl-tb', *args, **kwargs)
        self.team_to_follow = team_to_follow
        self.team_number = team_number
        self.image_file = os.path.join('.', 'images', 'volante.png')
        self.add_widget(
            MDLabel(text=str(self.team_number), size_hint=[1, 1], pos_hint={'center': [.5, .5]}, halign='center'))
        # self.bind(on_center_x=self.team_to_follow.setter('center_x'))

    def set_wins(self, all_pts):
        self.clear_widgets()
        if len(all_pts) > 1:
            for set in all_pts[:-1]:
                if set[-1] == (self.team_number + len(all_pts) % 2) % 2:
                    grid = MDGridLayout(cols=1, adaptive_size=True)
                    grid.add_widget(Image(source=self.image_file,
                                          pos_hint={'center': [.5, .5]}))
                    self.add_widget(grid)
        self.set_pos()

    def set_pos(self):
        pos_hint = self.team_to_follow.pos_hint
        x, y = pos_hint.get('center')
        self.pos_hint = {'center': [x, .85]}


class MainWindow(MDRelativeLayout):
    def __init__(self, app, **kwargs):
        # super().__init__(cols=2, size_hint=[1, 1], padding = [50,50,50,50], **kwargs)
        super().__init__(size_hint=[1, 1], pos_hint={'center': [.5, .5]}, **kwargs)
        self.app = app
        grid = MDGridLayout(cols=2, size_hint=[.9, .8], pos_hint={'center': [.5, .5]}, spacing=50)
        grid.add_widget(MDRectangleFlatButton(text='Simples', size_hint=[1, 1], on_release=partial(self.change_window,
                                                                                                   'single')))
        grid.add_widget(MDRectangleFlatButton(text='Duplas', size_hint=[1, 1], on_release=partial(self.change_window,
                                                                                                  'double')))
        self.add_widget(grid)

    def change_window(self, new_window, *args):
        self.app.sm.current = new_window


class TeamLabel(MDGridLayout):
    def __init__(self, team_name, initial_right=True, initial_top=True, **kwargs):
        self.initial_right = initial_right
        self.initial_top = initial_top

        if self.initial_right:
            x = .5 - .12
        else:
            x = .5 + .12

        if self.initial_top:
            y = .5 + .25
        else:
            y = .5 - .25

        super().__init__(cols=1, md_bg_color=[.7, .7, .7, 1], adaptive_size=True, size_hint=[.4, .2],
                         pos_hint={'center': [x, y]},
                         **kwargs)

        self.team_name_lbl = MDLabel(text=team_name, valign='center', halign='center', font_style='H5', max_lines=1,
                                     size_hint=[1, 1])
        self.add_widget(self.team_name_lbl)

    def change_pos(self, new_pos):
        anim = Animation(pos_hint={'center': new_pos}, duration=.1, t='in_out_cubic')
        anim.start(self)

    def change_label(self, new_name):
        self.team_name_lbl.text = new_name

    def get_name(self):
        return self.team_name_lbl.text

    def get_pos_hint(self):
        return self.pos

    def change_position(self, sets=1, even=True, past_half=False, single=True):
        x_dif = .1 + self.size_hint[0] / 2
        y_dif = .12

        if self.initial_right:
            x_dif *= -1
        if sets % 2 == 0:
            x_dif *= -1
            if single:
                y_dif *= -1

        if past_half:
            x_dif *= -1
            y_dif *= -1

        if self.initial_top:
            y_dif *= -1

        if even:
            y_dif *= -1

        x = .5
        y = .5 + y_dif
        self.change_pos([x, y])


class ScoreLabel(MDGridLayout):
    def __init__(self, right_side, **kwargs):
        self.size_hint_w = .2

        if right_side:
            pos_hint_x = 1-self.size_hint_w/2
        else:
            pos_hint_x = self.size_hint_w/2

        super().__init__(cols=1, size_hint=[.4, .2], md_bg_color=[0, 0, 0, 1], pos_hint={'center': [pos_hint_x, .5]}, **kwargs)
        self.score_lbl = MDLabel(text='0', halign='center', font_style='H2', max_lines=1, theme_text_color='Custom',
                                 text_color='white')
        self.add_widget(self.score_lbl)

    def change_position(self, right_side):
        if right_side:
            pos_hint_x = self.size_hint_w / 2
        else:
            pos_hint_x = 1 - self.size_hint_w/ 2
        pos_hint = {'center': [pos_hint_x, .5]}

        anim_lbl = Animation(pos_hint=pos_hint, duration=.1)
        anim_lbl.start(self)

    def change_label(self, new_name):
        self.score_lbl.text = str(new_name)

    def get_name(self):
        return self.score_lbl.text

    def get_pos_hint(self):
        return self.pos

    def change_color(self, color):
        self.score_lbl.text_color = color


class GameOver(MDRelativeLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(md_bg_color= [0,0,0,1],size_hint=[1, 1], pos_hint={'center': [.5, -.5]},adaptive_height=True, *args, **kwargs)
        self.lbl = MDLabel(theme_text_color='Custom', text_color=[1,1,1,1], font_style='H1', valign='center', halign='center', italic=True)
        self.random_text()
        self.add_widget(self.lbl)

    def move_up(self):
        anim = Animation(pos_hint={'center': [.5, .5]}, duration=.2)
        anim.start(self)

    def move_down(self):
        anim = Animation(pos_hint={'center': [.5, -.5]}, duration=.2)
        anim.start(self)

    def random_text(self):
        texts = [
            'Vitória!',
            'Terminou!',
            'This is Sparta!',
            'GG!',
            'Bom jogo!',
            'Decimou!',
            'Fim de Jogo!',
            'Game!',
            'K.O.!',
            'Qua Qua!',
            'Cumprimentos'
        ]
        text = random.choice(texts)
        self.lbl.text = text


class NameInputs(MDGridLayout):
    def __init__(self, x2=False, *args, **kwargs):
        super().__init__(cols=1, spacing=20, *args, **kwargs)
        self.x2 = x2
        default_args = dict(size_hint=[1,1],mode= "fill", radius=[0,40,0,40], fill_color_focus='white',
                            text_color_focus='black', helper_text_color_focus='white', helper_text_mode='on_error',
                            text_color_normal='black'
                            )
        self.name1 = MDTextField(text='Jogador 1', **default_args)
        self.add_widget(self.name1)
        if self.x2:
            self.name2 = MDTextField(text='Jogador 2', **default_args)
            self.add_widget(self.name2)

    def get_names(self):
        names = list()
        names.append(self.name1.text)
        if self.x2:
            names.append(self.name2.text)
        return names


class Team(MDRelativeLayout):
    def __init__(self, right_side=True, x2=True, team_number=1, board=None, *args, **kwargs):
        super().__init__(size_hint=TEAM_SIZE_HINT, *args, **kwargs)
        if team_number not in [1, 2]:
            raise ValueError(f'Value Should be 1 or 2')
        self.team_number = team_number
        self.right_side = right_side
        self.x2 = x2
        # self.winnings = StackLayout(size_hint=[.9,.1], pos_hint={'center':[.5,.95]},orientation='rl-tb')
        self.winnings = MDGridLayout(rows=1, size_hint=[.3,.1], pos_hint={'center':[.5,.95]})
        self.add_widget(self.winnings)
        self.team1 = TeamLabel(f'time {self.team_number}', initial_right=self.right_side, initial_top=not self.right_side)

        if self.x2:
            self.team2 = TeamLabel(f'time {self.team_number}.2', initial_right=self.right_side, initial_top=not self.right_side)
            self.add_widget(self.team2)
        self.add_widget(self.team1)
        self.team_sets = TeamSets(team_to_follow=self.team1, team_number=1)

        self.score_lbl = ScoreLabel(self.right_side)
        self.add_widget(self.score_lbl)

        self.all_points = list()
        self.add_widget(MDRectangleFlatButton(size_hint=[1,1], on_release=partial(board.set_points, self.team_number), line_color=[0,0,0,0]))

    def player_position(self, all_points, past_half):
        sets = len(all_points)
        even_sets = sets % 2 == 0

        self.change_position(even_sets, past_half)

        if self.x2:
            self.player_position_2x2(all_points, past_half)
        else:
            self.player_position_1x1(all_points, past_half)
        self.change_wins(all_points)

    def change_wins(self, all_points, end_game=False):
        self.winnings.clear_widgets()
        pts_to_check = all_points[:-1]
        if end_game:
            pts_to_check = all_points[:]
        for game in pts_to_check:
            if game:
                if game[-1] == self.team_number:
                    grid = MDGridLayout(cols=1, adaptive_width=True, size_hint=[.1,.8])
                    image = Image(source=os.path.join('.', 'images', 'volante.png'), size_hint=[1, 1],
                                 pos_hint={'center': [.5, .5]})
                    grid.add_widget(image)
                    self.winnings.add_widget(grid)

    def player_position_1x1(self, all_points, past_half):
        even_sets = len(all_points) % 2 == 0

        y_dif = .26

        if len(all_points)==0 or len(all_points[-1]) < 1:
            y_dif = 0
        else:
            last_pt = all_points[-1][-1]
            pts = all_points[-1][1:].count(last_pt)
            if pts % 2 == 0 ^ self.right_side:
                y_dif *= -1
            if even_sets:
                y_dif *= -1
            if past_half:
                y_dif *= -1
        self.team1.change_pos([.5, .5 + y_dif])

    def player_position_2x2(self, all_points, past_half):
        even = False

        if self.right_side:
            even = True

        for idx, pt in enumerate(all_points[-1][0:-1]):
            if pt == self.team_number and pt == all_points[-1][idx+1]:
                even = not even

        if past_half:
            even = not even


        if even:
            self.team1.change_pos([.5, .5 + .26])
            self.team2.change_pos([.5, .5 - .26])
        else:
            self.team1.change_pos([.5, .5 - .26])
            self.team2.change_pos([.5, .5 + .26])

    def change_names(self, name1=None , name2=None):
        if name1:
            self.team1.change_label(name1)
        if name2:
            self.team2.change_label(name2)

    def change_score(self, new_score):
        self.score_lbl.change_label(str(new_score))

    def change_color(self, color):
        self.score_lbl.change_color(color)

    def change_position(self, even_sets, past_half):
        x_dif = self.size_hint[0]/2
        y = .5
        lbl_right = False
        if even_sets == self.right_side:
            x_dif *= -1
            lbl_right = not lbl_right

        if past_half:
            x_dif *= -1
            lbl_right = not lbl_right
        main_center = {'center': [.5+x_dif, y]}


        self.score_lbl.change_position(lbl_right)

        if lbl_right:
            win_x = .85
        else:
            win_x = .15
        winnings_anim = Animation(pos_hint={'center': [win_x, .95]}, duration=.1)
        winnings_anim.start(self.winnings)

        anim = Animation(pos_hint=main_center, duration=.1)
        anim.start(self)

    def get_wins(self):
        return len(self.winnings.children)


class HistoryChart(Popup):
    def __init__(self, t1_name='team1', t2_name='team2', *args, **kwargs):
        super().__init__(title='Histórico', *args, **kwargs)
        self.score_history = MDGridLayout(cols=1)
        self.t1_name = t1_name
        self.t2_name = t2_name
        scroll = MDScrollView()

        # create the table
        ## head
        head = ['Times']
        head += tuple(range(1,60))

        # data
        data = [(self.t1_name, *list(range(1,60))), (self.t2_name, *list(range(1,60)))]

        scroll.add_widget(MDDataTable(column_data=head, row_data=data))

        self.add_widget(scroll)



    def update_score(self, score):
        t1 = list()
        t2 = list()
        pt_mark = '.'
        for pt in score[-1]:
            if pt == 1:
                t1.append(pt_mark)
                t2.append(' ')
            else:
                t1.append(' ')
                t2.append(pt_mark)
        self.t1.clear_widgets()
        self.t2.clear_widgets()
        for mark in t1:
            self.t1.add_widget(MDLabel(text=mark))
        for mark in t2:
            self.t2.add_widget(MDLabel(text=mark))


class SingleGame(MDRelativeLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.all_points = [[]]
        self.odds_begin = True
        self.max_points = 21
        self.score = [0, 0]
        self.game_over = GameOver()
        self.second_half = False
        self.hist = HistoryChart(size_hint=[.8, .4], pos_hint={'center': [.5, .8]})
        self.timer = MDRelativeLayout(md_bg_color=[0,0,0,1], size_hint=[.01, 0], pos_hint={'center_y':.5, 'center_x':.5})

        # Title
        if not hasattr(self, 'tittle'):
            self.tittle = MDLabel(text='Simples', font_style='H3', pos_hint={'center': [.5, .93]}, max_lines=1,
                                  halign='center', valign='center')


        # Teams
        if not hasattr(self, 'team1'):
            x2 = False
            self.team1 = Team(right_side=False, x2=x2, team_number=1, board=self,
                              pos_hint={'center': [.35, .6]})
            self.team2 = Team(right_side=True, x2=x2, team_number=2, board=self,
                              pos_hint={'center': [.65, .6]})


        # images
        self.image = Image(source=os.path.join('.', 'images', 'court.jpg'), size_hint=[.9, .7],
                           pos_hint={'center': [.5, .5]}, keep_ratio=False)

        self.shuttlecock = Image(source=os.path.join('.', 'images', 'volante.png'), size_hint=[.1, .1],
                                 pos_hint={'center': [.5, .5]})


        ############ Popups

        # Pontuation
        grid_pts = MDGridLayout(cols=1, adaptive_size=True, size_hint=[1, 1], spacing=10, padding=[10] * 4)

        for val in [7, 11, 15, 21, 'inf']:
            grid_pts.add_widget(
                MDRoundFlatButton(text=str(val), on_release=partial(self.change_max_points, val), halign='center',
                                  font_style='H6', size_hint=[1, 1]))
        self.popup = Popup(title=f'Pontuação', content=grid_pts, size_hint=[.5, .8], title_align='center',
                           title_size=MDLabel(font_style="H4").font_size)
        self.pts_btn = MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1],
                                             text=f'Pontuação: 21', size_hint=[.2, .1],
                                             pos_hint={'center': [.15, .93]}, font_style='H5',
                                             on_release=partial(self.popup.open), text_color=[0, 0, 0, 1])

        # Names Popup
        if not hasattr(self, 'names_popup'):
            team1 = NameInputs()
            team2 = NameInputs()
            names_grid = MDGridLayout(rows=1, spacing=20)
            names_grid.add_widget(team1)
            names_grid.add_widget(team2)
            self.names_popup = Popup(title=f'Times', content=names_grid, size_hint=[.5, 1], title_align='center',
                           title_size=MDLabel(font_style="H6").font_size, on_dismiss=partial(self.change_names, team1, team2))


        self.build()

    def build(self):
        self.clear_widgets()
        self.add_widget(self.image)
        self.add_widget(self.tittle)
        self.add_widget(MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1], text='Voltar',
                                              font_style='H5', size_hint=[.2, .1], pos_hint={'center': [.85, .93]},
                                              on_release=partial(self.change_window, 'main'), text_color=[0, 0, 0, 1]))
        self.add_widget(self.pts_btn)
        self.add_widget(self.team1)
        self.add_widget(self.team2)





        # Button for back point
        self.add_widget(
            MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1],
                                  text=f'Let it', size_hint=[.2, .1],
                                  pos_hint={'center': [.15, .08]}, font_style='H5',
                                  on_release=partial(self.back_point), text_color=[0, 0, 0, 1]))

        # Button for the history
        self.add_widget(
            MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1],
                                  text=f'Histórico', size_hint=[.2, .1],
                                  pos_hint={'center': [.85, .08]}, font_style='H5',
                                  on_release=partial(self.hist.open), text_color=[0, 0, 0, 1]))


        self.add_widget(self.shuttlecock)
        self.add_widget(
            MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1], text='^Acabar o set^',
                                  on_release=self.end_set, font_style='H3', text_color=[0, 0, 0, 1], size_hint=[.3,.1],
                                  pos_hint={'center': [.5, .08]}))


        self.add_widget(self.game_over)
        self.game_over.random_text()
        self.set_points()



    def change_names(self, team1, team2, *args):
        self.team1.change_names(*team1.get_names()[::-1])
        self.team2.change_names(*team2.get_names())

    def set_points(self, team=None, *args):

        if max(self.score) == 0:
            Animation.cancel_all(self.timer)
            self.remove_widget(self.timer)
        else:
            Animation.stop_all(self.timer)


        if not self.check_game_win() and not self.check_win() and team:
            if self.all_points == []:
                self.all_points.append([])
            self.all_points[-1].append(team)
            higher_score = max(self.score)
            if higher_score == self.max_points//2 and self.score[team-1] == higher_score:
                self.anim_timer(False)


        self.count_points()

        # change sides
        self.change_service()

        # change text
        self.change_text_score()

        # change color if match point
        self.change_text_score_color()

        # change_shuttlecock
        self.change_shuttlecock()

        self.hist.update_score(self.all_points)

    @staticmethod
    def set_players_name(obj):
        for widget in obj.content.children:
            widget.change_label()

    def check_game_win(self):
        t1 = self.team1.get_wins()
        t2 = self.team2.get_wins()

        if t1 >= 2 or t2>=2:
            self.game_over.move_up()
            self.remove_widget(self.timer)
            return True
        self.game_over.move_down()
        return False

    def reset_things(self, *args):
        self.all_points = [[]]
        self.score = [0, 0]
        self.build()
        self.game_over.move_down()
        self.set_points()
        self.names_popup.open()

    def change_window(self, new_window, *args):
        self.app.sm.current = new_window

    def end_set(self, *args):
        if len(self.all_points[-1]) == 0:
            return
        if len(self.all_points) >= 4:
            return
        if not self.check_game_win():
            self.all_points.append([])
        self.set_points()

        self.anim_timer()
        self.check_game_win()

    def check_win(self):
        """Returns True if any team won"""
        max_pts = max(self.score)
        min_pts = min(self.score)
        won = (max_pts >= self.max_points) and (abs(max_pts - min_pts) >= 2)
        if self.max_points != float('inf'):
            if max_pts >= 30:
                won = True
        if won:
            self.team1.change_wins(self.all_points, True)
            self.team2.change_wins(self.all_points, True)
            self.check_game_win()
        return won

    def change_text_score_color(self):
        t1, t2 = self.score
        color = 'red'
        default_color = 'white'
        max_default_pts = 29
        if self.check_win():
            color = 'gold'
        if (t1 > t2 and t1 >= self.max_points - 1):  # game point for team 1
            self.change_color(self.team1, color)
            self.change_color(self.team2, default_color)
        elif (t2 > t1 and t2 >= self.max_points - 1):  # game point for team 2
            self.change_color(self.team2, color)
            self.change_color(self.team1, default_color)
        else:
            self.change_color(self.team1, default_color)
            self.change_color(self.team2, default_color)

        if t1 == max_default_pts and t2 <= max_default_pts:
            self.change_color(self.team1, color)

        if t2 == max_default_pts and t1 <= max_default_pts:
            self.change_color(self.team2, color)

    def change_color(self, lbl, color, *args):
        lbl.change_color(color)

    def change_shuttlecock(self):
        if len(self.all_points)== 0 or len(self.all_points[-1]) == 0:
            self.shuttlecock.pos_hint = {'center': [.5, .5]}
            return
        x_dif = +.1
        y_dif = +.12

        last_pt = self.all_points[-1][-1]-1
        pts = self.score[last_pt]
        even_sets = len(self.all_points)%2 == 0

        if last_pt == 0:
            x_dif *= -1
            y_dif *= -1

        if even_sets:
            x_dif *= -1
            y_dif *= -1

        if pts % 2 == 1:
            y_dif *= -1

        if len(self.all_points) >= 3 and max(self.score) > self.max_points/2:
            y_dif *= -1
            x_dif *= -1


        y = .5 + y_dif
        x = .5 + x_dif

        anim = Animation(pos_hint={'center': [x, y]}, duration=.1, t='in_out_cubic')
        anim.start(self.shuttlecock)

    def change_text_score(self):
        t1, t2 = self.score
        self.team1.change_score(t1)
        self.team2.change_score(t2)

    def count_points(self):
        if len(self.all_points) < 1:
            return
        if len(self.all_points[-1]) >= 1:
            t1 = self.all_points[-1][1:].count(1)
            t2 = self.all_points[-1][1:].count(2)
        else:
            t1, t2 = 0, 0
        self.score = [t1, t2]

    def change_service(self):
        past_half = len(self.all_points) >= 3 and max(self.score) > ((self.max_points / 2))
        self.team1.player_position(self.all_points, past_half=past_half)
        self.team2.player_position(self.all_points, past_half=past_half)

    def back_point(self, *args):
        if len(self.all_points)>0 and len(self.all_points[-1]) >= 1:
            self.all_points[-1].pop()
        else:
            if self.all_points:
                self.all_points.pop()
        if self.all_points == []:
            self.all_points.append([])
        self.set_points()
        self.set_points()

    def change_max_points(self, new_pts, *args):
        self.max_points = float(new_pts)
        self.pts_btn.text = f'Pontuação: {new_pts}'
        self.popup.dismiss()

    def open_menu(self):
        self.popup.open()

    def anim_timer(self, full_timer=True):
        self.timer.md_bg_color = [0,0,0,1]
        if full_timer:
            duration = int(120)
        else:
            duration = int(60)
        self.add_widget(self.timer, -1)
        self.timer.size_hint = [.01, .7]
        anim_timer = Animation(size_hint=[.01, 0], duration=duration)
        anim_timer &= Animation(md_bg_color = [0,.7,0,1], duration=int(duration*.8))+\
                      Animation(md_bg_color = [0,1,0,1], duration=int(duration*.2))
        anim_timer.bind(on_complete=partial(self.on_complete, full_timer))
        anim_timer.start(self.timer)

    def on_complete(self, end_set, *args):
        self.remove_widget(self.timer)
        if end_set:
            last_pt = self.all_points[-2][-1]
            self.set_points(last_pt)


class DoubleGame(SingleGame):
    def __init__(self, *args, **kwargs):
        x2 = True
        self.team1 = Team(right_side=False, x2=x2, team_number=1, board=self,
                          pos_hint={'center': [.35, .6]})
        self.team2 = Team(right_side=True, x2=x2, team_number=2, board=self,
                          pos_hint={'center': [.65, .6]})
        self.tittle = MDLabel(text='Duplas', font_style='H3', pos_hint={'center': [.5, .93]}, max_lines=1,
                              halign='center', valign='center')
        team1 = NameInputs(True)
        team2 = NameInputs(True)
        grid = MDGridLayout(rows=1, spacing=20)
        grid.add_widget(team1)
        grid.add_widget(team2)
        self.names_popup = Popup(title=f'Times', content=grid, size_hint=[.5, 1], title_align='center',
                                 title_size=MDLabel(font_style="H6").font_size,
                                 on_dismiss=partial(self.change_names, team1, team2))
        super().__init__(*args, **kwargs)


class ContadorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_window = MainWindow(self)
        self.simple_game = SingleGame(self)
        self.double_game = DoubleGame(self)
        self.sm = ScreenManager()
        self.sm.add_widget(MyScreen(self.main_window, name='main'))
        self.sm.add_widget(MyScreen(self.simple_game, name='single', on_enter=self.simple_game.reset_things))
        self.sm.add_widget(MyScreen(self.double_game, name='double', on_enter=self.double_game.reset_things))

    def build(self):
        self.icon = os.path.join('.', 'images', 'icon.png')
        return self.sm


class EntreEmContato(MDApp):
    def build(self):
        txt = f'''Esse aplicativo foi desativado  por estar desatualizado. Entre em contato com Mutante Apps pelo email:

mutante.apps@gmail.com'''
        lbl = MDLabel(text=txt, font_style='H4', halign='center')
        return lbl

ContadorApp().run()

# if datetime.date.today() > PRAZO_MAXIMO:
#     EntreEmContato().run()
# else:
#     ContadorApp().run()
