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

    # Jumps (forward jump = Space, backflip = Backspace)
    JUMP_FWD_VX = 119
    JUMP_FWD_VY = -276          # +20% jump height (height scales with vy^2)
    BACKFLIP_VX = 91
    BACKFLIP_VY = -360
    JUMP_COOLDOWN = 0.3         # seconds after landing before you can jump again
