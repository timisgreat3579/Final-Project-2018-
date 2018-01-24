import pygame,os, sys
import importlib
from configparser import ConfigParser
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
#if pygame.QUIT in pygame.event.get(): pygame.quit();raise SystemExit;
user_login = ''

class load_screen():
    def __init__(self):
        self.screen = pygame.display.set_mode((640,350),pygame.NOFRAME)
        self.draw()
    def draw(self):
        self.screen.fill((0,0,0))
        pygame.display.flip() 

class buffer():
    def __init__(self,surface,x,y,default_text='',alpha=200):
        self.load_text = pygame.font.SysFont('Arial',50,True)
        self.default_text= default_text
        self.load_additive = self.default_text
        self.x =x
        self.y = y
        self.screen = surface
        self.background = pygame.Surface((surface.get_width(),surface.get_height()))
        self.background.fill((70,70,70))
        self.background.set_alpha(alpha)
    def draw(self,surf):
        self.load_additive += '.'
        if len(self.load_additive) > 3:
            self.load_additive = self.default_text
        self.text_surface = self.load_text.render(self.load_additive,True,(255,255,255))
        surf.blit(self.background,(self.x,self.y)) 
        surf.blit(self.text_surface,((self.background.get_width() - self.text_surface.get_width())/2 + self.x
                                               ,(self.background.get_height() - self.text_surface.get_height())/2+self.y))
        

class session_create():
    def __init__(self):
        import boto3
        from configparser import ConfigParser
        cred = ConfigParser()
        cred.read('./data/credentials.ini')
        self.session = boto3.resource('dynamodb',
                        aws_access_key_id=cred.get('default','aws_access_key_id'),
                         aws_secret_access_key=cred.get('default','aws_secret_access_key'),
                         region_name="ca-central-1"
                         )
class surface_object():
    def __init__(self,w,h,x,y,color,alpha=255):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.surface = pygame.Surface((self.w,self.h))
        self.surface = self.surface.convert()
        self.surface.fill(self.color)
        self.surface.set_alpha(alpha)
    def set_color(self,color):
        self.surface.fill(color)

    def on_mouse_hover(self):
        return pygame.Rect(self.x,self.y,self.w,self.h).collidepoint(pygame.mouse.get_pos())

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h

    def get_rect(self):
        return self.surface.get_rect(center=(self.x,self.y))
    
def change_text(text):
    buff.default_text = text
    buff.draw(scr)   
    pygame.display.flip()

    
scr = load_screen().screen
buff = buffer(surface_object(640,350,0,0,(0,0,0)),0,0,'LOADING',255)
buff.draw(scr)
pygame.display.flip()



change_text('CHECKING PIP')

if importlib.find_loader('pip') is None:
    from .getpip import *
import pip
change_text('CHECKING BOTO')
if importlib.find_loader('boto3') is None:
    change_text('INSTALLING BOTO')
    pip.main(['install','boto3'])

change_text('LOGGING IN...')
session_var = session_create().session
pygame.quit()

from .loginWindow import runLogin
file = open('./data/session.txt', 'r')
for line in file:
    us = line

if us == '0':
    user_login = runLogin()

    file = open('./data/usr.txt', 'w')
    file.write(user_login)
    file.close()


from .launcher_screen import *
