import pygame
import random

"""
Constantes globales
"""
 
# Colores
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
BLUE = (32, 30, 100)
RED = (255,0,0)
GREEN = (44,98,16)

# Dimensiones de la pantalla
LARGO_PANTALLA  = 900
ALTO_PANTALLA = 600

#----sprites------#
game_sprites = "E:/Apuntes/FIEE 2021-2/algoritmos/Scripts/Game/pacman.png"
#----------------#

class Pacman(pygame.sprite.Sprite):
    """ Esta clase representa la barra inferior que controla el protagonista. """
 
    # Función Constructor 
    def __init__(self, x, y):
        #  Llama al constructor padre
        super().__init__()
  
        # Establecemos el alto y largo
        # self.image = pygame.Surface([15, 15])
        # self.image.fill(BLANCO)
     
        self.image = pygame.image.load(game_sprites).convert_alpha()
        self.image = self.image.subsurface((853,54,35,34))

        #Look
        self.look = True
        
        # Establece como origen la esquina superior izquierda.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
        # Establecemos el vector velocidad
        self.cambio_x = 0
        self.cambio_y = 0
        self.paredes = None
     
    def change_look(self):

        if self.cambio_x != 0 or self.cambio_y != 0:

            # self.image = self.image.subsurface((853,5,35,34))
            self.image = pygame.image.load(game_sprites).convert_alpha()
            # Right
            if self.cambio_x > 0 and self.cambio_y == 0:
                self.image = self.image.subsurface((853,54,35,34))
            # Left
            elif self.cambio_x < 0 and self.cambio_y == 0:
                self.image = self.image.subsurface((853,354,35,34))
            # Up
            elif self.cambio_x == 0 and self.cambio_y > 0:
                self.image = self.image.subsurface((853,204,35,34))    
            # Down
            elif self.cambio_x == 0 and self.cambio_y < 0:
                self.image = self.image.subsurface((853,507,35,34))
            # Diagonal
            else:
                self.image = self.image.subsurface((853,5,35,34))
            
    def cambiovelocidad(self, x, y):
        """ Cambia la velocidad del protagonista. """
        self.cambio_x += x
        self.cambio_y += y
        
        self.change_look()
    
    def reset(self):
        self.rect.y = 50
        self.rect.x = 50

    def update(self):
        """ Cambia la velocidad del protagonista. """
        # Desplazar izquierda/derecha
        self.rect.x += self.cambio_x
         
        # Hemos chocado contra la pared después de esta actualización?
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.paredes, False)
        for bloque in lista_impactos_bloques:
            #Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado izquierdo del objeto que hemos tocado-
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            else:
                # En caso contrario, si nos desplazamos hacia la izquierda, hacemos lo opuesto.
                self.rect.left = bloque.rect.right
 
        # Desplazar arriba/izquierda
        self.rect.y += self.cambio_y
          
        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.paredes, False) 
        for bloque in lista_impactos_bloques:
                 
            # Reseteamos nuestra posición basándonos en la parte superior/inferior del objeto.
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top 
            else:
                self.rect.top = bloque.rect.bottom            
  

