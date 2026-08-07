"""
Game Logic for Quantum Snake Mobile
Adapted from the original pygame version
"""

import random
import math
from utils.constants import (
    LevelType, QuantumGate, GameSettings, 
    QUANTUM_GATE_COLORS, QUANTUM_GATE_SYMBOLS
)

class Particle:
    """Individual particle for visual effects"""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = random.randint(20, 40)
    
    def update(self):
        """Update particle position and life"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size *= 0.95
    
    def is_dead(self):
        """Check if particle is dead"""
        return self.life <= 0

class ParticleSystem:
    """System for managing particles"""
    
    def __init__(self):
        self.particles = []
    
    def add_particles(self, x, y, color, count=10):
        """Add multiple particles"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)
    
    def get_particles(self):
        """Get all active particles"""
        return self.particles

class Snake:
    """Snake game object"""
    
    def __init__(self, start_pos, color, name):
        self.body = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.color = color
        self.name = name
        self.original_color = color
        self.control_reversed = False
        self.quantum_effect = None
        self.effect_timer = 0
        self.grow_pending = 0
        self.shrink_pending = 0
        self.starvation_timer = 0
        self.is_starving = False
        self.hadamard_active = False
        self.particles = ParticleSystem()
        
        # Initialize with 5 segments
        self.reset(start_pos)
    
    def reset(self, start_pos):
        """Reset snake to initial state"""
        self.body = []
        for i in range(GameSettings.INITIAL_SNAKE_LENGTH):
            segment_x = (start_pos[0] - i) % GameSettings.GRID_WIDTH
            segment_y = start_pos[1]
            self.body.append((segment_x, segment_y))
        
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.control_reversed = False
        self.quantum_effect = None
        self.effect_timer = 0
        self.grow_pending = 0
        self.shrink_pending = 0
        self.starvation_timer = 0
        self.is_starving = False
        self.hadamard_active = False
        self.color = self.original_color
        self.particles = ParticleSystem()
    
    def move(self, level_type, other_snake=None):
        """Move the snake"""
        self.direction = self.next_direction
        
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        
        # Handle starvation in Level 2
        if level_type == LevelType.QUANTUM:
            if self.shrink_pending == 0 and not self.grow_pending:
                self.starvation_timer += 1
                if self.starvation_timer >= GameSettings.STARVATION_TIME:
                    self.is_starving = True
                    if self.starvation_timer % 10 == 0 and len(self.body) > 1:
                        self.shrink_pending += 1
            else:
                self.starvation_timer = 0
                self.is_starving = False
        
        # Apply quantum effects
        if self.quantum_effect and self.effect_timer > 0:
            if self.quantum_effect == QuantumGate.PAULI_X:
                dx, dy = -dx, -dy
            elif self.quantum_effect == QuantumGate.CNOT and other_snake:
                other_dx, other_dy = other_snake.direction
                if (other_dx, other_dy) != (-dx, -dy):
                    dx, dy = other_dx, other_dy
            self.effect_timer -= 1
            if self.effect_timer <= 0:
                self.quantum_effect = None
                self.hadamard_active = False
        
        # Apply control reversal
        if self.control_reversed:
            dx, dy = -dx, -dy
        
        # Prevent 180-degree turns in Super Quantum level
        if level_type == LevelType.SUPER_QUANTUM:
            if (dx, dy) == (-self.direction[0], -self.direction[1]):
                dx, dy = self.direction
        
        # Calculate new head position
        new_head = ((head_x + dx) % GameSettings.GRID_WIDTH, 
                   (head_y + dy) % GameSettings.GRID_HEIGHT)
        self.body.insert(0, new_head)
        
        # Handle growth and shrinkage
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            if self.shrink_pending > 0 and len(self.body) > 1:
                self.body.pop()
                self.shrink_pending -= 1
            elif len(self.body) > 1:
                self.body.pop()
        
        # Update particles
        self.particles.update()
    
    def change_direction(self, new_direction):
        """Change snake direction"""
        if self.hadamard_active and self.effect_timer > 0:
            if random.random() < 0.5:
                reversed_dir = (-new_direction[0], -new_direction[1])
                if reversed_dir != (-self.direction[0], -self.direction[1]):
                    new_direction = reversed_dir
            self.effect_timer -= 5
            if self.effect_timer <= 0:
                self.quantum_effect = None
                self.hadamard_active = False
        
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def check_collision_with_self(self):
        """Check if snake collided with itself"""
        return self.body[0] in self.body[1:]
    
    def check_collision_with_other(self, other_snake):
        """Check if snake collided with other snake"""
        return self.body[0] in other_snake.body
    
    def grow(self, amount):
        """Make snake grow"""
        self.grow_pending += amount
    
    def shrink(self, amount):
        """Make snake shrink"""
        self.shrink_pending += amount

