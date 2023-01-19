#! /usr/bin/env python3

import math
import os
from random import randint
from collections import deque
from sys import exit
import pygame
from pygame.locals import *

SOUNDS = {} # 사운드를 담는 dictionary 초기화
IMAGES = {} # 이미지를 담는 dictionary 초기화

FPS = 60
ANIMATION_SPEED = 0.18
WIN_WIDTH = 284 * 2     
WIN_HEIGHT = 512

# Bird 클래스 동작 방식:
#   image와 mask 속성은 pygame.time.get_ticks() 함수를 사용하여 현재 애니메이션 타이밍에 따라
#   반환할 이미지 또는 마스크를 결정합니다.
#   500 msec마다 wingup과 wingdown 이미지 사이를 전환하여 새의 날개 위치가 꾸어줍니다.
#   rect 속성은 새의 rect 위치를 반환하며 충돌 감지 및 화면에서의 배치에 사용됩니다.
class Bird(pygame.sprite.Sprite):

    # 상수값 정의: bird's size, speed and animation timing
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, msec_to_climb, images):
        super(Bird, self).__init__() # super class 초기화
        # bird's initial position and animation timing 설정
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        # bird's animation에 필요한 이미지 설정
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frames=1):
        if self.msec_to_climb > 0: # Check if the bird is still climbing
            # bird의 climb 동작을 끝내야 하는지 계산
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            # bird의 y좌표 위치 계산
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            # Decrement the climb time
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)

    @property
    def image(self): # animation timing에 따라 bird up/down 이미지 결정하여 반환
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown

    @property
    def mask(self): # animation timing에 따라 up/down mask 반환
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self): # bird의 rect 위치 반환
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


# 파이프 클래스 정의
class PipePair(pygame.sprite.Sprite):

    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):
        """Initialize a new PipePair.
        Args:
            pipe_end_img (pygame.Surface): The image of the end of the pipe.
            pipe_body_img (pygame.Surface): The image of the body of the pipe.
        """
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
    def top_height_px(self): # 위쪽 파이프의 높이 반환 
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self): # 아래쪽 파이프의 높이 반환 
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self): # 파이프가 현재 screen에서 보이는지 여부 반환
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self): # 충돌 여부 검출을 위한 파이프 rect 위치 반환
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)

    def update(self, delta_frames=1): # 파이프 위치 이동 update
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    def collides_with(self, bird): # 파이프와 bird가 충돌했는지 반환
        return pygame.sprite.collide_mask(self, bird)


def load_images(): # image file로부터 image dictionary로 이미지 읽어온다.
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

# helper function that converts the given number of frames to milliseconds.
def frames_to_msec(frames, fps=FPS):
    return 1000.0 * frames / fps

# helper function that converts the given number of milliseconds to frames.
def msec_to_frames(milliseconds, fps=FPS):
    return fps * milliseconds / 1000.0

# 게임 대기 함수: SPACE 누를 때까지 대기
def game_waiting(display_surface, clock, background_image):
    game_wait = True;
    while game_wait:
        clock.tick(FPS)
        
        # 게임 배경 화면 그리기
        for x in (0, WIN_WIDTH / 2):
            display_surface.blit(background_image, (x, 0))
        
        wait_for_space_font = pygame.font.Font(None, 40, bold=True)
        wait_label = wait_for_space_font.render("Press 'SPACE' to start", 1, (255,255,255))
        display_surface.blit(wait_label, (WIN_WIDTH/2 - wait_label.get_width()/2, 200))
        pygame.display.update()
        
        # SPACE 누르면 while 루프를 빠져 나감
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: # SPACE을 누르면 게임 시작
                if event.key == pygame.K_SPACE:
                    game_wait = False
    
