"""
This is a badminton points counter
"""
__version__ = "3.0.1"


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

# import other things


# variables


# Screens
class MyScreen(Screen):
    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(widget)


# Windows
# Main Window
class MainWindow(MDRelativeLayout):
    def __init__(self, app, **kwargs):
        # super().__init__(cols=2, size_hint=[1, 1], padding = [50,50,50,50], **kwargs)
        super().__init__(size_hint=[1, 1], pos_hint={'center': [.5, .5]}, **kwargs)
        self.app = app
        grid = MDGridLayout(cols=2, size_hint=[.9, .8], pos_hint={'center': [.5, .5]}, spacing=50)
        grid.add_widget(MDRectangleFlatButton(text='Simples', size_hint=[1, 1], on_release=partial(self.change_window,
                                                                                                   'single')))
        grid.add_widget(MDRectangleFlatButton(text='Duplas', size_hint=[1, 1],on_release=partial(self.change_window,
                                                                                                   'double')))
        self.add_widget(grid)

    def change_window(self, new_window, *args):
        self.app.sm.current = new_window


# helpers widgets Window
class TeamLabel(MDGridLayout):
    def __init__(self, team_name, pos_hint, **kwargs):
        super().__init__(cols=1, adaptive_size = True, md_bg_color=[.7, .7, .7, 1], pos_hint=pos_hint, **kwargs)
        self.team_name_lbl = MDLabel(text=team_name, halign='center', font_style='H4', max_lines=1)
        self.team_name_lbl = MDLabel(text=team_name, halign='center', font_style='H4', max_lines=1,adaptive_size=True)
        self.add_widget(self.team_name_lbl)

    def change_pos(self, new_pos):
        self.pos_hint = {'center': new_pos}

    def change_label(self, new_name):
        self.team_name_lbl.text = new_name

    def get_name(self):
        return self.team_name_lbl.text

    def get_pos_hint(self):
        return self.pos


class ScoreLabel(MDGridLayout):
    def __init__(self, score, pos_hint, **kwargs):
        super().__init__(cols=1, size_hint=[.1, .2], md_bg_color=[0, 0, 0, 1], pos_hint=pos_hint, **kwargs)
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