class Food:
    """Food game object for Levels 1 and 2"""
    
    def __init__(self):
        self.position = self.randomize_position()
        self.food_count = 0
        self.particles = ParticleSystem()
        self.pulse = 0
    
    def randomize_position(self):
        """Get random position"""
        return (random.randint(0, GameSettings.GRID_WIDTH - 1),
                random.randint(0, GameSettings.GRID_HEIGHT - 1))
    
    def reset(self):
        """Reset food position"""
        self.position = self.randomize_position()
        self.food_count = 0
        self.pulse = 0
    
    def update(self):
        """Update food animation"""
        self.pulse = (self.pulse + 0.1) % (2 * math.pi)
        self.particles.update()

class QuantumGateFood:
    """Quantum gate food for Level 3"""
    
    def __init__(self):
        self.position = self.randomize_position()
        self.gate_type = random.choice([
            QuantumGate.HADAMARD,
            QuantumGate.PAULI_X,
            QuantumGate.PAULI_Y,
            QuantumGate.PAULI_Z,
            QuantumGate.CNOT,
            QuantumGate.SWAP,
            QuantumGate.TELEPORT
        ])
        self.color = QUANTUM_GATE_COLORS.get(self.gate_type, (255, 255, 255))
        self.particles = ParticleSystem()
        self.rotation = 0
        self.pulse = 0
    
    def randomize_position(self):
        """Get random position"""
        return (random.randint(0, GameSettings.GRID_WIDTH - 1),
                random.randint(0, GameSettings.GRID_HEIGHT - 1))
    
    def reset(self):
        """Reset quantum gate"""
        self.position = self.randomize_position()
        self.gate_type = random.choice([
            QuantumGate.HADAMARD,
            QuantumGate.PAULI_X,
            QuantumGate.PAULI_Y,
            QuantumGate.PAULI_Z,
            QuantumGate.CNOT,
            QuantumGate.SWAP,
            QuantumGate.TELEPORT
        ])
        self.color = QUANTUM_GATE_COLORS.get(self.gate_type, (255, 255, 255))
        self.rotation = 0
        self.pulse = 0
    
    def update(self):
        """Update quantum gate animation"""
        self.rotation += 2
        self.pulse = (self.pulse + 0.15) % (2 * math.pi)
        self.particles.update()

