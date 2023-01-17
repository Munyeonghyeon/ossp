#! /usr/bin/env python3
"""Flappy Bird, implemented using Pygame."""
import math
import os
from random import randint
from collections import deque
import pygame
from pygame.locals import *
FPS = 60
ANIMATION_SPEED = 0.18  # 밀리초당 픽셀 수
WIN_WIDTH = 284 * 2     # BG 이미지 크기: 284x512px, 타일을 두 번 붙임
WIN_HEIGHT = 512
class Bird(pygame.sprite.Sprite):
    """
     새는 이 게임의 '영웅'이다. 플레이어는 기어오를 수 있다
     (빠른 속도로), 그렇지 않으면 가라앉습니다(더 느리게 끝납니다). 꼭 해야 한다
      파이프 사이의 공간을 통과한다(파이프를 통과할 때마다, 하나씩)
      점수가 매겨짐); 파이프에 충돌하면 게임이 종료됩니다.
     속성(Attributes)
     x: 새의 X 좌표입니다.
     y: 새의 Y 좌표입니다.
     msec_to_interval: 상승할 때까지 남은 밀리초(밀리초)입니다
     마지막 등반은 새가 한다.CLAMP_Duration 밀리초.
     상수(Constants)
     WIDTH - 너비: 새 이미지의 너비(픽셀)입니다.
     HEIGHT - 높이: 새 이미지의 높이(픽셀)입니다.
     SINK_SPEED - 싱크_스피드: 새의 속도(밀리초당 픽셀 단위)
     등반하지 않고 1초 만에 하강한다.
     CLAMP_SPEED: 새의 속도(밀리초당 픽셀 단위)
     평균적으로 등반 중 1초 만에 오른다. 자세한 내용은 을 참조하십시오
     Bird.docstring을 업데이트합니다.
     CLAMP_Duration: 새가 다음 시간까지 걸리는 시간(밀리초) 완등하다.
    """
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3
    def __init__(self, x, y, msec_to_climb, images):
        """
        새로운 Bird 인스턴스를 초기화
        Arguments(인수):
        x: 새의 초기 X 좌표입니다.
        y: 새의 초기 y 좌표입니다.
        msec_to_interval: 완전한 등반이 새를 지속하는 등반 시간(밀리초).
        CLAMP_Duration 밀리초: 게임 시작 시 새가 (작은?) 오르도록 하려면 이 옵션을 사용합니다.
        images 이 새가 사용하는 이미지가 들어 있는 튜플입니다. 그 튜플 에는 다음 이미지가 순서대로 포함되어 있습니다.
           -> 0. 날개가 위로 향한 그 새의 이미지
           -> 1. 날개가 아래를 향하고 있는 새의 모습
        """
        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)
    def update(self, delta_frames=1):
        """
        새의 위치를 업데이트합니다.
        이 함수는 코사인 함수를 사용하여 원활한 조작을 실행합니다: 처음과 마지막 몇 프레임에서, 새는 아주 조금 오르고, 중간에, 많이 올라갑니다.(?)
         CLAMP_Duration 밀리초 동안 지속되며, 이 기간 동안 새는 CLAMP_SPEED px/ms의 평균 속도로 상승한다.
        이 메서드가 호출되었을 때 0보다 크면 이 Bird의 msec_to_climb 속성이 자동으로 감소합니다.
        Arguments:
        delta_frames - 델타_프레임: 이 메서드를 마지막으로 호출한 이후 경과된 프레임 수입니다.
        """
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)
    @property
    def image(self):
        """이 새의 이미지가 포함된 표면을 가져옵니다.
        이것은 pygame.time.get_ticks()를 기준으로 
        새의 보이는 날개가 위쪽을 가리키고 있는 이미지를 반환할지 
        또는 아래쪽을 가리키고 있는 이미지를 반환할지 결정합니다.  
        
        파이게임은 GIF를 지원하지 않지만, 이함수는 펄럭이는 새 애니메이션을 만들 것이다.
        """
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown
    @property
    def mask(self):
        """충돌 감지에 사용할 비트 마스크를 가져옵니다.
         비트마스크는 self.image의 모든 픽셀을 제외합니다
         투명도가 127보다 큽니다.
         """
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown
    @property
    def rect(self):
        """새의 위치, 너비 및 높이 가져오기, as a pygame.Rect."""
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)
class PipePair(pygame.sprite.Sprite):
    """장애물을 나타냅니다.
    파이프 쌍에는 상하 파이프가 있고, 그 사이에서만 새가 지나갈 수 있습니다. 
    새가 파이프에 충돌하면 게임은 끝납니다.
    Attributes - 속성:
    x: 파이프 쌍의 X 위치. 이것은 움직임을 더 부드럽게 하기 위한 플로트입니다. 
    y 속성은 항상 0이 되기 때문에 없습니다.
    image:파이 게임.파이프 쌍을 표시하기 위해 표시 표면에 블릿할 수 있는 표면입니다.
    mask: self.image에서 투명도가 127보다 큰 모든 픽셀을 제외하는 비트마스크입니다. 충돌 감지에 사용할 수 있습니다.
    top_pieces: 맨 위 파이프의 끝 부분을 포함한 조각 수입니다.
    bottom_pieces: 맨 아래 파이프의 끝 부분을 포함한 조각 수입니다.
    Constants - 상수:
    WIDTH - 너비: 파이프 조각의 너비(픽셀)입니다. 파이프의 너비가 한 조각에 불과하기 때문에 파이프 쌍 이미지의 너비이기도 합니다.
    PIECE_HIGHT: 파이프 조각의 높이(픽셀)입니다.
    ADD_INTERVAL: 새 파이프를 추가하는 간격(밀리초)입니다.
    """
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000
    def __init__(self, pipe_end_img, pipe_body_img):
        """새 랜덤 파이프 쌍을 초기화합니다.
        새 PipePair에는 mfloat의 x 속성(WIN_WIDTH - 1)이 자동으로 할당됩니다.
        Arguments - 인수:
        pipe_end_img: 파이프의 끝 부분을 나타내는 데 사용할 이미지입니다.
        pipe_body_img: 파이프 본문의 하나의 수평 슬라이스를 나타내는 데 사용할 이미지입니다.
        """
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False
        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()   # 속도를 높이다
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int(
            (WIN_HEIGHT -                  # 위에서 아래까지 window창을 채운다
             3 * Bird.HEIGHT -             # 새가 파이프 사이를 통과 할 수 있는 공간을 만들다
             3 * PipePair.PIECE_HEIGHT) /  # 2 end pieces + 1 body piece
            PipePair.PIECE_HEIGHT          # 파이프 조각 수를 구하다
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces
       # 바닥 파이프(아래쪽에 위치)
        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i*PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)
        # 맨 위의 파이프(위쪽에 위치)
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))
        # compensate for added end pieces
        self.top_pieces += 1
        self.bottom_pieces += 1
        #충돌 감지용
        self.mask = pygame.mask.from_surface(self.image)
    @property
    def top_height_px(self):
        #상단 파이프의 높이를 픽셀 단위로 가져옵니다
        return self.top_pieces * PipePair.PIECE_HEIGHT
    @property
    def bottom_height_px(self):
        #하단 파이프의 높이를 픽셀 단위로 가져옵니다.
        return self.bottom_pieces * PipePair.PIECE_HEIGHT
    @property
    def visible(self):
        #플레이어가 이 파이프 쌍을 게임화면 볼 수 있는지 여부를 확인합니다.
        return -PipePair.WIDTH < self.x < WIN_WIDTH
    @property
    def rect(self):
        #이 파이프 쌍이 들어 있는 Rect를 가져옵니다.
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)
    def update(self, delta_frames=1):
        """파이프 쌍의 위치를 업데이트합니다.
        Arguments - 인수:
        delta_frames: 이 메서드를 마지막으로 호출한 이후 경과된 프레임 수입니다.
        """
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)
    def collides_with(self, bird):
        """이 파이프 쌍에서 새가 파이프와 충돌하는지 확인하십시오.
        arguments - 인수:
        bird - 새: 이 파이프 쌍과의 충돌을 테스트해야 하는 새.
        """
        return pygame.sprite.collide_mask(self, bird)