# Single Window
class SingleGame(MDRelativeLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.all_points = list()
        self.odds_begin = True
        self.max_points = 21
        self.score = [0, 0]
        self.team1 = TeamLabel('time 1', {'center': [.25, .5]})
        self.team2 = TeamLabel('time 2', {'center': [.75, .5]})
        self.image = Image(source=os.path.join('.', 'images', 'court.jpg'), size_hint = [.9,.8], pos_hint={'center':[.5,.5]})
        self.shuttlecock = Image(source=os.path.join('.', 'images', 'volante.png'), size_hint=[.1, .1],
                                 pos_hint={'center': [.5, .5]})
        self.score_t1 = ScoreLabel(str(0), {'center': [.05, .5]})
        self.score_t2 = ScoreLabel(str(0), {'center': [.95, .5]})

        # buttons


        # popup
        grid = MDGridLayout(cols=1,adaptive_size=True, size_hint=[1,1],spacing=10, padding=[10]*4)
        for val in [7,11,15,21, 'inf']:
            grid.add_widget(MDRoundFlatButton(text=str(val), on_release=partial(self.change_max_points, val),halign='center',font_style='H5',size_hint=[1,1]))
        self.popup = Popup(title = f'Pontuação',content=grid, size_hint=[.5,.8],title_align='center',title_size=MDLabel(font_style="H4").font_size)
        self.pts_btn = MDRectangleFlatButton(text=f'Pontuação: {float("inf")}', size_hint=[.2, .1],
                                             pos_hint={'center': [.15, .93]}, font_style='H5',
                                             on_release=partial(self.popup.open), text_color=[0, 0, 0, 1])
        self.build()

    def build(self):
        self.clear_widgets()
        self.add_widget(self.image)
        self.add_widget(MDLabel(text='1x1', font_style='H3', adaptive_size=True, pos_hint={'center': [.5, .93]}))
        self.add_widget(MDRectangleFlatButton(text='Voltar', font_style='H5', size_hint=[.2, .1], pos_hint={'center': [.85, .93]},
                                              on_release=partial(self.change_window, 'main'),text_color = [0,0,0,1]))
        self.add_widget(self.pts_btn)  # ! preciso fazer a função para criar uma popup
        self.add_widget(self.team1)
        self.add_widget(self.team2)

        # buttons for increase points
        self.add_widget(MDRectangleFlatButton(pos_hint={'center': [.25, .5]}, size_hint=[.5, .65],
                                              on_release=partial(self.set_points, 1)))
        self.add_widget(MDRectangleFlatButton(pos_hint={'center': [.75, .5]}, size_hint=[.5, .65],
                                              on_release=partial(self.set_points, 2)))

        # Button for back point
        self.add_widget(
            MDRectangleFlatButton(text=f'Let it', size_hint=[.2, .1],
                                  pos_hint={'center': [.15, .08]}, font_style='H5',
                                  on_release=partial(self.back_point), text_color=[0, 0, 0, 1]))

        self.add_widget(self.score_t1)
        self.add_widget(self.score_t2)
        self.add_widget(self.shuttlecock)
        self.add_widget(MDRectangleFlatButton(text='^Acabar o set^', on_release=self.end_set, font_style= 'H3', text_color = [0,0,0,1], pos_hint={'center': [.5, .08]}))
        self.set_points()

    def reset_things(self, *args):
        self.all_points = list()
        self.score = [0, 0]
        self.build()

    def change_window(self, new_window, *args):
        self.reset_things()
        self.app.sm.current = new_window

    def set_points(self, team=None, *args):
        # add the point
        if team is not None and max(self.score)<self.max_points:
            self.all_points.append(team)

        # count
        self.count_points()

        # change sides
        self.change_service()

        # change text
        self.change_text_score()

        # change_shuttlecock
        self.change_shuttlecock()

    def end_set(self, *args):
        self.reset_things()
        lbl1 = self.team1.get_name()
        lbl2 = self.team2.get_name()
        self.team1.change_label(lbl2)
        self.team2.change_label(lbl1)

    def change_shuttlecock(self):
        if len(self.all_points) == 0:
            self.shuttlecock.pos_hint = {'center': [.5, .5]}
            return
        x = .4
        y = .62
        last_pt = self.all_points[-1] - 1
        pts = self.score[last_pt]

        if last_pt == 1:
            x = .6

        if pts % 2 == 0 and last_pt == 0:
            y = .38
        elif pts % 2 == 1 and last_pt == 1:
            y = .38

        self.shuttlecock.pos_hint = {'center': [x, y]}

    def change_text_score(self):
        t1, t2 = self.score
        self.score_t1.change_label(t1)
        self.score_t2.change_label(t2)

    def count_points(self):
        if len(self.all_points) >= 1:
            t1 = self.all_points[1:].count(1)
            t2 = self.all_points[1:].count(2)
        else:
            t1, t2 = 0, 0
        self.score = [t1, t2]

    def change_service(self):
        if len(self.all_points) >= 1:
            last_pt = self.all_points[-1] - 1
            pts = self.score[last_pt]
            if pts % 2 == 0:
                self.set_even_side()
            else:
                self.set_odds_side()
        else:
            self.set_center_side()

    def set_odds_side(self):
        dif = .12
        self.team1.change_pos([.25, .5 + dif])
        self.team2.change_pos([.75, .5 - dif])

    def set_even_side(self):
        dif = .12
        self.team1.change_pos([.25, .5 - dif])
        self.team2.change_pos([.75, .5 + dif])

    def set_center_side(self):
        self.team1.change_pos([.25, .5])
        self.team2.change_pos([.75, .5])

    def back_point(self, *args):
        if len(self.all_points) >= 1:
            self.all_points.pop()
            self.set_points()

    def change_max_points(self, new_pts, *args):
        self.max_points = float(new_pts)
        self.pts_btn.text= f'Pontuação: {new_pts}'
        self.popup.dismiss()

    def open_menu(self):
        self.popup.open()


# double Window
class DoubleGame(SingleGame):
    def __init__(self,*args, **kwargs):
        self.team3 = TeamLabel('time 1.2', {'center': [.25, .38]})
        self.team4 = TeamLabel('time 2.2', {'center': [.75, .38]})
        super().__init__(*args, **kwargs)
        self.team1 = TeamLabel('time 1.1', {'center': [.25, .62]})
        self.team2 = TeamLabel('time 2.1', {'center': [.75, .62]})
        self.build()

    def build(self):
        super().build()
        ind = 7
        self.add_widget(self.team3, ind)
        self.add_widget(self.team4, ind)

    def change_service(self):
        change = [True, True]
        if len(self.all_points)>1:
            for idx, pt in enumerate(self.all_points[1:]):
                if pt == self.all_points[idx]:
                    change[pt-1] = not change[pt-1]
        t1 , t2 = change
        self.set_t1_pos(t1)
        self.set_t2_pos(t2)

    def set_t1_pos(self, even):
        p1 = [.25, .62]
        p2 = [.25, .38]
        if not even:
            p1,p2 = p2,p1
        self.team1.change_pos(p1)
        self.team3.change_pos(p2)

    def set_t2_pos(self, even):
        p1 = [.75, .62]
        p2 = [.75, .38]
        if not even:
            p1, p2 = p2, p1
        self.team2.change_pos(p1)
        self.team4.change_pos(p2)

    def end_set(self, *args):
        self.reset_things()
        lbl1 = self.team1.get_name()
        lbl3 = self.team3.get_name()
        lbl2 = self.team2.get_name()
        lbl4 = self.team4.get_name()
        self.team1.change_label(lbl4)
        self.team3.change_label(lbl2)
        self.team2.change_label(lbl3)
        self.team4.change_label(lbl1)

# Main App
class ContadorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_window = MainWindow(self)
        self.simple_game = SingleGame(self)
        self.double_game = DoubleGame(self)
        self.sm = ScreenManager()
        self.sm.add_widget(MyScreen(self.double_game, name='double'))
        self.sm.add_widget(MyScreen(self.simple_game, name='single'))
        self.sm.add_widget(MyScreen(self.main_window, name='main'))

    def build(self):
        return self.sm


# tests
ContadorApp().run()
