import turtle
import random
import time

# Screen setup
screen = turtle.Screen()
screen.title("Space Invaders - Retro Version")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# Draw bottom HUD line
hud = turtle.Turtle()
hud.color("green")
hud.penup()
hud.goto(-300, -220)
hud.pendown()
hud.forward(600)
hud.hideturtle()

# Score Display
score = 0
score_display = turtle.Turtle()
score_display.color("green")
score_display.penup()
score_display.hideturtle()
score_display.goto(200, -250)
score_display.write(f"Score: {score}", align="left", font=("Courier", 14, "normal"))

# Player (Tank)
player = turtle.Turtle()
player.shape("square")
player.color("green")
player.penup()
player.shapesize(stretch_wid=1, stretch_len=2)
player.goto(0, -200)
player_speed = 20

# Move player left
def move_left():
    x = player.xcor()
    if x > -260:
        player.setx(x - player_speed)

# Move player right
def move_right():
    x = player.xcor()
    if x < 260:
        player.setx(x + player_speed)

# Bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("white")
bullet.penup()
bullet.shapesize(stretch_wid=0.2, stretch_len=0.8)
bullet.hideturtle()
bullet_speed = 15
bullet_state = "ready"

# Fire bullet
def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# Aliens (Randomly Spread)
aliens = []
alien_count = 8  # Number of aliens
alien_speed = 0.05

for _ in range(alien_count):
    alien = turtle.Turtle()
    alien.shape("square")
    alien.color("green")
    alien.penup()
    alien.shapesize(stretch_wid=1, stretch_len=1.5)
    x = random.randint(-250, 250)
    y = random.randint(100, 200)
    alien.goto(x, y)
    aliens.append(alien)

# Collision detection
def is_collision(t1, t2):
    return t1.distance(t2) < 20

# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Main game loop
game_over = False
game_won = False

while not game_over and not game_won:
    screen.update()

    # Move aliens down slowly
    for alien in aliens[:]:
        alien.sety(alien.ycor() - alien_speed)

        # Check if alien reaches player
        if alien.ycor() < -190:
            game_over = True
            break

    # Bullet movement and collision
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)

        # Bullet out of bounds
        if bullet.ycor() > 250:
            bullet.hideturtle()
            bullet_state = "ready"

        # Check collision with aliens
        for alien in aliens[:]:
            if is_collision(bullet, alien):
                alien.hideturtle()
                aliens.remove(alien)  # Remove the alien from the list
                bullet.hideturtle()
                bullet_state = "ready"  # Bullet resets after hitting ONE alien
                score += 10
                score_display.clear()
                score_display.write(f"Score: {score}", align="left", font=("Courier", 14, "normal"))
                break  # Stop checking after hitting one alien

    # Check if all aliens are gone
    if not aliens:
        game_won = True

# End game screen
screen.clear()
screen.bgcolor("black")
hud.goto(-50, 0)

if game_over:
    hud.write("GAME OVER", align="center", font=("Courier", 20, "bold"))
elif game_won:
    hud.write("YOU WIN!", align="center", font=("Courier", 20, "bold"))

# Close the game after 3 seconds
time.sleep(3)
screen.bye()