class GameLogic:
    """Main game logic controller"""
    
    def __init__(self, level_type):
        self.level_type = level_type
        self.snakes = []
        self.food = None
        self.score = 0
        self.game_over = False
        self.effect_particles = ParticleSystem()
        
        # Initialize game
        self.initialize_game()
    
    def initialize_game(self):
        """Initialize game state"""
        # Create snakes
        snake1 = Snake(
            (10, GameSettings.GRID_HEIGHT // 2),
            (0, 255, 0),  # Green
            "GREEN"
        )
        
        snake2 = Snake(
            (GameSettings.GRID_WIDTH - 10, GameSettings.GRID_HEIGHT // 2),
            (0, 0, 255),  # Blue
            "BLUE"
        )
        
        self.snakes = [snake1, snake2]
        
        # Create food based on level
        if self.level_type == LevelType.SUPER_QUANTUM:
            self.food = QuantumGateFood()
        else:
            self.food = Food()
    
    def handle_input(self, direction):
        """Handle player input"""
        if len(self.snakes) >= 2:
            # Mirror movement: green snake follows input, blue snake moves opposite
            self.snakes[0].change_direction(direction)
            
            # Blue snake moves in opposite direction (quantum mirror effect)
            opposite_direction = (-direction[0], -direction[1])
            self.snakes[1].change_direction(opposite_direction)
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Move snakes
        if len(self.snakes) >= 2:
            self.snakes[0].move(self.level_type, self.snakes[1])
            self.snakes[1].move(self.level_type, self.snakes[0])
        
        # Update food
        if hasattr(self.food, 'update'):
            self.food.update()
        
        # Check food collisions
        self.check_food_collisions()
        
        # Update effect particles
        self.effect_particles.update()
    
    def check_food_collisions(self):
        """Check if snakes collided with food"""
        if len(self.snakes) < 2:
            return
        
        food_eaten = False
        
        for i, snake in enumerate(self.snakes):
            if snake.body[0] == self.food.position:
                food_eaten = True
                other_snake = self.snakes[1 - i]
                
                # Handle based on level type
                if self.level_type == LevelType.SUPER_QUANTUM:
                    # Level 3: Apply quantum gate effects
                    self.apply_quantum_gate_effect(
                        self.food.gate_type, snake, other_snake
                    )
                    snake.grow(3)
                    other_snake.grow(3)
                else:
                    # Levels 1 and 2: Regular food
                    self.food.food_count += 1
                    
                    if self.level_type == LevelType.SEMI_QUANTUM:
                        # Level 1: Both snakes grow
                        self.score += 1
                        snake.grow(3)
                        other_snake.grow(3)
                    elif self.level_type == LevelType.QUANTUM:
                        # Level 2: One grows, other shrinks
                        self.score += 1
                        snake.grow(1)
                        other_snake.shrink(1)
                
                # Create explosion effect
                self.effect_particles.add_particles(
                    self.food.position[0] * 20 + 10,
                    self.food.position[1] * 20 + 10,
                    self.food.color if hasattr(self.food, 'color') else (255, 0, 0),
                    20
                )
                
                # Reset food
                self.food.reset()
                
                # Ensure food doesn't spawn on snakes
                while self.food.position in snake.body or self.food.position in other_snake.body:
                    self.food.reset()
                
                break
    
    def apply_quantum_gate_effect(self, gate_type, snake, other_snake):
        """Apply quantum gate effects for Level 3"""
        if gate_type == QuantumGate.HADAMARD:
            snake.quantum_effect = QuantumGate.HADAMARD
            snake.effect_timer = GameSettings.EFFECT_DURATION
            snake.hadamard_active = True
        elif gate_type == QuantumGate.PAULI_X:
            snake.quantum_effect = QuantumGate.PAULI_X
            snake.effect_timer = GameSettings.EFFECT_DURATION
        elif gate_type == QuantumGate.PAULI_Y:
            snake.color, other_snake.color = other_snake.color, snake.color
            snake.quantum_effect = QuantumGate.PAULI_Y
            snake.effect_timer = GameSettings.EFFECT_DURATION
        elif gate_type == QuantumGate.PAULI_Z:
            snake.quantum_effect = QuantumGate.PAULI_Z
            snake.effect_timer = GameSettings.EFFECT_DURATION
        elif gate_type == QuantumGate.CNOT:
            snake.quantum_effect = QuantumGate.CNOT
            snake.effect_timer = GameSettings.EFFECT_DURATION
        elif gate_type == QuantumGate.SWAP:
            if len(snake.body) > 0 and len(other_snake.body) > 0:
                old_head1 = snake.body[0]
                old_head2 = other_snake.body[0]
                
                if (old_head2 not in snake.body[1:] and 
                    old_head1 not in other_snake.body[1:]):
                    snake.body[0], other_snake.body[0] = old_head2, old_head1
        elif gate_type == QuantumGate.TELEPORT:
            self.teleport_both_snakes(snake, other_snake)
    
    def teleport_both_snakes(self, snake1, snake2):
        """Teleport both snakes to random positions"""
        all_positions = [(x, y) for x in range(GameSettings.GRID_WIDTH) 
                        for y in range(GameSettings.GRID_HEIGHT)]
        
        snake1_positions = set(snake1.body)
        snake2_positions = set(snake2.body)
        occupied = snake1_positions.union(snake2_positions)
        
        available_positions = [pos for pos in all_positions if pos not in occupied]
        
        if len(available_positions) >= 2:
            new_pos1 = random.choice(available_positions)
            available_positions.remove(new_pos1)
            new_pos2 = random.choice(available_positions)
            
            # Teleport snake1
            head_offset_x = snake1.body[0][0] - new_pos1[0]
            head_offset_y = snake1.body[0][1] - new_pos1[1]
            
            new_body1 = []
            for segment in snake1.body:
                new_x = (segment[0] - head_offset_x) % GameSettings.GRID_WIDTH
                new_y = (segment[1] - head_offset_y) % GameSettings.GRID_HEIGHT
                new_body1.append((new_x, new_y))
            snake1.body = new_body1
            
            # Teleport snake2
            head_offset_x = snake2.body[0][0] - new_pos2[0]
            head_offset_y = snake2.body[0][1] - new_pos2[1]
            
            new_body2 = []
            for segment in snake2.body:
                new_x = (segment[0] - head_offset_x) % GameSettings.GRID_WIDTH
                new_y = (segment[1] - head_offset_y) % GameSettings.GRID_HEIGHT
                new_body2.append((new_x, new_y))
            snake2.body = new_body2
            
            # Add teleport particles
            for pos in [new_pos1, new_pos2]:
                snake1.particles.add_particles(
                    pos[0] * 20 + 10,
                    pos[1] * 20 + 10,
                    (0, 255, 255) if random.random() > 0.5 else (255, 255, 255),
                    15
                )
    
    def check_game_over(self):
        """Check if game is over"""
        if len(self.snakes) < 2:
            return True
        
        snake1, snake2 = self.snakes
        
        # Self collision
        if snake1.check_collision_with_self() or snake2.check_collision_with_self():
            return True
        
        # Collision with other snake
        if snake1.check_collision_with_other(snake2) or snake2.check_collision_with_other(snake1):
            return True
        
        # Starvation in Level 2
        if self.level_type == LevelType.QUANTUM:
            if len(snake1.body) <= 1 or len(snake2.body) <= 1:
                return True
        
        return False
    
    def get_score(self):
        """Get current score"""
        return self.score
    
    def reset(self):
        """Reset game state"""
        self.initialize_game()
        self.score = 0
        self.game_over = False