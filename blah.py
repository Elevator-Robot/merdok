import time
import random
import os

# Function to clear the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to create the orb face with a given number
def create_orb_face(number, position):
    orb_faces = {
        "center": f"""
                 (  )
              ( )     (
            (    {str(number).center(3)}    )
              (         )
                 (  )
        """,
        "left": f"""
              (  )
             ( )     (
           (    {str(number).center(3)}    )
             (         )
              (  )
        """,
        "right": f"""
                 (  )
                ( )     (
              (    {str(number).center(3)}    )
                (         )
                 (  )
        """
    }
    return orb_faces[position]

# Function to generate a list of orb faces for numbers 1 to top_int
def generate_orb_faces(top_int, positions):
    orb_faces = []
    for i in range(1, top_int + 1):
        for pos in positions:
            orb_faces.append(create_orb_face(i, pos))
    return orb_faces

# Function to animate dice roll
def roll_orb_animation(orb_faces, animation_frames):
    for _ in range(animation_frames):  # Number of frames in the animation
        clear()
        print(random.choice(orb_faces))
        time.sleep(0.1)  # Delay between frames

# Function to roll the orb and display the final result
def roll_orb(top_int, animation_frames=30):
    positions = ["center", "left", "right"]
    orb_faces = generate_orb_faces(top_int, positions)
    roll_orb_animation(orb_faces, animation_frames)
    clear()
    result = random.choice(orb_faces)
    print(result)
    return orb_faces.index(result) // len(positions) + 1

# Simulate a magical orb roll with a top integer
top_int = 20
result = roll_orb(top_int)
print(f"You rolled a {result}!")
