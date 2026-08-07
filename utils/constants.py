"""
Game constants and configurations
"""

# Game States
class GameState:
    MAIN_MENU = "main_menu"
    LEVEL_SELECT = "level_select"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# Level Types
class LevelType:
    SEMI_QUANTUM = "semi_quantum"    # Level 1
    QUANTUM = "quantum"              # Level 2  
    SUPER_QUANTUM = "super_quantum"  # Level 3

# Quantum Gate Types
class QuantumGate:
    HADAMARD = "hadamard"      # Randomly reverses controls when changing direction
    PAULI_X = "pauli_x"        # Reverses controls
    PAULI_Y = "pauli_y"        # Swaps snake colors/behavior
    PAULI_Z = "pauli_z"        # Inverts growth/shrink
    CNOT = "cnot"              # Links snakes movement
    SWAP = "swap"              # Swaps positions
    TELEPORT = "teleport"      # Teleports both snakes randomly

# Colors (RGB)
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)
    YELLOW = (255, 255, 0)
    GRAY = (100, 100, 100)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)
    DARK_GREEN = (0, 150, 0)
    DARK_BLUE = (0, 0, 150)
    DARK_RED = (150, 0, 0)
    LIGHT_GREEN = (100, 255, 100)
    LIGHT_BLUE = (100, 100, 255)
    PINK = (255, 105, 180)
    TEAL = (0, 128, 128)
    DARK_YELLOW = (200, 200, 0)

# Mobile-specific Colors (for Kivy)
class MobileColors:
    PRIMARY_BG = (0.1, 0.1, 0.18, 1)  # Dark blue
    SECONDARY_BG = (0.15, 0.15, 0.25, 1)
    ACCENT_CYAN = (0, 0.83, 1, 1)
    ACCENT_PURPLE = (0.55, 0.36, 0.96, 1)
    TEXT_WHITE = (1, 1, 1, 1)
    TEXT_GRAY = (0.7, 0.7, 0.7, 1)
    SUCCESS_GREEN = (0.06, 0.72, 0.51, 1)
    WARNING_ORANGE = (0.96, 0.62, 0.04, 1)
    ERROR_RED = (0.94, 0.27, 0.27, 1)

# Game Settings
class GameSettings:
    # Grid dimensions (adapted for mobile)
    GRID_SIZE = 20
    GRID_WIDTH = 18  # Reduced for mobile screens
    GRID_HEIGHT = 24  # Adjusted for mobile aspect ratio
    
    # Game speeds (affected by settings)
    BASE_FPS = 60
    GAME_SPEEDS = {
        LevelType.SEMI_QUANTUM: 10,
        LevelType.QUANTUM: 10,
        LevelType.SUPER_QUANTUM: 12
    }
    
    # Touch control settings
    MIN_TOUCH_TARGET = 60  # Minimum touch target size in pixels
    CONTROL_PADDING = 20   # Padding around controls
    
    # Snake settings
    INITIAL_SNAKE_LENGTH = 5
    GROWTH_RATE = {
        LevelType.SEMI_QUANTUM: 3,
        LevelType.QUANTUM: 1,
        LevelType.SUPER_QUANTUM: 3
    }
    
    # Quantum effects
    EFFECT_DURATION = 25  # Frames
    STARVATION_TIME = 30  # Frames before starvation
    
    # UI Settings
    SCORE_FONT_SIZE = 24
    UI_FONT_SIZE = 18
    BUTTON_RADIUS = 10
    
    # Audio settings
    DEFAULT_SOUND_VOLUME = 0.7
    DEFAULT_MUSIC_VOLUME = 0.5

# Screen Names
class ScreenNames:
    MENU = 'menu'
    LEVEL_SELECT = 'level_select'
    GAME = 'game'
    SETTINGS = 'settings'

# Quantum Gate Colors
QUANTUM_GATE_COLORS = {
    QuantumGate.HADAMARD: Colors.GREEN,
    QuantumGate.PAULI_X: Colors.RED,
    QuantumGate.PAULI_Y: Colors.YELLOW,
    QuantumGate.PAULI_Z: Colors.BLUE,
    QuantumGate.CNOT: Colors.PURPLE,
    QuantumGate.SWAP: Colors.ORANGE,
    QuantumGate.TELEPORT: Colors.CYAN
}

# Quantum Gate Symbols
QUANTUM_GATE_SYMBOLS = {
    QuantumGate.HADAMARD: "H",
    QuantumGate.PAULI_X: "X",
    QuantumGate.PAULI_Y: "Y",
    QuantumGate.PAULI_Z: "Z",
    QuantumGate.CNOT: "⊕",
    QuantumGate.SWAP: "⇄",
    QuantumGate.TELEPORT: "⤴"
}

# Level Descriptions
LEVEL_DESCRIPTIONS = {
    LevelType.SEMI_QUANTUM: {
        "title": "LEVEL 1: SEMI-QUANTUM",
        "description": "Both snakes grow when eating\nClassic mirror movement",
        "color": MobileColors.SUCCESS_GREEN
    },
    LevelType.QUANTUM: {
        "title": "LEVEL 2: QUANTUM",
        "description": "Eating grows your snake\nStarvation kills!",
        "color": MobileColors.ACCENT_CYAN
    },
    LevelType.SUPER_QUANTUM: {
        "title": "LEVEL 3: SUPER-QUANTUM",
        "description": "Quantum gates with TELEPORT\nHadamard reverses controls",
        "color": MobileColors.ACCENT_PURPLE
    }
}

# File Paths
class FilePaths:
    SETTINGS_FILE = "quantum_snake_settings.json"
    HIGH_SCORES_FILE = "quantum_snake_scores.json"