def load_images():
    """게임에 필요한 모든 이미지를 로드하고 해당 이미지의 딕트를 반환합니다.
    반환된 딕트에는 다음과 같은 키가 있습니다:
    background - 배경: 게임의 배경 이미지입니다.
    bird-wingup - 새 날개 돋우기: 날개가 위쪽을 향하고 있는 그 새의 이미지.
    이것과 새의 날개를 내려 날개를 퍼덕이는 새를 만들어 보세요.
    bird-wingdown - 새 날개 아래: 날개가 아래를 향하고 있는 새의 이미지.
    이것을 이용해서 새의 날개를 세워 날개를 퍼덕이는 새를 만들어 보세요.
    파이프 끝: 파이프 끝 부분(약간 넓은 비트)의 이미지입니다.
    이것과 파이프 본체를 사용하여 파이프를 만듭니다.
    파이프 본체: 파이프 본체 조각의 이미지입니다. 이것과 파이프 본체를 사용하여 파이프를 만듭니다.
    """
    def load_image(img_file_name):
        """지정한 파일 이름으로 로드된 파이 게임 이미지를 반환합니다.
        이 기능은 게임의 이미지 폴더(dirname(_file__)/images/)에서 이미지를 찾습니다. 
        모든 영상은 블릿 속도를 높이기 위해 반환되기 전에 변환됩니다.
        Arguments - 인수:
        img_file_name:  파일 경로가 없는 필수 이미지의 파일 이름입니다. (예: 'png'과 같은 확장자 포함)
        """
       # 이 스크립트와 관련된 이미지를 찾으십시오. 그래서 우리는 "cd"를 하지 않아도 됩니다
       # 스크립트를 실행하기 전에 스크립트의 디렉터리를 참조하십시오.
       # 참고 항목: https://github.com/TimoWilken/flappy-bird-pygame/pull/3
        file_name = os.path.join(os.path.dirname(__file__),
                                 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img
     # 펄럭이는 새를 애니메이션화하기 위한 이미지 -- 애니메이션 GIF는 파이 게임에서 지원되지 않음
    return {'background': load_image('background.png'),
            'pipe-end': load_image('pipe_end.png'),
            'pipe-body': load_image('pipe_body.png'),
            'bird-wingup': load_image('bird_wing_up.png'),
            'bird-wingdown': load_image('bird_wing_down.png')}
def frames_to_msec(frames, fps=FPS):
    """지정된 프레임 속도에서 프레임을 밀리초로 변환합니다.
    Arguments - 인수:
    frames: 밀리초로 변환할 프레임 수
    fps: 변환에 사용할 프레임률입니다. 기본값은 FPS입니다.
    """
    return 1000.0 * frames / fps
def msec_to_frames(milliseconds, fps=FPS):
    """밀리초를 지정된 프레임 속도의 프레임으로 변환합니다.
    Arguments - 인수:
    milliseconds: 프레임으로 변환할 시간(밀리초)입니다.
    fps: 변환에 사용할 프레임률입니다. 기본값은 FPS입니다.
    """
    return fps * milliseconds / 1000.0
def main():
    """응용 프로그램의 시작 지점입니다.
     다른 사용자가 이 모듈을 실행하는 경우(이 모듈을 가져오는 대신), 이 함수를 호출합니다.
    """
    pygame.init()
    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pygame Flappy Bird')
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 32, bold=True)  # default font
    images = load_images()
    # 새는 같은 x 위치에 있기 때문에 bird.x는 상수이다
    # 화면에 새를 띄우다
    bird = Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                (images['bird-wingup'], images['bird-wingdown']))
    pipes = deque()
    frame_clock = 0  # 이 카운터는 게임이 일시 중지되지 않은 경우에만 증분됩니다
    score = 0
    done = paused = False
    while not done:
        clock.tick(FPS)
        # 수동으로 처리하십시오. 만약 pygame.time.set_timer()를 사용했다면, 파이프 추가는 일시 중지되면서 엉망이 됩니다.
        if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
            pp = PipePair(images['pipe-end'], images['pipe-body'])
            pipes.append(pp)
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                paused = not paused
            elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                    e.key in (K_UP, K_RETURN, K_SPACE)):
                bird.msec_to_climb = Bird.CLIMB_DURATION
        if paused:
            continue  # don't draw anything
        # 충돌 여부를 점검하다
        pipe_collision = any(p.collides_with(bird) for p in pipes)
        if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
            done = True
        for x in (0, WIN_WIDTH / 2):
            display_surface.blit(images['background'], (x, 0))
        while pipes and not pipes[0].visible:
            pipes.popleft()
        for p in pipes:
            p.update()
            display_surface.blit(p.image, p.rect)
        bird.update()
        display_surface.blit(bird.image, bird.rect)
        # 점수 업데이트 및 표시
        for p in pipes:
            if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                score += 1
                p.score_counted = True
        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = WIN_WIDTH/2 - score_surface.get_width()/2
        display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))
        pygame.display.flip()
        frame_clock += 1
    print('Game over! Score: %i' % score)
    pygame.quit()
if __name__ == '__main__':
    # 이 모듈을 가져온 경우 __name_은(는) '플랩피버드'가 됩니다.
    # 실행되었으니 main을 불러라. (예: 파일을 두 번 클릭하여),
    main()
