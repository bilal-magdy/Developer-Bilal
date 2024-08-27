import pygame
import pymunk
import pymunk.pygame_util

# تعاريف للألوان والصور
BG = (50, 50, 50)
dia = 36

# تحميل الصور
try:
    t_image = pygame.image.load('table.png').convert_alpha()
    cue_image = pygame.image.load('cue.png').convert_alpha()
    balls_imgs = []
    for imo in range(1, 17):
        ball_img = pygame.image.load(f'ball_{imo}.png').convert_alpha()
        balls_imgs.append(ball_img)
except pygame.error as e:
    print(f"Error loading images: {e}")
    exit()

# إعداد Pygame و Pymunk
pygame.init()
WIDTH = 1200
HEIGHT = 640
PANEL = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT + PANEL))
pygame.display.set_caption("BILAL MAGDY")
clock = pygame.time.Clock()
FPS = 60

space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    move = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    move.max_bias = 0
    move.max_force = 1000
    space.add(body, shape, move)
    return shape

def create_border(poly_d):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Poly(body, poly_d)
    shape.elasticity = 0.8
    space.add(body, shape)

# إنشاء الكرات
balls = []
rows = 5
for col in range(5):
    for row in range(rows):
        pos = (250 + (col * dia), 267 + (row * dia) + (col * dia / 2))
        new_ball = create_ball(dia / 2, pos)
        balls.append(new_ball)
    rows -= 1

# إضافة كرة إضافية في موضع ثابت
pos = (888, HEIGHT / 2)
new1_ball = create_ball(dia / 2, pos)
balls.append(new1_ball)

# تعريف حدود التربيزة
borders = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

# إضافة الحدود إلى التربيزة
for b in borders:
    create_border(b)

class Cue:
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        surface.blit(self.image, self.rect.topleft)

cue = Cue(balls[-1].body.position)

run = True
while run:
    screen.fill(BG)
    screen.blit(t_image, (0, 0))  # رسم التربيزة
    
    # رسم الكرات
    for i, ball in enumerate(balls):
        screen.blit(balls_imgs[i], (ball.body.position[0] - dia / 2, ball.body.position[1] - dia / 2))
    
    # تحديث موقع العصا بناءً على موقع الكرة الأخيرة
    cue.rect.center = balls[-1].body.position
    
    # رسم العصا
    cue.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # زيادة السرعة باستخدام قوة دفع أكبر
            new1_ball.body.apply_impulse_at_local_point((-2200, 0), (0, 0))
        if event.type == pygame.QUIT:
            run = False

    # تحديث الشاشة
    clock.tick(FPS)
    space.step(1 / FPS)
    pygame.display.flip()

pygame.quit()
