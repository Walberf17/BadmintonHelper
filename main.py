"""
This is a badminton points counter
"""
__version__ = "3.4.4"

import os
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
from kivy.uix.label import Label
from kivy.uix.button import Button


# import other things


# variables


# Screens
class MyScreen(Screen):
    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(widget)


class TeamSets(MDGridLayout):
    def __init__(self, team_to_follow, team_number=2, *args, **kwargs):
        super().__init__(rows=1, size_hint=[.3, .1], pos_hint={'center': [.5, .8]}, *args, **kwargs)
        self.team_to_follow = team_to_follow
        self.team_number = team_number
        self.image_file = os.path.join('.', 'images', 'volante.png')
        self.add_widget(
            MDLabel(text=str(self.team_number), size_hint=[1, 1], pos_hint={'center': [.5, .5]}, halign='center'))
        self.bind(on_center_x=self.team_to_follow.setter('center_x'))

    def set_wins(self, all_pts):
        self.clear_widgets()
        self.add_widget(
            MDLabel(text=str(self.team_number), size_hint=[1, 1], pos_hint={'center': [.5, .5]}, halign='center'))
        if len(all_pts) > 1:
            for set in all_pts[:-1]:
                if set[-1] == (self.team_number + len(all_pts) % 2) % 2:
                    self.add_widget(Image(source=self.image_file, size_hint=[1, 1],
                                          pos_hint={'center': [.5, .5]}))
        self.set_pos3()

    def set_pos3(self):
        pos_hint = self.team_to_follow.pos_hint
        x, y = pos_hint.get('center')
        self.pos_hint = {'center': [x, .85]}

    def set_pos2(self, all_pts):
        x, y = self.initial_right * 2


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
    def __init__(self, score, pos_hint, **kwargs):
        super().__init__(cols=1, size_hint=[.3, .2], md_bg_color=[0, 0, 0, 1], pos_hint=pos_hint, **kwargs)
        self.score_lbl = MDLabel(text=score, halign='center', font_style='H2', max_lines=1, theme_text_color='Custom',
                                 text_color='white')
        self.add_widget(self.score_lbl)

    def change_pos(self, new_pos):
        self.pos_hint = {'center': new_pos}

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
        super().__init__(size_hint=[1, 1], pos_hint={'center': [.5, -.5]}, *args, **kwargs)
        self.add_widget(MDLabel(text='Eba!!! Ganhou!!!', font_style='H1', valign='center', halign='center'))

    def move_up(self):
        anim = Animation(pos_hint={'center': [.5, .3]}, duration=.2)
        anim.start(self)

    def move_down(self):
        anim = Animation(pos_hint={'center': [.5, -.5]}, duration=.2)
        anim.start(self)


class NameInput(MDTextField):
    def __init__(self, name, label_team, *args, **kwargs):
        super().__init__(text_color_normal=[0, 0, 0, 1], text=name, mode='round', fill_color_normal=[1, 1, 1, 1], *args,
                         **kwargs)
        self.label_team = label_team

    def change_label(self):
        if self.text:
            return
            self.label_team.change_label(self.text)


