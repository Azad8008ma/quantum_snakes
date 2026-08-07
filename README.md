# Quantum Snake Mobile

A mobile adaptation of the Quantum Snake game with touch controls, modern UI, and all the quantum mechanics from the original desktop version.

## Features

### 🎮 Three Game Levels
- **Level 1 - Semi-Quantum**: Classic mirror movement, both snakes grow when eating
- **Level 2 - Quantum**: Eating grows your snake and shrinks the opponent. Starvation kills!
- **Level 3 - Super-Quantum**: Quantum gates with TELEPORT, Hadamard randomly reverses controls

### 🎯 Quantum Mechanics
- **Hadamard Gate**: Randomly reverses controls when changing direction
- **Pauli X Gate**: Reverses controls completely
- **Pauli Y Gate**: Temporarily swaps snake colors/behavior
- **Pauli Z Gate**: Inverts growth/shrink mechanics
- **CNOT Gate**: Links snake movements
- **SWAP Gate**: Instantly swaps snake positions
- **TELEPORT Gate**: Teleports both snakes to random positions

### 📱 Mobile-Optimized Controls
- Large touch control pad with directional buttons
- Responsive touch feedback
- Haptic feedback (vibration) support
- Optimized for portrait and landscape modes

### 🎨 Modern UI
- Material Design-inspired interface
- Smooth animations and transitions
- Particle effects for visual feedback
- Dark theme with quantum-inspired colors

### 🔊 Audio System
- Background music
- Sound effects for all game actions
- Volume controls in settings
- Vibration feedback

### ⚙️ Customizable Settings
- Sound effects volume
- Background music volume
- Vibration toggle
- Game speed adjustment
- Control sensitivity

## Installation

### On Desktop (for testing)

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

### On Android

1. Install Buildozer:
   ```bash
   pip install buildozer
   ```
2. Navigate to project directory
3. Initialize buildozer:
   ```bash
   buildozer init
   ```
4. Build APK:
   ```bash
   buildozer -v android debug
   ```
5. Install on device:
   ```bash
   buildozer android deploy run
   ```

## How to Play

### Controls
- Use the directional pad in the bottom-left corner to control the green snake
- The blue snake moves in the opposite direction (quantum mirror effect)
- Press the pause button to pause/resume the game

### Objective
- Eat food (or quantum gates in Level 3) to grow your snake
- Avoid collisions with walls, yourself, or the other snake
- In Level 2, avoid starvation by eating regularly
- In Level 3, use quantum gates to your advantage

### Scoring
- **Level 1**: +1 point per food, both snakes grow by 3 segments
- **Level 2**: +1 point per food, your snake grows by 1, opponent shrinks by 1
- **Level 3**: +1 point per quantum gate, both snakes grow by 3 segments

## Game Mechanics

### Quantum Effects
Different quantum gates apply different effects when collected:

- **H (Hadamard)**: 50% chance to reverse your next direction change
- **X (Pauli-X)**: Reverses your controls for 5 seconds
- **Y (Pauli-Y)**: Swaps snake colors temporarily
- **Z (Pauli-Z)**: Inverts growth mechanics
- **⊕ (CNOT)**: Links your movement to the other snake
- **⇄ (SWAP)**: Instantly swaps snake positions
- **⤴ (TELEPORT)**: Teleports both snakes to random safe locations

### Starvation System (Level 2)
- If you don't eat, a starvation timer increases
- After 6 seconds of not eating, you start shrinking
- If your snake shrinks to 1 segment, you die

### Mirror Movement
- Both snakes are controlled simultaneously
- Green snake follows your input direction
- Blue snake moves in the opposite direction
- This creates interesting strategic situations

## Development

### Project Structure
```
quantum_snake_mobile/
├── main.py                 # Main application entry point
├── menu_screen.py          # Main menu screen
├── game_screen.py          # Game screen with touch controls
├── settings_screen.py      # Settings screen
├── level_select_screen.py  # Level selection screen
├── game_logic.py           # Core game logic
├── utils/
│   ├── constants.py        # Game constants and configurations
│   └── helpers.py          # Utility functions (future)
├── resources/              # Game assets
│   ├── sounds/            # Audio files
│   ├── fonts/             # Custom fonts
│   └── images/            # UI images
└── requirements.txt        # Python dependencies
```

### Key Classes

- **QuantumSnakeApp**: Main application class
- **MenuScreen**: Main menu with animated background
- **GameScreen**: Main game screen with touch controls
- **SettingsScreen**: Settings and configuration
- **LevelSelectScreen**: Level selection interface
- **GameLogic**: Core game mechanics
- **Snake**: Individual snake objects
- **Food/QuantumGateFood**: Food objects
- **ParticleSystem**: Visual effects

### Customization

#### Adding New Quantum Gates
1. Add gate type to `QuantumGate` class in `constants.py`
2. Add color to `QUANTUM_GATE_COLORS`
3. Add symbol to `QUANTUM_GATE_SYMBOLS`
4. Implement effect in `apply_quantum_gate_effect` method

#### Modifying Controls
Edit the `TouchControlPad` class in `game_screen.py` to change:
- Control layout
- Touch sensitivity
- Visual appearance
- Button mapping

#### Changing Game Balance
Modify values in `GameSettings` class:
- Growth rates
- Effect durations
- Starvation timing
- Grid dimensions

## Technical Details

### Framework
- **Kivy**: Cross-platform UI framework
- **KivyMD**: Material Design components
- **Python 3.8+**: Core language

### Performance Optimizations
- Efficient particle system
- Optimized rendering loops
- Memory-conscious design
- Battery-friendly animations

### Mobile Features
- Touch-optimized controls (minimum 60px touch targets)
- Haptic feedback
- Responsive design
- Safe area handling for notches

## Troubleshooting

### Common Issues

**Game runs slowly:**
- Reduce particle count in settings
- Lower game speed setting
- Close other apps

**Touch controls not responsive:**
- Increase control sensitivity in settings
- Check for screen protector interference
- Clean screen surface

**No sound:**
- Check volume settings in-game and device
- Verify audio files are present
- Restart the app

### Debug Mode
Add this to the beginning of `main.py` for debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- Multiplayer mode via Bluetooth/WiFi
- New quantum gates and effects
- Power-ups and special abilities
- Custom level editor
- Achievement system
- Leaderboards
- Different snake skins
- Background themes

## License

This project is created as a mobile adaptation of the Quantum Snake game. All quantum mechanics and game concepts are preserved from the original version.

## Credits

- Original game concept and mechanics
- Quantum physics inspiration
- Kivy framework for mobile development
- Material Design for UI inspiration

---

**Enjoy playing Quantum Snake Mobile!** 🐍⚛️📱