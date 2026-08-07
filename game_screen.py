"""
Game Screen for Quantum Snake Mobile
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Canvas, InstructionGroup
from kivy.core.window import Window
from kivy.vector import Vector
import random
import math
from utils.constants import (
    ScreenNames, LevelType, QuantumGate, QUANTUM_GATE_COLORS, 
    QUANTUM_GATE_SYMBOLS, GameSettings, MobileColors
)

# Import game logic classes (will be created)
from game_logic import Snake, Food, QuantumGateFood, ParticleSystem, GameLogic

class TouchControlPad(Widget):
    """Touch control pad for mobile controls"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 200)
        self.pos_hint = {'left': 0.05, 'bottom': 0.05}
        
        # Control state
        self.active = False
        self.direction = (0, 0)  # Current direction
        self.base_pos = (0, 0)   # Center position
        
        # Draw control pad
        self.draw_controls()
    
    def draw_controls(self):
        """Draw the control pad"""
        with self.canvas:
            # Background circle
            Color(*MobileColors.SECONDARY_BG)
            self.bg_circle = Ellipse(
                pos=(self.center_x - 80, self.center_y - 80),
                size=(160, 160)
            )
            
            # Direction buttons
            button_size = 50
            button_positions = [
                ('up', (self.center_x - 25, self.center_y + 30)),
                ('down', (self.center_x - 25, self.center_y - 80)),
                ('left', (self.center_x - 80, self.center_y - 25)),
                ('right', (self.center_x + 30, self.center_y - 25))
            ]
            
            self.buttons = {}
            for name, pos in button_positions:
                Color(*MobileColors.ACCENT_CYAN)
                button = Ellipse(
                    pos=pos,
                    size=(button_size, button_size)
                )
                self.buttons[name] = button
                
                # Button label
                Color(*MobileColors.TEXT_WHITE)
                # Labels will be added in update method
    
    def on_touch_down(self, touch):
        """Handle touch down events"""
        if self.collide_point(*touch.pos):
            self.active = True
            self.base_pos = touch.pos
            self.update_direction(touch.pos)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """Handle touch move events"""
        if self.active:
            self.update_direction(touch.pos)
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Handle touch up events"""
        if self.active:
            self.active = False
            self.direction = (0, 0)
            return True
        return super().on_touch_up(touch)
    
    def update_direction(self, touch_pos):
        """Update direction based on touch position"""
        dx = touch_pos[0] - self.center_x
        dy = touch_pos[1] - self.center_y
        
        # Determine direction
        if abs(dx) > abs(dy):
            # Horizontal
            if dx > 20:
                self.direction = (1, 0)  # Right
            elif dx < -20:
                self.direction = (-1, 0)  # Left
            else:
                self.direction = (0, 0)
        else:
            # Vertical
            if dy > 20:
                self.direction = (0, 1)  # Up
            elif dy < -20:
                self.direction = (0, -1)  # Down
            else:
                self.direction = (0, 0)
    
    def get_direction(self):
        """Get current direction"""
        return self.direction

class GameArea(Widget):
    """Main game area where snake game is rendered"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.75)  # 75% of screen height
        self.game_logic = None
        self.grid_size = GameSettings.GRID_SIZE
        
        # Calculate grid dimensions
        self.grid_width = GameSettings.GRID_WIDTH
        self.grid_height = GameSettings.GRID_HEIGHT
        
        # Drawing instructions
        self.canvas_instructions = InstructionGroup()
        
    def set_game_logic(self, game_logic):
        """Set the game logic instance"""
        self.game_logic = game_logic
    
    def draw_grid(self):
        """Draw the game grid"""
        cell_width = self.width / self.grid_width
        cell_height = self.height / self.grid_height
        
        with self.canvas:
            # Draw grid lines
            Color(0.1, 0.1, 0.1, 1)
            
            # Vertical lines
            for x in range(self.grid_width + 1):
                x_pos = self.x + x * cell_width
                Rectangle(
                    pos=(x_pos, self.y),
                    size=(1, self.height)
                )
            
            # Horizontal lines
            for y in range(self.grid_height + 1):
                y_pos = self.y + y * cell_height
                Rectangle(
                    pos=(self.x, y_pos),
                    size=(self.width, 1)
                )
    
    def draw_snake(self, snake):
        """Draw a snake"""
        if not self.game_logic:
            return
            
        cell_width = self.width / self.grid_width
        cell_height = self.height / self.grid_height
        
        with self.canvas:
            # Draw snake body
            for i, segment in enumerate(snake.body):
                x, y = segment
                
                # Calculate screen position
                screen_x = self.x + x * cell_width
                screen_y = self.y + y * cell_height
                
                # Determine color
                if i == 0:  # Head
                    color = snake.color
                else:
                    # Gradient effect
                    gradient_factor = 0.6 + 0.4 * (i / len(snake.body))
                    color = (
                        int(snake.color[0] * gradient_factor),
                        int(snake.color[1] * gradient_factor),
                        int(snake.color[2] * gradient_factor)
                    )
                
                # Draw segment
                Color(*[c/255.0 for c in color])
                Rectangle(
                    pos=(screen_x + 2, screen_y + 2),
                    size=(cell_width - 4, cell_height - 4)
                )
    
    def draw_food(self, food):
        """Draw food or quantum gate"""
        if not self.game_logic:
            return
            
        cell_width = self.width / self.grid_width
        cell_height = self.height / self.grid_height
        
        x, y = food.position
        screen_x = self.x + x * cell_width
        screen_y = self.y + y * cell_height
        
        with self.canvas:
            if hasattr(food, 'gate_type'):  # Quantum gate
                color = QUANTUM_GATE_COLORS.get(food.gate_type, (255, 255, 255))
                Color(*[c/255.0 for c in color])
                
                # Draw gate symbol
                # This is simplified - full implementation would draw proper symbols
                Rectangle(
                    pos=(screen_x + 5, screen_y + 5),
                    size=(cell_width - 10, cell_height - 10)
                )
            else:  # Regular food
                Color(1, 0, 0, 1)  # Red
                Rectangle(
                    pos=(screen_x + 5, screen_y + 5),
                    size=(cell_width - 10, cell_height - 10)
                )
    
    def update_game_area(self):
        """Update the game area drawing"""
        self.canvas.clear()
        
        if self.game_logic:
            self.draw_grid()
            
            # Draw snakes
            for snake in self.game_logic.snakes:
                self.draw_snake(snake)
            
            # Draw food
            self.draw_food(self.game_logic.food)

