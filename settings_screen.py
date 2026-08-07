"""
Settings Screen for Quantum Snake Mobile
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock
from utils.constants import ScreenNames, MobileColors, GameSettings

class SettingRow(BoxLayout):
    """A single setting row with label and control"""
    
    def __init__(self, title, description="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.padding = [0, 10, 0, 10]
        self.size_hint_y = None
        self.height = 80
        
        # Label container
        label_container = BoxLayout(
            orientation='vertical',
            size_hint_x=0.6,
            spacing=2
        )
        
        # Title label
        self.title_label = Label(
            text=title,
            font_size=18,
            color=MobileColors.TEXT_WHITE,
            size_hint_y=0.6,
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        
        # Description label
        if description:
            self.desc_label = Label(
                text=description,
                font_size=12,
                color=MobileColors.TEXT_GRAY,
                size_hint_y=0.4,
                halign='left',
                valign='middle'
            )
            self.desc_label.bind(size=self.desc_label.setter('text_size'))
        
        label_container.add_widget(self.title_label)
        if description:
            label_container.add_widget(self.desc_label)
        
        # Control container
        control_container = BoxLayout(
            size_hint_x=0.4,
            padding=[10, 0, 10, 0]
        )
        
        self.add_widget(label_container)
        self.add_widget(control_container)

class VolumeSlider(Slider):
    """Custom volume slider"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 1
        self.step = 0.1
        self.value_track = True
        self.value_track_color = MobileColors.ACCENT_CYAN
        self.cursor_size = (30, 30)
        self.background_width = 30

