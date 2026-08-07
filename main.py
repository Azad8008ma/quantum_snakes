"""
Quantum Snake Mobile - Main Application
A mobile adaptation of the Quantum Snake game with touch controls and modern UI
"""

from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
import json
import os

# Configure Kivy for mobile
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Import screens (will be created next)
from menu_screen import MenuScreen
from game_screen import GameScreen
from settings_screen import SettingsScreen
from level_select_screen import LevelSelectScreen

class QuantumSnakeApp(App):
    """Main application class"""
    
    # App properties
    version = StringProperty("1.0.0")
    
    # Settings properties
    sound_volume = NumericProperty(0.7)
    music_volume = NumericProperty(0.5)
    vibration_enabled = BooleanProperty(True)
    game_speed = NumericProperty(1.0)
    control_sensitivity = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings_file = os.path.join(os.path.expanduser("~"), ".quantum_snake_settings.json")
        self.load_settings()
        
    def build(self):
        """Build the application UI"""
        # Create screen manager
        self.screen_manager = ScreenManager(transition=SlideTransition())
        
        # Add screens
        self.screen_manager.add_widget(MenuScreen(name='menu'))
        self.screen_manager.add_widget(LevelSelectScreen(name='level_select'))
        self.screen_manager.add_widget(GameScreen(name='game'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        
        # Bind settings to screens
        self.bind_settings()
        
        return self.screen_manager
    
    def load_settings(self):
        """Load saved settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    
                self.sound_volume = settings.get('sound_volume', 0.7)
                self.music_volume = settings.get('music_volume', 0.5)
                self.vibration_enabled = settings.get('vibration_enabled', True)
                self.game_speed = settings.get('game_speed', 1.0)
                self.control_sensitivity = settings.get('control_sensitivity', 1.0)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'sound_volume': self.sound_volume,
                'music_volume': self.music_volume,
                'vibration_enabled': self.vibration_enabled,
                'game_speed': self.game_speed,
                'control_sensitivity': self.control_sensitivity
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def bind_settings(self):
        """Bind settings to all screens"""
        for screen in self.screen_manager.screens:
            screen.app = self
            
    def change_screen(self, screen_name, direction='left'):
        """Change to a different screen"""
        self.screen_manager.transition.direction = direction
        self.screen_manager.current = screen_name
    
    def on_stop(self):
        """Called when app is closing"""
        self.save_settings()
        
    def vibrate(self, duration=0.1):
        """Trigger vibration if enabled"""
        if self.vibration_enabled:
            try:
                from kivy.utils import platform
                if platform == 'android':
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    activity = PythonActivity.mActivity
                    vibrator = activity.getSystemService(activity.VIBRATOR_SERVICE)
                    if vibrator.hasVibrator():
                        vibrator.vibrate(int(duration * 1000))
            except:
                pass

if __name__ == '__main__':
    QuantumSnakeApp().run()