# main 게임 함수
def main():
    pygame.init()

    # game window 생성 
    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pygame Flappy Bird')

    # frame rate에 따른 clock 생성
    clock = pygame.time.Clock()
    
    # "game over" 및 "score" text 표시를 위한 font 생성
    gameOver_font = pygame.font.Font(None, 100, bold=True)
    gameOver_restart_font = pygame.font.Font(None, 40, bold=True)
    score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
    
    # 게임 이미지 읽어서 생성
    images = load_images() 

    # bird up/down에 대해 초기 이미지 생성
    bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                (images['bird-wingup'], images['bird-wingdown']))
    pipes = deque() # deque로부터 파이프 가져오기

    # 사운드 효과를 위한 dictionary 생성
    SOUNDS['die']    = pygame.mixer.Sound('audio/die.wav')
    SOUNDS['hit']    = pygame.mixer.Sound('audio/hit.wav')
    SOUNDS['point']  = pygame.mixer.Sound('audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    SOUNDS['wing']   = pygame.mixer.Sound('audio/wing.wav')
    SOUNDS['good']   = pygame.mixer.Sound('audio/good.wav')
    SOUNDS['good_2']   = pygame.mixer.Sound('audio/good_2.wav')

    # Load images for gameover, restart, good_job, and great 
    IMAGES['gameover'] = pygame.image.load('images/gameover.png').convert_alpha()
    IMAGES['restart'] = pygame.image.load('images/restart.png').convert_alpha()
    IMAGES['good'] = pygame.image.load('images/good.png').convert_alpha()
    IMAGES['great'] = pygame.image.load('images/great.png').convert_alpha()

    frame_clock = 0 
    score = 0
    done = paused = False
    game_on = True
    game_running = True
    game_over = False

    # SPACE 누를 때까지 대기
    game_waiting(display_surface, clock, images['background'])
        
    # Main game 루프
    while not done:
        # Reset bird and pipes for a new game
        bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,(images['bird-wingup'], images['bird-wingdown']))
        pipes = deque()
        SOUNDS['swoosh'].play() # 게임 시작 사운드 play
        
        # Inner game loop for running the game
        while game_running:
              clock.tick(FPS)

              # Add a new pipe pair if the frame clock is at the correct interval
              if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
                pp = PipePair(images['pipe-end'], images['pipe-body'])
                pipes.append(pp)

              # Handle events such as UP/DOWN, 정지(K_p), quitting(K_ESCAPE) or space bar press
              for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                   done = True # 게임 종료
                   break
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                   bird.msec_to_climb = Bird.CLIMB_DURATION # 위로올라가기 시작
                   SOUNDS['wing'].play()
                elif event.type == KEYUP and event.key in (K_PAUSE, K_p):
                   paused = not paused # 게임 정지 toggle

              # 게임 정지 상태이면, 아래 게임 처리 로직을 skip함
              if paused:
                  continue 

              # bird와 파이프가 충돌했는지 혹은 bird가 화면 끝에 부딪혔는지 체크
              pipe_collision = any(p.collides_with(bird) for p in pipes)
              if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                # done = True
                game_over = True # 게임 종료
                game_running = False
                SOUNDS['hit'].play()
                SOUNDS['die'].play()
              
              # 게임 배경 화면 그리기
              for x in (0, WIN_WIDTH / 2):
                display_surface.blit(images['background'], (x, 0))

              # 파이프가 화면에서 사라졌다면 파이프 제거
              while pipes and not pipes[0].visible:
                 pipes.popleft()

              # 파이프 새로 그리기
              for p in pipes:
                 p.update()
                 display_surface.blit(p.image, p.rect)

              # bird 새로 그리기
              bird.update()
              display_surface.blit(bird.image, bird.rect)

              # bird가 파이프를 통과했는지 체크
              for p in pipes:
                if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                    score += 1 # 점수 증가
                    SOUNDS['point'].play()
                    if score == 1 or score == 3:
                        SOUNDS['good'].play() # good 사운드 play
                    p.score_counted = True
                if not game_over and score == 1: # 게임종료가 아니고 score가 1이면 good 표시
                    display_surface.blit(IMAGES['good'], (140, 290))
                if not game_over and score == 3: # 게임종료가 아니고 score가 3이면 great 표시
                    display_surface.blit(IMAGES['great'], (120, 290))

              # 점수 표시
              score_surface = score_font.render('score: ' + str(score), True, (255, 255, 255))
              score_x = WIN_WIDTH/2 + score_surface.get_width()/2
              display_surface.blit(score_surface, (score_x, 20)) # PipePair.PIECE_HEIGHT))

              pygame.display.flip() # Update the display
              frame_clock += 1 # Increase the frame clock

        while game_over: # Handle game over status
            clock.tick(FPS)

            for event in pygame.event.get():
                if (event.type == pygame.KEYUP and event.key == K_ESCAPE) or (event.type == pygame.QUIT):
                    done = True # 게임 종료
                    game_over = 0
                    break
                if event.type == pygame.KEYUP and event.key == K_SPACE: # SPCAE 누르면 게임 다시 시작
                    game_running = True
                    game_over = False
                    score = 0
            
            display_surface.blit(IMAGES['gameover'], (180, 180))
            display_surface.blit(IMAGES['restart'], (110, 300))
            pygame.display.flip()

    print('FLAPPY BIRD play well')
    pygame.quit()

if __name__ == '__main__':
    main()
