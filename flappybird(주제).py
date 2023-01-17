#! /usr/bin/env python3

"""Flappy Bird, implemented using Pygame."""

import math
import os
from random import randint
from collections import deque
import pygame
from pygame.locals import *

SOUNDS = {}

FPS = 60
ANIMATION_SPEED = 0.18
WIN_WIDTH = 284 * 2     
WIN_HEIGHT = 512


class Bird(pygame.sprite.Sprite):

    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, msec_to_climb, images):
    
        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frames=1):

        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)

    @property
    def image(self):

        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown

    @property
    def mask(self):

        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


class PipePair(pygame.sprite.Sprite):

    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):

        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False

        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()  
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int(
            (WIN_HEIGHT -                
             3 * Bird.HEIGHT -            
             3 * PipePair.PIECE_HEIGHT) /  
            PipePair.PIECE_HEIGHT         
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i*PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))
        self.top_pieces += 1
        self.bottom_pieces += 1
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self):
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)

    def update(self, delta_frames=1):
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    def collides_with(self, bird):
        return pygame.sprite.collide_mask(self, bird)


def load_images():
    def load_image(img_file_name):
        file_name = os.path.join(os.path.dirname(__file__),
                                 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'background': load_image('background.png'),
            'pipe-end': load_image('pipe_end.png'),
            'pipe-body': load_image('pipe_body.png'),
            'bird-wingup': load_image('bird_wing_up.png'),
            'bird-wingdown': load_image('bird_wing_down.png')}


def frames_to_msec(frames, fps=FPS):
    return 1000.0 * frames / fps


def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0


def main():
    pygame.init()

    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pygame Flappy Bird')

    clock = pygame.time.Clock()
    gameOver_font = pygame.font.Font(None, 100, bold=True)
    gameOver_restart_font = pygame.font.Font(None, 40, bold=True)
    score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
    images = load_images()

    bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                (images['bird-wingup'], images['bird-wingdown']))
    pipes = deque()

    SOUNDS['die']    = pygame.mixer.Sound('audio/die.wav')
    SOUNDS['hit']    = pygame.mixer.Sound('audio/hit.wav')
    SOUNDS['point']  = pygame.mixer.Sound('audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    SOUNDS['wing']   = pygame.mixer.Sound('audio/wing.wav')

    frame_clock = 0 
    score = 0
    done = paused = False
    game_running = True
    game_over = False

    while not done:
        bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,(images['bird-wingup'], images['bird-wingdown']))
        pipes = deque()
        SOUNDS['swoosh'].play()
        while game_running:
              clock.tick(FPS)

              if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
                pp = PipePair(images['pipe-end'], images['pipe-body'])
                pipes.append(pp)

              for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                   done = True
                   break
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                   bird.msec_to_climb = Bird.CLIMB_DURATION
                   SOUNDS['wing'].play()
                elif event.type == KEYUP and event.key in (K_PAUSE, K_p):
                   paused = not paused

              if paused:
                  continue 

              pipe_collision = any(p.collides_with(bird) for p in pipes)
              if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                # done = True
                game_over = True
                game_running = False
                SOUNDS['hit'].play()
              for x in (0, WIN_WIDTH / 2):
                display_surface.blit(images['background'], (x, 0))

              while pipes and not pipes[0].visible:
                 pipes.popleft()

              for p in pipes:
                 p.update()
                 display_surface.blit(p.image, p.rect)

              bird.update()
              display_surface.blit(bird.image, bird.rect)

            # update and display score
              for p in pipes:
                if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                    score += 1
                    SOUNDS['point'].play()
                    p.score_counted = True

              score_surface = score_font.render(str(score), True, (255, 255, 255))
              score_x = WIN_WIDTH/2 - score_surface.get_width()/2
              display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

              pygame.display.flip()
              frame_clock += 1

        while game_over:
            clock.tick(FPS)

            for event in pygame.event.get():
                if (event.type == pygame.KEYUP and event.key == K_ESCAPE) or (event.type == pygame.QUIT):
                    done = True
                    game_over = 0
                    break
                if event.type == pygame.KEYUP and event.key == K_SPACE:
                    game_running = True
                    game_over = False
                    score = 0

            gameOver = gameOver_font.render("Game Over", True, (255, 0, 0))
            gameOver_rect = gameOver.get_rect()
            gameOver_rect.center = (int(WIN_WIDTH / 2), 200)

            gameOverRestart = gameOver_restart_font.render("Press space to restart!", True, (255, 0, 0))
            gameOverRestart_rect = gameOverRestart.get_rect()
            gameOverRestart_rect.center = (int(WIN_WIDTH / 2), 301)

            display_surface.blit(gameOver, gameOver_rect)
            display_surface.blit(gameOverRestart, gameOverRestart_rect)

            pygame.display.flip()


    print('Game over! Score: %i' % score)
    pygame.quit()

if __name__ == '__main__':
    main()