class GameScreen(Screen):
    """Main game screen"""
    
    current_level = StringProperty('')
    score = NumericProperty(0)
    game_over = BooleanProperty(False)
    paused = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.game_logic = None
        self.game_area = None
        self.control_pad = None
        self.game_clock = None
        self.level_type = LevelType.SEMI_QUANTUM
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface"""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=0,
            spacing=0
        )
        
        # Top UI bar
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            padding=10,
            spacing=10
        )
        
        # Level indicator
        self.level_label = Label(
            text='LEVEL 1',
            font_size=18,
            bold=True,
            color=MobileColors.ACCENT_CYAN,
            size_hint_x=0.3
        )
        
        # Score
        self.score_label = Label(
            text='SCORE: 0',
            font_size=18,
            bold=True,
            color=MobileColors.TEXT_WHITE,
            size_hint_x=0.4,
            halign='center'
        )
        
        # Pause button
        self.pause_button = Button(
            text='⏸',
            font_size=24,
            color=MobileColors.TEXT_WHITE,
            background_color=MobileColors.WARNING_ORANGE,
            background_normal='',
            size_hint_x=0.3,
            on_release=self.on_pause
        )
        
        top_bar.add_widget(self.level_label)
        top_bar.add_widget(self.score_label)
        top_bar.add_widget(self.pause_button)
        
        # Game area
        self.game_area = GameArea()
        
        # Control area
        control_area = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            padding=10
        )
        
        # Touch control pad
        self.control_pad = TouchControlPad()
        
        # Info panel
        info_panel = BoxLayout(
            orientation='vertical',
            spacing=5,
            padding=[10, 0, 10, 0]
        )
        
        self.snake1_label = Label(
            text='Green: 5',
            font_size=14,
            color=(0, 1, 0, 1),
            halign='left'
        )
        
        self.snake2_label = Label(
            text='Blue: 5',
            font_size=14,
            color=(0, 0, 1, 1),
            halign='left'
        )
        
        self.status_label = Label(
            text='Ready to start!',
            font_size=12,
            color=MobileColors.TEXT_GRAY,
            halign='left'
        )
        
        info_panel.add_widget(self.snake1_label)
        info_panel.add_widget(self.snake2_label)
        info_panel.add_widget(self.status_label)
        
        control_area.add_widget(self.control_pad)
        control_area.add_widget(info_panel)
        
        # Add all to main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(self.game_area)
        main_layout.add_widget(control_area)
        
        self.add_widget(main_layout)
    
    def set_level(self, level_type):
        """Set the game level"""
        self.level_type = level_type
        level_names = {
            LevelType.SEMI_QUANTUM: 'SEMI-QUANTUM',
            LevelType.QUANTUM: 'QUANTUM',
            LevelType.SUPER_QUANTUM: 'SUPER-QUANTUM'
        }
        self.level_label.text = level_names.get(level_type, 'UNKNOWN')
    
    def on_enter(self):
        """Called when screen is entered"""
        self.start_game()
    
    def start_game(self):
        """Initialize and start the game"""
        # Create game logic instance
        self.game_logic = GameLogic(self.level_type)
        
        # Connect game area to game logic
        self.game_area.set_game_logic(self.game_logic)
        
        # Start game loop
        self.game_clock = Clock.schedule_interval(
            self.update_game, 
            1.0 / GameSettings.BASE_FPS
        )
        
        self.game_over = False
        self.paused = False
        
        # Initial draw
        self.game_area.update_game_area()
        self.update_ui()
    
    def update_game(self, dt):
        """Main game update loop"""
        if self.game_over or self.paused or not self.game_logic:
            return
        
        # Get input from control pad
        direction = self.control_pad.get_direction()
        if direction != (0, 0):
            self.game_logic.handle_input(direction)
        
        # Update game logic
        self.game_logic.update()
        
        # Update game area
        self.game_area.update_game_area()
        
        # Update UI
        self.update_ui()
        
        # Check game over
        if self.game_logic.check_game_over():
            self.on_game_over()
    
    def update_ui(self):
        """Update UI elements"""
        if not self.game_logic:
            return
        
        # Update score
        self.score = self.game_logic.get_score()
        self.score_label.text = f'SCORE: {self.score}'
        
        # Update snake lengths
        if len(self.game_logic.snakes) >= 2:
            self.snake1_label.text = f'Green: {len(self.game_logic.snakes[0].body)}'
            self.snake2_label.text = f'Blue: {len(self.game_logic.snakes[1].body)}'
        
        # Update status
        if self.level_type == LevelType.QUANTUM:
            # Show hunger status
            status = "HUNGRY!" if self.game_logic.snakes[0].is_starving else "OK"
            self.status_label.text = f'Hunger: {status}'
        elif self.level_type == LevelType.SUPER_QUANTUM:
            # Show current quantum gate
            if hasattr(self.game_logic.food, 'gate_type'):
                gate = self.game_logic.food.gate_type
                self.status_label.text = f'Gate: {gate.replace("_", " ").upper()}'
    
    def on_pause(self, instance):
        """Handle pause button"""
        if self.app:
            self.app.vibrate(0.05)
        
        self.paused = not self.paused
        instance.text = '▶' if self.paused else '⏸'
        
        if self.paused:
            self.status_label.text = 'PAUSED'
        else:
            self.status_label.text = 'Resumed'
    
    def on_game_over(self):
        """Handle game over"""
        self.game_over = True
        self.game_clock.cancel()
        
        if self.app:
            self.app.vibrate(0.2)
        
        # Show game over screen
        self.show_game_over_dialog()
    
    def show_game_over_dialog(self):
        """Show game over dialog"""
        # This would be implemented with a proper popup in the full version
        self.status_label.text = f'GAME OVER! Score: {self.score}'
        self.status_label.color = MobileColors.ERROR_RED
        
        # Auto-return to menu after 3 seconds
        Clock.schedule_once(
            lambda dt: self.change_screen(ScreenNames.MENU, 'right'),
            3
        )
    
    def change_screen(self, screen_name, direction='left'):
        """Change to different screen"""
        if self.app:
            # Stop game before changing screen
            if self.game_clock:
                self.game_clock.cancel()
            self.app.change_screen(screen_name, direction)
    
    def on_leave(self):
        """Called when screen is left"""
        # Clean up game
        if self.game_clock:
            self.game_clock.cancel()
        self.game_logic = None