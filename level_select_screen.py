"""
Level Selection Screen for Quantum Snake Mobile
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty
from kivy.animation import Animation
from kivy.clock import Clock
from utils.constants import ScreenNames, LevelType, LEVEL_DESCRIPTIONS, MobileColors

class LevelCard(Button):
    """Custom level selection card"""
    
    level_type = StringProperty('')
    title = StringProperty('')
    description = StringProperty('')
    card_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = self.card_color
        self.color = MobileColors.TEXT_WHITE
        self.font_size = 16
        self.bold = True
        self.size_hint_y = None
        self.height = 150
        
        # Create card content
        self.build_content()
    
    def build_content(self):
        """Build card content layout"""
        # Clear existing content
        self.clear_widgets()
        
        # Main layout
        card_layout = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=5
        )
        
        # Title
        title_label = Label(
            text=self.title,
            font_size=20,
            bold=True,
            color=MobileColors.TEXT_WHITE,
            size_hint_y=0.3,
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Description
        desc_label = Label(
            text=self.description,
            font_size=14,
            color=MobileColors.TEXT_GRAY,
            size_hint_y=0.5,
            halign='left',
            valign='top'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        
        # Difficulty indicator
        difficulty_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.2,
            spacing=5
        )
        
        # Add difficulty dots based on level
        difficulty_levels = {
            LevelType.SEMI_QUANTUM: 1,
            LevelType.QUANTUM: 2,
            LevelType.SUPER_QUANTUM: 3
        }
        
        difficulty = difficulty_levels.get(self.level_type, 1)
        for i in range(3):
            dot = Label(
                text='●',
                font_size=20,
                color=MobileColors.ACCENT_CYAN if i < difficulty else MobileColors.TEXT_GRAY,
                size_hint_x=None,
                width=20
            )
            difficulty_container.add_widget(dot)
        
        difficulty_container.add_widget(Label())  # Spacer
        
        card_layout.add_widget(title_label)
        card_layout.add_widget(desc_label)
        card_layout.add_widget(difficulty_container)
        
        self.add_widget(card_layout)

class LevelSelectScreen(Screen):
    """Level selection screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface"""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # Header
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing=10
        )
        
        # Back button
        back_button = Button(
            text='← BACK',
            font_size=18,
            color=MobileColors.TEXT_WHITE,
            background_color=MobileColors.SECONDARY_BG,
            background_normal='',
            size_hint_x=0.3,
            on_release=self.on_back
        )
        
        # Title
        title = Label(
            text='SELECT LEVEL',
            font_size=24,
            bold=True,
            color=MobileColors.TEXT_WHITE,
            size_hint_x=0.7,
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Level cards container
        cards_container = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint_y=0.8
        )
        
        # Create level cards
        for level_type, level_info in LEVEL_DESCRIPTIONS.items():
            card = LevelCard(
                level_type=level_type,
                title=level_info['title'],
                description=level_info['description'],
                card_color=level_info['color'],
                on_release=lambda btn, lvl=level_type: self.on_level_select(btn, lvl)
            )
            cards_container.add_widget(card)
        
        # Instructions
        instructions = Label(
            text='Each level introduces new quantum mechanics!\nComplete Level 1 to unlock the next challenge.',
            font_size=14,
            color=MobileColors.TEXT_GRAY,
            size_hint_y=0.1,
            halign='center',
            valign='middle'
        )
        instructions.bind(size=instructions.setter('text_size'))
        
        # Add all to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(cards_container)
        main_layout.add_widget(instructions)
        
        self.add_widget(main_layout)
    
    def on_back(self, instance):
        """Handle back button"""
        if self.app:
            self.app.vibrate(0.05)
        self.animate_button_press(instance)
        Clock.schedule_once(lambda dt: self.change_screen(ScreenNames.MENU, 'right'), 0.2)
    
    def on_level_select(self, instance, level_type):
        """Handle level selection"""
        if self.app:
            self.app.vibrate(0.1)
        self.animate_button_press(instance)
        
        # Store selected level and navigate to game
        Clock.schedule_once(
            lambda dt: self.start_game(level_type), 
            0.3
        )
    
    def start_game(self, level_type):
        """Start the game with selected level"""
        if self.app:
            # Pass level to game screen
            game_screen = self.app.screen_manager.get_screen(ScreenNames.GAME)
            game_screen.set_level(level_type)
            
            # Navigate to game
            self.change_screen(ScreenNames.GAME)
    
    def animate_button_press(self, button):
        """Animate button press effect"""
        original_scale = button.size_hint_x if button.size_hint_x else 1
        original_y = button.y
        
        # Scale down and move slightly
        anim = Animation(
            size_hint_x=original_scale * 0.95,
            y=original_y - 5,
            duration=0.1
        ) + Animation(
            size_hint_x=original_scale,
            y=original_y,
            duration=0.1
        )
        anim.start(button)
    
    def change_screen(self, screen_name, direction='left'):
        """Change to different screen"""
        if self.app:
            self.app.change_screen(screen_name, direction)
    
    def on_enter(self):
        """Called when screen is entered"""
        # Animate cards entrance
        cards = [child for child in self.children[0].children if isinstance(child, BoxLayout)][0].children
        
        for i, card in enumerate(cards):
            if isinstance(card, LevelCard):
                card.opacity = 0
                card.y -= 50
                
                anim = Animation(
                    opacity=1,
                    y=card.y + 50,
                    duration=0.6,
                    t='out_quad'
                )
                anim.start_delay = i * 0.1
                anim.start(card)