class Pared(pygame.sprite.Sprite):
    """ Pared con la que el protagonista puede encontrarse. """
    def __init__(self, x, y, largo, alto,color):
        """ Constructor para la pared con la que el protagonista puede encontrarse """
        #  Llama al constructor padre
        super().__init__()
 
        # Construye una pared azul con las dimensiones especificadas por los parámetros
        self.image = pygame.Surface([largo, alto])
        self.image.fill(color)
 
        # Establece como origen la esquina superior izquierda.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Ghost(pygame.sprite.Sprite):  
    """
    Esta clase representa la pelota.        
    Deriva de la clase "Sprite" en Pygame
    """
     
    def __init__(self, select):
        """Constructor. Le pasa el color al bloque,
        así como la posición de x,y """
        # Llama a la clase constructor padre (Sprite)
        super().__init__()
 
        # Crea una imagen del bloque y lo rellena de color.
        # También podríamos usar una imagen guardada en disco.
        # self.image = pygame.Surface([width, height])
        # self.image.fill(color)

        self.image = pygame.image.load(game_sprites).convert_alpha()
        
        if select == 0:
            self.image = self.image.subsurface((649,103,38,37))
        if select == 1:
            self.image = self.image.subsurface((700,103,37,37))
        if select == 2:
            self.image = self.image.subsurface((750,103,38,37))

        # Extraemos el objeto rectángulo que posee las dimensiones
        # de la imagen.
        # Estableciendo los valores para rect.x and rect.y actualizamos
        # la posición de este objeto.
        self.rect = self.image.get_rect()
 
        # Variables de instancia que controlan los bordes
        # donde rebotamos
        self.limite_izquierdo = 0
        self.limite_derecho = 0
        self.limite_superior = 0
        self.limite_inferior = 0
 
        # Variables de instancia que controlan nuestras
        # velocidades y dirección actuales
        self.cambio_x = 0
        self.cambio_y = 0
            
        self.paredes = None
 
    # Llamada para cada fotograma.
    def update(self):
        #------------------------------------------------------------------#
        # Desplazar izquierda/derecha
        self.rect.x += self.cambio_x
         
        # Hemos chocado contra la pared después de esta actualización?
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.paredes, False)
        for bloque in lista_impactos_bloques:
            #Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado izquierdo del objeto que hemos tocado-
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            else:
                # En caso contrario, si nos desplazamos hacia la izquierda, hacemos lo opuesto.
                self.rect.left = bloque.rect.right
            self.cambio_x *= -1

        # Desplazar arriba/izquierda
        self.rect.y += self.cambio_y
          
        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.paredes, False) 
        for bloque in lista_impactos_bloques:
                 
            # Reseteamos nuestra posición basándonos en la parte superior/inferior del objeto.
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top 
            else:
                self.rect.top = bloque.rect.bottom
            self.cambio_y *= -1


class Coin(pygame.sprite.Sprite):
    """ Pared con la que el protagonista puede encontrarse. """
    def __init__(self, x, y):
        """ Constructor para la pared con la que el protagonista puede encontrarse """
        #  Llama al constructor padre
        super().__init__()
 
        # Construye una pared azul con las dimensiones especificadas por los parámetros
        # self.image = pygame.Surface([largo, alto])
        # self.image.fill(ROJO)
 
        self.image = pygame.image.load(game_sprites).convert_alpha()
        self.image = self.image.subsurface((410,312,18,18))

        # Establece como origen la esquina superior izquierda.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.wall = None
        self.delete = False

    def check_position(self):
        superposition = pygame.sprite.spritecollide(self, self.wall, False)
        for i in superposition:
            self.delete = True


