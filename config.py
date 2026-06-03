# config.py

class Config:
    # Display
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60

    # Physics
    GRAVITY = 980
    MAX_FALL_SPEED = 1000

    # Movement (~30% slower than the first tuning pass)
    PLAYER_SPEED = 105          # max walk speed
    GROUND_ACCEL = 980          # how fast we reach walk speed on ground
    AIR_ACCEL = 245             # reduced air control mid-jump
    MAX_STEP = 6                # max slope height (px) the worm can walk up

    # Jumps (forward jump = Space, backflip = LShift)
    JUMP_FWD_VX = 119
    JUMP_FWD_VY = -276          # +20% jump height (height scales with vy^2)
    BACKFLIP_VX = 91
    BACKFLIP_VY = -360
    JUMP_COOLDOWN = 0.3         # seconds after landing before you can jump again

    # Turns
    TURN_TIME = 20.0           # seconds per turn (Enter ends it early)

    # Weapons (bazooka: aim with mouse or Up/Down, hold LMB/F to charge, release to fire)
    PROJECTILE_MIN_POWER = 250
    PROJECTILE_MAX_POWER = 950
    CHARGE_RATE = 600          # power gained per second while holding fire
    EXPLOSION_RADIUS = 55
    EXPLOSION_DAMAGE = 45      # damage at blast center
    EXPLOSION_EDGE_DAMAGE = 15 # damage at the blast edge (floor for anyone in radius)
    KNOCKBACK = 350
    RETREAT_TIME = 2.0         # seconds after the blast before the turn ends
    AIM_SPEED = 90             # degrees/sec when aiming with Up/Down keys
