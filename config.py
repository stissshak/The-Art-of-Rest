# config.py

class Config:
    # Display
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60

    # Physics
    GRAVITY = 980
    MAX_FALL_SPEED = 1000

    PLAYER_SPEED = 60           # max walk speed
    GROUND_ACCEL = 980          # how fast we reach walk speed on ground
    AIR_ACCEL = 245             # reduced air control mid-jump
    MAX_STEP = 6                # max slope height (px) the worm can walk up

    JUMP_FWD_VX = 119
    JUMP_FWD_VY = -276          # +20% jump height (height scales with vy^2)
    BACKFLIP_VX = 91
    BACKFLIP_VY = -360
    JUMP_COOLDOWN = 0.3         # seconds after landing before you can jump again

    # Turns
    TURN_TIME = 20.0           # seconds per turn (Enter ends it early)

    # Weapons — switch with 1/2/3. Aim with Up/Down, fire/use with F.
    #   1 Bazooka  2 Rope  3 Shotgun
    AIM_SPEED = 90             # degrees/sec when aiming with Up/Down keys

    # Bazooka (hold F to charge, release to fire)
    PROJECTILE_MIN_POWER = 250
    PROJECTILE_MAX_POWER = 950
    CHARGE_RATE = 600          # power gained per second while holding fire
    EXPLOSION_RADIUS = 55
    EXPLOSION_DAMAGE = 45      # damage at blast center
    EXPLOSION_EDGE_DAMAGE = 15 # damage at the blast edge (floor for anyone in radius)
    KNOCKBACK = 350
    RETREAT_TIME = 2.0         # seconds after the blast before the turn ends

    # Rope (ninja rope: F to fire/attach, F again to detach; A/D swing, Up/Down reel)
    ROPE_MAX_LENGTH = 450      # furthest the grapple can reach
    ROPE_MIN_LENGTH = 25       # can't reel in past this
    ROPE_SWING_ACCEL = 700     # tangential push from A/D while swinging
    ROPE_REEL_SPEED = 130      # px/sec the rope shortens/lengthens with Up/Down

    # Shotgun (instant hitscan, two shots per turn)
    SHOTGUN_RANGE = 650
    SHOTGUN_DAMAGE = 25
    SHOTGUN_KNOCKBACK = 180
    SHOTGUN_CRATER = 13        # terrain bite at the impact point
    SHOTGUN_SHOTS = 2