class Level():
    def __init__(self, Pared, Coin, Ghost, Pacman,dificulty):
        super().__init__()

        # Lista que almacena todos los sprites
        self.all_sprites = pygame.sprite.Group()
        
        # Construimos las paredes. (x_pos, y_pos, largo, alto)
        self.pared_list = pygame.sprite.Group()

        # Ghost list
        self.ghost_list = pygame.sprite.Group()

        # Coin list
        self.coin_list = pygame.sprite.Group()

        self.dificulty = dificulty

        self.stage()
    

    def stage(self):

        if self.dificulty == 0:
            color = BLUE
            
            # Block UR
            self.block = Pared(600,100,80,20,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block UR
            self.block = Pared(680,100,20,100,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block UL
            self.block = Pared(100,100,20,100,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block UL
            self.block = Pared(120,100,80,20,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block DR
            self.block = Pared(600,480,80,20,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block DR
            self.block = Pared(680,400,20,100,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)
            
            # Block DL
            self.block = Pared(100,400,20,100,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block DL
            self.block = Pared(120,480,80,20,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block C
            self.block = Pared(380,240,40,120,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)

            # Block C
            self.block = Pared(340,280,120,40,color)
            self.pared_list.add(self.block)
            self.all_sprites.add(self.block)
            
        elif self.dificulty == 1:
            color = GREEN

            #----------------------#
            # Add blocks
            #-----------------------#
        elif self.dificulty == 2:
            color = RED
            #----------------------#
            # Add blocks
            #-----------------------#


        # Left wall
        self.pared = Pared(0,0,10,600,color)
        self.pared_list.add(self.pared)
        self.all_sprites.add(self.pared)

        # Right wall
        self.pared = Pared(790,0,10,600,color)
        self.pared_list.add(self.pared)
        self.all_sprites.add(self.pared)

        # Up wall
        self.pared = Pared(10,0,790,10,color)
        self.pared_list.add(self.pared)
        self.all_sprites.add(self.pared)

        # Down wall
        self.pared = Pared(10,590,790,10,color)
        self.pared_list.add(self.pared)
        self.all_sprites.add(self.pared)



        # Coin
        for x in range(0,800,50):
            for y in range(0,600,50):

                self.coin = Coin(x,y)
                self.coin.wall = self.pared_list
                self.coin.check_position()

                if self.coin.delete == True:
                    del self.coin   
                else:
                    self.coin_list.add(self.coin)
                    self.all_sprites.add(self.coin)

        # Ghost
        for i in range(3):
            self.ghost = Ghost(i)
            self.ghost.paredes = self.pared_list

            # Establece una ubicación aleatoria para el bloque
            # ghost.rect.x = random.randrange(10,LARGO_PANTALLA-10)
            # ghost.rect.y = random.randrange(10,ALTO_PANTALLA-10)
            
            self.ghost.rect.x = 400
            self.ghost.rect.y = 100
            
            self.ghost.cambio_x = random.randrange(-5,5)
            while self.ghost.cambio_x == 0:
                self.ghost.cambio_x = random.randrange(-5,5)
                  
            self.ghost.cambio_y = random.randrange(-5,5)
            while self.ghost.cambio_y == 0:
                self.ghost.cambio_y = random.randrange(-5,5)

            self.ghost.limite_izquierdo = 10
            self.ghost.limite_superior = 10
            self.ghost.limite_derecho = 790
            self.ghost.limite_inferior = 590

            #Añade el bloque a la lista de objetos
            self.ghost_list.add(self.ghost)
            self.all_sprites.add(self.ghost)

        # objeto pacman
        self.protagonista = Pacman(50, 50)
        self.protagonista.paredes = self.pared_list
            
        self.all_sprites.add(self.protagonista)


class Stats():

    def __init__(self,lives,points,actual_level):
        super().__init__()

#---------------------------------------------------------------------------#

# Llamamos a esta función para que la biblioteca Pygame pueda autoiniciarse.
pygame.init()
 
# Creamos una pantalla de 800x600
screen = pygame.display.set_mode([LARGO_PANTALLA, ALTO_PANTALLA])
 
# Creamos el título de la ventana
pygame.display.set_caption('Pacman')
 
# Create level
level = Level(Pared, Coin, Ghost, Pacman,0)

reloj = pygame.time.Clock()
 
hecho = False

lives = 5
points = 0
actual_level = 0

while not hecho:
     
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
 
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                level.protagonista.cambiovelocidad(-3,0)
            elif evento.key == pygame.K_RIGHT:
                level.protagonista.cambiovelocidad(3,0)
            elif evento.key == pygame.K_UP:
                level.protagonista.cambiovelocidad(0,-3)
            elif evento.key == pygame.K_DOWN:
                level.protagonista.cambiovelocidad(0,3)
                 
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                level.protagonista.cambiovelocidad(3,0)
            elif evento.key == pygame.K_RIGHT:
                level.protagonista.cambiovelocidad(-3,0)
            elif evento.key == pygame.K_UP:
                level.protagonista.cambiovelocidad(0,3)
            elif evento.key == pygame.K_DOWN:
                level.protagonista.cambiovelocidad(0,-3)
  
    level.all_sprites.update()
     
    screen.fill(BLACK)
    
    # Desaparece fantasma
    ghost_hit_list = pygame.sprite.spritecollide(level.protagonista, level.ghost_list, False)
    
    # Lose lives
    for ghost in ghost_hit_list:
        lives -= 1
        print("lives: " + str(lives))
        level.protagonista.reset()

    # Game over
    if lives == 0:
        lives = 5
        points = 0
        actual_level = 0

        del level
        level = Level(Pared, Coin, Ghost, Pacman,actual_level)
        pygame.event.clear()

    
    # Desaparece moneda
    get_coin_list = pygame.sprite.spritecollide(level.protagonista, level.coin_list, True)

    for coin in get_coin_list:
        points+=1
        print("points: "+str(points))

        if len(level.coin_list) == 0:
            # New level
            lives +=1
            actual_level+=1
            del level
            level = Level(Pared, Coin, Ghost, Pacman,actual_level)
            pygame.event.clear()


    level.all_sprites.draw(screen)

    pygame.display.flip()
 
    reloj.tick(60)
             
pygame.quit()