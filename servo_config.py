import math
 
servo_param = {
    # Upper Arm Servo
    1: { 
        'home_encoder': 0,
        'max_ang': math.radians( 360 ),
        'min_ang': math.radians( 0 )
#       'max_speed': math.radians(50)
#		'rad_per_enc': math.radians(300.0) / 1024.0,
#		'flipped': False,
       },

    # Grasper Servo
    2: {
        'home_encoder': 0,
        'max_ang': math.radians( 360 ),
        'min_ang': math.radians( 0 )
        },
    3: {
        'home_encoder': 0,
        'max_ang': math.radians( 360 ),
        'min_ang': math.radians( 0 )
        },
    4: {
        'home_encoder': 0,
        'max_ang': math.radians( 360 ),
        'min_ang': math.radians( 0 )
        },
    5: {
        'home_encoder': 0x01FF,
        'max_encoder': 0xFFF,  # Assumes 0 is min.
        'flipped': False,
        }
}

# CW negative, CCW positive from face
