"""
Main Menu Screen for Quantum Snake Mobile
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
import random
from utils.constants import ScreenNames, MobileColors, GameSettings

class AnimatedBackground(FloatLayout):
    """Animated quantum background with floating particles"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.init_particles()
        Clock.schedule_interval(self.update_particles, 1/30)
    
    def init_particles(self):
        """Initialize background particles"""
        for i in range(30):
            particle = Ellipse(
                pos=(random.randint(0, self.width), random.randint(0, self.height)),
                size=(random.randint(2, 6), random.randint(2, 6))
            )
            self.particles.append({
                'shape': particle,
                'speed_x': random.uniform(-1, 1),
                'speed_y': random.uniform(-1, 1),
                'color': random.choice([
                    MobileColors.ACCENT_CYAN[:3] + (0.3,),
                    MobileColors.ACCENT_PURPLE[:3] + (0.3,),
                    (0.5, 0.5, 1, 0.2)
                ])
            })
            
            with self.canvas:
                Color(*self.particles[-1]['color'])
                self.canvas.add(particle)
    
    def update_particles(self, dt):
        """Update particle positions"""
        for particle in self.particles:
            x, y = particle['shape'].pos
            x += particle['speed_x']
            y += particle['speed_y']
            
            # Wrap around screen
            if x < 0:
                x = self.width
            elif x > self.width:
                x = 0
            if y < 0:
                y = self.height
            elif y > self.height:
                y = 0
                
            particle['shape'].pos = (x, y)

class GlowingLabel(Label):
    """Label with glowing animation effect"""
    
    glow_intensity = NumericProperty(0.5)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_glow_animation()
    
    def start_glow_animation(self):
        """Start pulsing glow animation"""
        anim = Animation(glow_intensity=1.0, duration=1.5) + \
               Animation(glow_intensity=0.5, duration=1.5)
        anim.repeat = True
        self.start_anim = anim
        anim.start(self)

class MenuButton(Button):
    """Custom styled menu button"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = MobileColors.SUCCESS_GREEN
        self.color = MobileColors.TEXT_WHITE
        self.font_size = GameSettings.UI_FONT_SIZE + 6
        self.bold = True
        self.size_hint = (0.8, None)
        self.height = 60
        self.pos_hint = {'center_x': 0.5}

class MenuScreen(Screen):
    """Main menu screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface"""
        # Create main layout
        self.layout = FloatLayout()
        
        # Add animated background
        self.background = AnimatedBackground(size=self.size)
        self.layout.add_widget(self.background)
        
        # Create content container
        content = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=40,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Game title with glow effect
        self.title = GlowingLabel(
            text='QUANTUM SNAKE',
            font_size=48,
            bold=True,
            color=MobileColors.ACCENT_CYAN,
            size_hint=(1, 0.3),
            halign='center',
            valign='middle'
        )
        self.title.bind(size=self.title.setter('text_size'))
        
        # Subtitle
        self.subtitle = Label(
            text='Mobile Edition',
            font_size=24,
            color=MobileColors.WARNING_ORANGE,
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.subtitle.bind(size=self.subtitle.setter('text_size'))
        
        # Button container
        button_container = BoxLayout(
            orientation='vertical',
            spacing=15,
            size_hint=(1, 0.4),
            pos_hint={'center_x': 0.5}
        )
        
        # Create buttons
        self.start_button = MenuButton(
            text='START GAME',
            background_color=MobileColors.SUCCESS_GREEN,
            background_normal='',
            on_release=self.on_start_game
        )
        
        self.settings_button = MenuButton(
            text='SETTINGS',
            background_color=MobileColors.ACCENT_CYAN,
            background_normal='',
            on_release=self.on_settings
        )
        
        self.exit_button = MenuButton(
            text='EXIT',
            background_color=MobileColors.ERROR_RED,
            background_normal='',
            on_release=self.on_exit
        )
        
        # Add buttons to container
        button_container.add_widget(self.start_button)
        button_container.add_widget(self.settings_button)
        button_container.add_widget(self.exit_button)
        
        # Add widgets to content
        content.add_widget(self.title)
        content.add_widget(self.subtitle)
        content.add_widget(button_container)
        
        # Add level descriptions
        desc_container = BoxLayout(
            orientation='vertical',
            spacing=5,
            size_hint=(1, 0.2),
            padding=[20, 0, 20, 0]
        )
        
        descriptions = [
            "• Level 1: Semi-Quantum - Both snakes grow",
            "• Level 2: Quantum - Eating grows you, shrinks opponent",
            "• Level 3: Super-Quantum - Quantum gates with TELEPORT"
        ]
        
        for desc in descriptions:
            desc_label = Label(
                text=desc,
                font_size=14,
                color=MobileColors.TEXT_GRAY,
                size_hint=(1, None),
                height=20,
                halign='center',
                valign='middle'
            )
            desc_label.bind(size=desc_label.setter('text_size'))
            desc_container.add_widget(desc_label)
        
        content.add_widget(desc_container)
        
        # Add content to main layout
        self.layout.add_widget(content)
        
        # Add version info
        version_label = Label(
            text=f'v{self.app.version if self.app else "1.0.0"}',
            font_size=12,
            color=MobileColors.TEXT_GRAY,
            size_hint=(None, None),
            pos=(10, 10)
        )
        self.layout.add_widget(version_label)
        
        self.add_widget(self.layout)
        
        # Start entrance animation
        self.animate_entrance()
    
    def animate_entrance(self):
        """Animate screen entrance"""
        # Start with title off screen
        self.title.y = self.height
        
        # Animate title dropping in
        anim = Animation(y=self.height * 0.2, duration=0.8, t='out_bounce')
        anim.start(self.title)
        
        # Animate buttons appearing with delay
        buttons = [self.start_button, self.settings_button, self.exit_button]
        for i, button in enumerate(buttons):
            button.opacity = 0
            button.y -= 50
            
            anim = Animation(opacity=1, y=button.y + 50, duration=0.5, t='out_quad')
            anim.start_delay = 0.5 + i * 0.1
            anim.start(button)
    
    def on_start_game(self, instance):
        """Handle start game button press"""
        if self.app:
            self.app.vibrate(0.05)
        self.animate_button_press(instance)
        Clock.schedule_once(lambda dt: self.change_screen(ScreenNames.LEVEL_SELECT), 0.2)
    
    def on_settings(self, instance):
        """Handle settings button press"""
        if self.app:
            self.app.vibrate(0.05)
        self.animate_button_press(instance)
        Clock.schedule_once(lambda dt: self.change_screen(ScreenNames.SETTINGS), 0.2)
    
    def on_exit(self, instance):
        """Handle exit button press"""
        if self.app:
            self.app.vibrate(0.05)
        self.animate_button_press(instance)
        Clock.schedule_once(lambda dt: self.app.stop() if self.app else exit(), 0.2)
    
    def animate_button_press(self, button):
        """Animate button press effect"""
        original_scale = button.size_hint_x
        
        anim = Animation(size_hint_x=original_scale * 0.95, duration=0.1) + \
               Animation(size_hint_x=original_scale, duration=0.1)
        anim.start(button)
    
    def change_screen(self, screen_name):
        """Change to different screen"""
        if self.app:
            self.app.change_screen(screen_name)
    
    def on_enter(self):
        """Called when screen is entered"""
        # Restart background animation
        if hasattr(self, 'background'):
            self.background.init_particles()
    
    def on_leave(self):
        """Called when screen is left"""
        # Stop animations
        if hasattr(self.title, 'start_anim'):
            self.title.start_anim.cancel(self.title)