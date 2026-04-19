import pygame

pygame.init()
ventana_x = 700
ventana_y = 700

ventana = pygame.display.set_mode((ventana_x, ventana_y))
pygame.display.set_caption("Moni")
reloj = pygame.time.Clock()

#clase personaje
class personaje(object):

    def __init__(self, x, y, fuente, limite):
        self.x = x
        self.y = y
        self.velocidad = 5
        #atributos para el salto
        self.impulso_salto=8
        self.ha_saltado=False

        #atributos para animacion de sprites
        self.va_izquierda = False
        self.va_derecha = False
        self.contador_pasos = 0
        fuente += "/"
        self.camina_izquierda = [pygame.image.load("img/"+fuente+"l1.png"), pygame.image.load("img/"+fuente+"l2.png"), pygame.image.load("img/"+fuente+"l3.png"), pygame.image.load("img/"+fuente+"l4.png"), pygame.image.load("img/"+fuente+"l5.png"), pygame.image.load("img/"+fuente+"l6.png")]

        self.camina_derecha = [pygame.image.load("img/"+fuente+"r1.png"), pygame.image.load("img/"+fuente+"r2.png"), pygame.image.load("img/"+fuente+"r3.png"), pygame.image.load("img/"+fuente+"r4.png"), pygame.image.load("img/"+fuente+"r5.png"), pygame.image.load("img/"+fuente+"r6.png")]

        self.quieto = pygame.image.load("img/"+fuente+"parado.png")
        # self.quieto = pygame.transform.scale(self.quieto, (40, 80))
        self.ancho = self.quieto.get_width()
        self.alto = self.quieto.get_height()
        #control desplazamiento automatico
        
        self.camino = [self.x, limite]
        #nivel de salud
        
    def dibujar(self, cuadro):
        if self.contador_pasos + 1 > 6:
            self.contador_pasos = 0 
        if self.va_izquierda:
            cuadro.blit(self.camina_izquierda[self.contador_pasos], (self.x + camara_x, self.y))
            self.contador_pasos +=1
        elif self.va_derecha:
            cuadro.blit(self.camina_derecha[self.contador_pasos], (self.x + camara_x, self.y))
            self.contador_pasos +=1
        else:
            cuadro.blit(self.quieto, (self.x + camara_x, self.y))
        
    def se_mueve_segun(self, k, iz, de, ar, ab, salta):
        if k[iz] and self.x > self.velocidad:
            self.x -= self.velocidad
            #controles de animacion
            self.va_izquierda = True
            self.va_derecha = False

        elif k[de] and self.x < ventana_x - self.ancho - self.velocidad:
            self.x += self.velocidad
            self.va_derecha = True
            self.va_izquierda = False

        else:
            #controles de animacion en caso de dejar de moverse horizontal
            self.va_izquierda = False
            self.va_derecha = False
            self.contador_pasos = 0

        #control del salto
        if self.ha_saltado:
            if self.impulso_salto >= -8:
                if self.impulso_salto < 0:
                    self.y += (self.impulso_salto**2)*0.5
                else:
                    self.y -= (self.impulso_salto**2)*0.5
                self.impulso_salto -= 1
            else:
                self.ha_saltado = False
                self.impulso_salto = 8
        else:
            if k[ar]:
                self.y -= self.velocidad
            if k[ab]:
                self.y += self.velocidad
            if k[salta]:
                self.ha_saltado = True
                #controles de animacion
                self.va_izquierda = False
                self.va_derecha = False
                self.contador_pasos = 0

    def se_mueve_solo(self):
        if self.velocidad > 0:
            if self.x - self.velocidad > self.camino[1]:
                self.x -= self.velocidad
                self.va_derecha = False
                self.va_izquierda = True
            else:
                self.velocidad = self.velocidad * -1
                self.contador_pasos = 0
        else:
            if self.x - self.velocidad < self.camino[0]:
                self.x -= self.velocidad
                self.va_izquierda = False
                self.va_derecha = True
            else:
                self.velocidad = self.velocidad * -1
                self.contador_pasos = 0


camara_x = 0
def repintar_cuadro_juego():
    global camara_x
    ventana.blit(imagen_fondo, (camara_x, 0))
    #mover la camara inmediatamente
    # camara_x = -heroe.x
    camara_x += ((-heroe.x + 100) - camara_x) / 15
    #dibujar personaje
    heroe.dibujar(ventana)
    gato.dibujar(ventana)

    pygame.display.update()

# Inicio funcion principal
repetir = True
while repetir:

    #inicializacion de elementos del juego
    imagen_fondo = pygame.image.load("img/fondo.png")

    #creacion personaje heroe
    heroe = personaje(100, ventana_y - 200, "heroe", ventana_x)
    gato = personaje(1200, ventana_y - 100, "villano", 200)

    #seccion del juego 
    esta_jugando = True
    #control de la velocidad del juego
    while esta_jugando:
        reloj.tick(18)
        #evento de cierre
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
        #evento de movimiento del personaje
        teclas = pygame.key.get_pressed()
        heroe.se_mueve_segun(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE)
        gato.se_mueve_solo()
        repintar_cuadro_juego() 
#termina el juego
pygame.quit()