class Team(MDRelativeLayout):
    def __init__(self, right_side=True, x2=True, team_number=1, board=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if team_number not in [1, 2]:
            raise ValueError(f'Value Should be 1 or 2')
        self.team_number = team_number
        self.right_side = right_side
        self.x2 = x2
        self.winnings = MDGridLayout(rows=1, size_hint=[.9,.1], pos_hint={'center':[.5,.95]})
        self.add_widget(self.winnings)
        self.team1 = TeamLabel(f'time {self.team_number}', initial_right=self.right_side, initial_top=not self.right_side)

        if self.x2:
            self.team2 = TeamLabel(f'time {self.team_number}.2', initial_right=self.right_side, initial_top=not self.right_side)
            self.add_widget(self.team2)
        self.add_widget(self.team1)
        self.team_sets = TeamSets(team_to_follow=self.team1, team_number=1)

        self.score_dif = .05
        center = {'center': [0 + self.score_dif, .5]}

        if self.right_side:
            center = {'center': [1 - self.score_dif, .5]}
        self.score_lbl = ScoreLabel(str(0), center)
        self.add_widget(self.score_lbl)

        self.all_points = list()
        self.add_widget(MDRectangleFlatButton(size_hint=[1,1], on_release=partial(board.set_points, self.team_number)))

    def player_position(self, all_points, past_half):
        sets = len(all_points)
        even_sets = sets % 2 == 0

        self.change_position(even_sets, past_half)

        if self.x2:
            self.player_position_2x2(all_points, past_half)
        else:
            self.player_position_1x1(all_points, past_half)
        self.change_wins(all_points)

    def change_wins(self, all_points):
        self.winnings.clear_widgets()
        for game in all_points[:-1]:
            if game:
                if game[-1] == self.team_number:
                    image = Image(source=os.path.join('.', 'images', 'volante.png'), size_hint=[.1, .1],
                                 pos_hint={'center': [.5, .5]})
                    self.winnings.add_widget(image)

    def player_position_1x1(self, all_points, past_half):
        even_sets = len(all_points) % 2 == 0

        y_dif = .23

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

    def change_names(self, name1=None, name2=None):
        if name1:
            self.team1.change_label(name1)
        if name2:
            self.team2.change_label(name2)

    def change_score(self, new_score):
        self.score_lbl.change_label(str(new_score))

    def change_color(self, color):
        self.score_lbl.change_color(color)

    def change_position(self, even_sets, past_half):
        x_dif = .2
        y = .5
        lbl_right = False
        if even_sets == self.right_side:
            x_dif *= -1
            lbl_right = not lbl_right

        if past_half:
            x_dif *= -1
            lbl_right = not lbl_right
        center = {'center': [.5+x_dif, y]}

        if lbl_right:
            pos_hint = {'center': [.05, .5]}
        else:
            pos_hint = {'center': [.95, .5]}

        anim_lbl = Animation(pos_hint=pos_hint, duration=.1)
        anim_lbl.start(self.score_lbl)

        anim = Animation(pos_hint=center, duration=.1)
        anim.start(self)

    def get_wins(self):
        return len(self.winnings.children)


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

        if not hasattr(self, 'team1'):
            self.team1 = Team(right_side=False, x2=False, team_number=1, size_hint=[.4, .7], board=self,
                              pos_hint={'center': [.35, .6]})
            self.team2 = Team(right_side=True, x2=False, team_number=2, size_hint=[.4, .7], board=self,
                              pos_hint={'center': [.65, .6]})

        self.image = Image(source=os.path.join('.', 'images', 'court.jpg'), size_hint=[.9, .7],
                           pos_hint={'center': [.5, .5]}, keep_ratio=False)

        self.shuttlecock = Image(source=os.path.join('.', 'images', 'volante.png'), size_hint=[.1, .1],
                                 pos_hint={'center': [.5, .5]})

        if not hasattr(self, 'tittle'):
            self.tittle = MDLabel(text='Simples', font_style='H3', pos_hint={'center': [.5, .93]}, max_lines=1,
                                  halign='center', valign='center')

        # buttons

        # popup
        grid = MDGridLayout(cols=1, adaptive_size=True, size_hint=[1, 1], spacing=10, padding=[10] * 4)

        for val in [7, 11, 15, 21, 'inf']:
            grid.add_widget(
                MDRoundFlatButton(text=str(val), on_release=partial(self.change_max_points, val), halign='center',
                                  font_style='H5', size_hint=[1, 1]))
        self.popup = Popup(title=f'Pontuação', content=grid, size_hint=[.5, .8], title_align='center',
                           title_size=MDLabel(font_style="H4").font_size)
        self.pts_btn = MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1],
                                             text=f'Pontuação: 21', size_hint=[.2, .1],
                                             pos_hint={'center': [.15, .93]}, font_style='H5',
                                             on_release=partial(self.popup.open), text_color=[0, 0, 0, 1])

        # names popup
        names_grid = MDGridLayout(cols=2, adaptive_size=True, size_hint=[1, 1], spacing=10, padding=[10] * 4)
        names_grid.add_widget(NameInput(name='Player1', label_team=self.team1))
        names_grid.add_widget(NameInput(name='Player2', label_team=self.team2))

        self.names_popup = Popup(pos_hint={'center': [.5, .3]}, on_dismiss=self.set_players_name,
                                 title=f'Nome dos Competidores', content=names_grid, size_hint=[.6, 1],
                                 title_align='center', title_size=MDLabel(font_style="H4").font_size)

        self.build()

    def build(self):
        self.clear_widgets()
        self.add_widget(self.image)
        self.add_widget(self.tittle)
        self.add_widget(MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1], text='Voltar',
                                              font_style='H5', size_hint=[.2, .1], pos_hint={'center': [.85, .93]},
                                              on_release=partial(self.change_window, 'main'), text_color=[0, 0, 0, 1]))
        self.add_widget(self.pts_btn)  # ! preciso fazer a função para criar uma popup
        self.add_widget(self.team1)
        self.add_widget(self.team2)

        # Button for back point
        self.add_widget(
            MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1],
                                  text=f'Let it', size_hint=[.2, .1],
                                  pos_hint={'center': [.15, .08]}, font_style='H5',
                                  on_release=partial(self.back_point), text_color=[0, 0, 0, 1]))

        self.add_widget(self.shuttlecock)
        self.add_widget(
            MDRectangleFlatButton(line_color=[0, 0, 0, 0], md_bg_color=[.7, 0.7, 0.7, 1], text='^Acabar o set^',
                                  on_release=self.end_set, font_style='H3', text_color=[0, 0, 0, 1],
                                  pos_hint={'center': [.5, .08]}))
        self.add_widget(self.game_over)
        self.set_points()


    def set_points(self, team=None, *args):


        if not self.check_game_win() and not self.check_win() and team:
            if self.all_points == []:
                self.all_points.append([])
            self.all_points[-1].append(team)
            # count


        self.count_points()

        # change sides
        self.change_service()

        # change text
        self.change_text_score()

        # change color if match point
        self.change_text_score_color()

        # change_shuttlecock
        self.change_shuttlecock()


    @staticmethod
    def set_players_name(obj):
        for widget in obj.content.children:
            widget.change_label()

    def check_game_win(self):
        t1 = self.team1.get_wins()
        t2 = self.team2.get_wins()
        if t1 >= 2 or t2>=2:
            self.game_over.move_up()
            return True
        self.game_over.move_down()
        return False

    def set_team_sets_position(self):
        past_half = len(self.all_points) >= 3 and max(self.score) >= ((self.max_points / 2) + 1)
        self.team1_sets.player_position(all_points=self.all_points, past_half=past_half)
        self.team2_sets.player_position(all_points=self.all_points, past_half=past_half)

    def reset_things(self, *args):
        self.all_points = [[]]
        self.score = [0, 0]
        self.build()
        self.game_over.move_down()
        self.set_points()

    def change_window(self, new_window, *args):
        self.reset_things()
        self.app.sm.current = new_window

    def check_game_win_counter(self):
        t1, t2 = self.score

        self.check_win()
        if self.won:
            if t1 > t2:
                self.team1_sets.text = (len(self.team1_sets.text) + 1) * '*'
            else:
                self.team2_sets.text = (len(self.team2_sets.text) + 1) * '*'

    def end_set(self, *args):
        if len(self.all_points[-1]) == 0:
            return
        if len(self.all_points) >= 4:
            return
        last_pt = self.all_points[-1][-1]
        self.all_points.append([])
        self.set_points()
        self.set_points(last_pt)

    def check_win(self):
        """Returns True if any team won"""
        max_pts = max(self.score)
        min_pts = min(self.score)
        won = (max_pts >= self.max_points) and (abs(max_pts - min_pts) >= 2)
        if self.max_points != float('inf'):
            if max_pts >= 30:
                won = True
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


class DoubleGame(SingleGame):
    def __init__(self, *args, **kwargs):
        self.tittle = MDLabel(text='Duplas', font_style='H3', pos_hint={'center': [.5, .93]}, max_lines=1,
                              halign='center', valign='center')
        self.team1 = Team(right_side=False, x2=True, team_number=1, size_hint=[.4, .7], board=self,
                          pos_hint={'center': [.35, .6]})
        self.team2 = Team(right_side=True, x2=True, team_number=2, size_hint=[.4, .7], board=self,
                          pos_hint={'center': [.65, .6]})
        super().__init__(*args, **kwargs)



# Tests
class ContadorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_window = MainWindow(self)
        self.simple_game = SingleGame(self)
        self.double_game = DoubleGame(self)
        self.sm = ScreenManager()
        self.sm.add_widget(MyScreen(self.main_window, name='main'))
        self.sm.add_widget(MyScreen(self.simple_game, name='single', on_enter=self.simple_game.names_popup.open))
        self.sm.add_widget(MyScreen(self.double_game, name='double', on_enter=self.double_game.names_popup.open))

    def build(self):
        return self.sm


ContadorApp().run()