class SettingsToggle(ToggleButton):
    """Custom toggle button for settings"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = MobileColors.SECONDARY_BG
        self.background_normal = ''
        self.background_down = ''
        self.color = MobileColors.TEXT_WHITE
        self.font_size = 16
        self.size_hint = (None, None)
        self.size = (80, 40)
        
    def on_state(self, instance, value):
        """Update color based on state"""
        if value == 'down':
            self.background_color = MobileColors.SUCCESS_GREEN
        else:
            self.background_color = MobileColors.ERROR_RED

class SettingsScreen(Screen):
    """Settings screen with all game options"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.original_settings = {}
        self.build_ui()
    
    def build_ui(self):
        """Build the user interface"""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10
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
            text='SETTINGS',
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
        
        # Scrollable content
        scroll_view = ScrollView(
            size_hint_y=0.8,
            bar_width=10,
            bar_color=MobileColors.ACCENT_CYAN,
            bar_inactive_color=MobileColors.SECONDARY_BG
        )
        
        # Settings container
        settings_container = GridLayout(
            cols=1,
            spacing=15,
            padding=[0, 20, 0, 20],
            size_hint_y=None
        )
        settings_container.bind(minimum_height=settings_container.setter('height'))
        
        # Sound Effects Volume
        sound_row = SettingRow(
            title='Sound Effects',
            description='Volume of game sounds and effects'
        )
        self.sound_slider = VolumeSlider(
            value=GameSettings.DEFAULT_SOUND_VOLUME
        )
        sound_row.children[1].add_widget(self.sound_slider)
        settings_container.add_widget(sound_row)
        
        # Music Volume
        music_row = SettingRow(
            title='Background Music',
            description='Volume of background music'
        )
        self.music_slider = VolumeSlider(
            value=GameSettings.DEFAULT_MUSIC_VOLUME
        )
        music_row.children[1].add_widget(self.music_slider)
        settings_container.add_widget(music_row)
        
        # Vibration
        vibration_row = SettingRow(
            title='Vibration',
            description='Enable haptic feedback'
        )
        self.vibration_toggle = SettingsToggle(
            text='ON',
            state='down'
        )
        vibration_row.children[1].add_widget(self.vibration_toggle)
        settings_container.add_widget(vibration_row)
        
        # Game Speed
        speed_row = SettingRow(
            title='Game Speed',
            description='Adjust overall game speed'
        )
        self.speed_slider = VolumeSlider(
            value=1.0,
            min=0.5,
            max=2.0,
            step=0.1
        )
        speed_row.children[1].add_widget(self.speed_slider)
        settings_container.add_widget(speed_row)
        
        # Control Sensitivity
        sensitivity_row = SettingRow(
            title='Control Sensitivity',
            description='How responsive the controls are'
        )
        self.sensitivity_slider = VolumeSlider(
            value=1.0,
            min=0.5,
            max=2.0,
            step=0.1
        )
        sensitivity_row.children[1].add_widget(self.sensitivity_slider)
        settings_container.add_widget(sensitivity_row)
        
        # Reset button
        reset_button = Button(
            text='RESET TO DEFAULTS',
            font_size=18,
            color=MobileColors.TEXT_WHITE,
            background_color=MobileColors.WARNING_ORANGE,
            background_normal='',
            size_hint_y=None,
            height=50,
            on_release=self.on_reset_defaults
        )
        settings_container.add_widget(reset_button)
        
        scroll_view.add_widget(settings_container)
        
        # Action buttons
        action_buttons = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=0.1
        )
        
        cancel_button = Button(
            text='CANCEL',
            font_size=18,
            color=MobileColors.TEXT_WHITE,
            background_color=MobileColors.ERROR_RED,
            background_normal='',
            on_release=self.on_cancel
        )
        
        save_button = Button(
            text='SAVE',
            font_size=18,
            color=MobileColors.TEXT_WHITE,
            background_color=MobileColors.SUCCESS_GREEN,
            background_normal='',
            on_release=self.on_save
        )
        
        action_buttons.add_widget(cancel_button)
        action_buttons.add_widget(save_button)
        
        # Add all to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(action_buttons)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        """Called when screen is entered"""
        self.load_current_settings()
        self.save_original_settings()
    
    def load_current_settings(self):
        """Load current app settings into UI"""
        if self.app:
            self.sound_slider.value = self.app.sound_volume
            self.music_slider.value = self.app.music_volume
            self.vibration_toggle.state = 'down' if self.app.vibration_enabled else 'normal'
            self.speed_slider.value = self.app.game_speed
            self.sensitivity_slider.value = self.app.control_sensitivity
    
    def save_original_settings(self):
        """Save original settings for cancel functionality"""
        if self.app:
            self.original_settings = {
                'sound_volume': self.app.sound_volume,
                'music_volume': self.app.music_volume,
                'vibration_enabled': self.app.vibration_enabled,
                'game_speed': self.app.game_speed,
                'control_sensitivity': self.app.control_sensitivity
            }
    
    def on_back(self, instance):
        """Handle back button"""
        self.animate_button_press(instance)
        Clock.schedule_once(lambda dt: self.change_screen(ScreenNames.MENU, 'right'), 0.2)
    
    def on_save(self, instance):
        """Save settings"""
        self.animate_button_press(instance)
        
        if self.app:
            self.app.sound_volume = self.sound_slider.value
            self.app.music_volume = self.music_slider.value
            self.app.vibration_enabled = self.vibration_toggle.state == 'down'
            self.app.game_speed = self.speed_slider.value
            self.app.control_sensitivity = self.sensitivity_slider.value
            
            self.app.save_settings()
            
            # Vibrate to confirm save
            self.app.vibrate(0.1)
        
        Clock.schedule_once(lambda dt: self.change_screen(ScreenNames.MENU, 'right'), 0.2)
    
    def on_cancel(self, instance):
        """Cancel and restore original settings"""
        self.animate_button_press(instance)
        
        if self.app and self.original_settings:
            # Restore original settings
            for key, value in self.original_settings.items():
                setattr(self.app, key, value)
        
        Clock.schedule_once(lambda dt: self.change_screen(ScreenNames.MENU, 'right'), 0.2)
    
    def on_reset_defaults(self, instance):
        """Reset to default settings"""
        self.animate_button_press(instance)
        
        # Reset sliders to default values
        self.sound_slider.value = GameSettings.DEFAULT_SOUND_VOLUME
        self.music_slider.value = GameSettings.DEFAULT_MUSIC_VOLUME
        self.vibration_toggle.state = 'down'
        self.speed_slider.value = 1.0
        self.sensitivity_slider.value = 1.0
        
        if self.app:
            self.app.vibrate(0.05)
    
    def animate_button_press(self, button):
        """Animate button press effect"""
        original_scale = button.size_hint_x if button.size_hint_x else 1
        
        anim = Animation(size_hint_x=original_scale * 0.95, duration=0.1) + \
               Animation(size_hint_x=original_scale, duration=0.1)
        anim.start(button)
    
    def change_screen(self, screen_name, direction='left'):
        """Change to different screen"""
        if self.app:
            self.app.change_screen(screen_name, direction)
    
    def on_vibration_toggle(self, instance, value):
        """Update toggle button text"""
        instance.text = 'ON' if value == 'down' else 'OFF'
        
        # Vibrate on toggle if enabled
        if self.app and self.app.vibration_enabled and value == 'down':
            self.app.vibrate(0.05)