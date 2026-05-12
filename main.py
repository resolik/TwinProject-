import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Ellipse, Mesh, RoundedRectangle
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from random import choice, randint

# Пути к ресурсам
BG_PATH = 'images/background.jpg'
FONT_PATH = 'fonts/main_font.ttf' 

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.font_name = FONT_PATH if os.path.exists(FONT_PATH) else 'Roboto'
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0.6, 0, 1) 
            RoundedRectangle(pos=self.pos, size=self.size, radius=[25,])

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = FloatLayout()
        
        if os.path.exists(BG_PATH):
            layout.add_widget(Image(source=BG_PATH, allow_stretch=True, keep_ratio=False))
        
        title = Label(
            text="TWIN", 
            font_size='60sp',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else 'Roboto',
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            color=(1, 1, 1, 1),
            outline_width=3, outline_color=(0,0,0,1)
        )
        
        btn_play = StyledButton(
            text="PLAY",
            size_hint=(0.5, 0.12),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            font_size='35sp'
        )
        btn_play.bind(on_release=self.start_game)
        
        layout.add_widget(title)
        layout.add_widget(btn_play)
        self.add_widget(layout)

    def start_game(self, *args):
        self.manager.current = 'game'

class GameScreen(Screen):
    def on_enter(self):
        self.layout = FloatLayout()
        self.score = 0
        
        if os.path.exists(BG_PATH):
            self.layout.add_widget(Image(source=BG_PATH, allow_stretch=True, keep_ratio=False))
        
        # ТЕПЕРЬ ПО ЦЕНТРУ (center_x: 0.5)
        self.score_label = Label(
            text=f"SCORE: {self.score}",
            font_size='30sp',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else 'Roboto',
            pos_hint={'center_x': 0.5, 'top': 0.97}, 
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            outline_width=2, outline_color=(0,0,0,1)
        )
        
        self.add_widget(self.layout)
        self.add_widget(self.score_label)
        self.event = Clock.schedule_interval(self.spawn_shape, 0.5)

    def spawn_shape(self, dt):
        colors = [(1, 0, 0, 1), (1, 0.5, 0, 1), (1, 1, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (0.2, 0, 0.5, 1), (0.5, 0, 1, 1), (1, 0.4, 0.7, 1)]
        size_val = randint(180, 350)
        shape_color = choice(colors)
        shape_type = choice(['square', 'circle', 'triangle'])
        side = choice(['left', 'right', 'top', 'bottom'])
        if side == 'left': start_pos = (-size_val, randint(0, Window.height)); end_pos = (Window.width + size_val, randint(0, Window.height))
        elif side == 'right': start_pos = (Window.width + size_val, randint(0, Window.height)); end_pos = (-size_val, randint(0, Window.height))
        elif side == 'top': start_pos = (randint(0, Window.width), Window.height + size_val); end_pos = (randint(0, Window.width), -size_val)
        else: start_pos = (randint(0, Window.width), -size_val); end_pos = (randint(0, Window.width), Window.height + size_val)
        shape = Button(size_hint=(None, None), size=(size_val, size_val), pos=start_pos, background_normal='', background_color=(0, 0, 0, 0))
        shape.shape_type = shape_type
        shape.shape_color = shape_color
        self.draw_figure(shape)
        shape.bind(pos=self.draw_figure, on_press=self.on_hit)
        self.layout.add_widget(shape)
        anim = Animation(x=end_pos[0], y=end_pos[1], duration=randint(1, 4))
        anim.bind(on_complete=lambda *args: self.remove_shape(shape))
        anim.start(shape)

    def draw_figure(self, instance, *args):
        instance.canvas.clear()
        with instance.canvas:
            Color(*instance.shape_color)
            x, y = instance.pos
            w, h = instance.size
            if instance.shape_type == 'square': Rectangle(pos=(x, y), size=(w, h))
            elif instance.shape_type == 'circle': Ellipse(pos=(x, y), size=(w, h))
            elif instance.shape_type == 'triangle': Mesh(vertices=[x, y, 0, 0, x+w, y, 0, 0, x+w/2, y+h, 0, 0], indices=[0, 1, 2], mode='triangles')

    def on_hit(self, instance):
        self.score += 1
        self.score_label.text = f"SCORE: {self.score}"
        self.layout.remove_widget(instance)

    def remove_shape(self, instance):
        if instance in self.layout.children:
            self.layout.remove_widget(instance)

    def on_leave(self):
        Clock.unschedule(self.event)
        self.layout.clear_widgets()

class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    MyGameApp().run()
