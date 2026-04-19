import pygame

pygame.init()
ventana_x = 1366
ventana_y = 700

ventana = pygame.display.set_mode((ventana_x, ventana_y))
pygame.display.set_caption("Moni")
reloj = pygame.time.Clock()

#importar imagenes
corazon_vacio = pygame.image.load("img\heart\heart_vacio.png")
corazon_creciente = pygame.image.load("img\heart\heart_creciente.png")
corazon_medio = pygame.image.load("img\heart\heart_medio.png")
corazon_cuarto = pygame.image.load("img\heart\heart_cuarto.png")
corazon_lleno = pygame.image.load("img\heart\heart_lleno.png")
#clase personaje
class personaje(object):

    def __init__(self, x, y, fuente, limite):
        self.x = x
        self.y = y
        self.velocidad = 15
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
        self.salud = 100
        #Hitbox
        self.zona_impacto = (self.x, self.y + 10, self.ancho, self.alto)
        

    def dibujar(self, cuadro):
        if self.contador_pasos + 1 > 6:
            self.contador_pasos = 0
        if self.va_izquierda:
            cuadro.blit(self.camina_izquierda[self.contador_pasos], (self.x, self.y))
            self.contador_pasos +=1
        elif self.va_derecha:
            cuadro.blit(self.camina_derecha[self.contador_pasos], (self.x, self.y))
            self.contador_pasos +=1
        else:
            cuadro.blit(self.quieto, (self.x, self.y))
        
        # crear clase barra de vida
        # if self.salud == 100:
        #     self.corazon_cuarto = pygame.image.load("img\heart\heart_cuarto.png")
        #     self.ancho = self.corazon_cuarto.get_width()
        #     self.alto = self.corazon_cuarto.get_height()
        #     self.corazon_cuarto.blit(corazon_cuarto,(self.x + 5, self.y - 20))
        # else:
        #     corazon_cuarto = pygame.image.load("img\heart\heart_cuarto.png")
        #     self.ancho = corazon_cuarto.get_width()
        #     self.alto = corazon_cuarto.get_height()
        #     corazon_cuarto.blit(corazon_cuarto,(self.x + 5, self.y - 20))
        pygame.draw.rect(cuadro, (255, 0, 0), (self.x + 5, self.y -20, 50, 10))
        pygame.draw.rect(cuadro, (0, 128, 0), (self.x + 5, self.y -20, 50 - (5 * (100 - self.salud)*0.1), 10))

        #dibujo del hitbox
        self.zona_impacto = (self.x, self.y + 10, self.ancho, self.alto)
        # pygame.draw.rect(cuadro, (255, 0, 0), self.zona_impacto, 2)

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
            self.va_derecha = False
            self.va_izquierda = False
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

    #deteccion de colisiones
    def se_encuentra_con(self, alguien):
        R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
        R1_ar = self.zona_impacto[1]
        R1_iz = self.zona_impacto[0]
        R1_de = self.zona_impacto[0] + self.zona_impacto[2]
        R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
        R2_ar = alguien.zona_impacto[1]
        R2_iz = alguien.zona_impacto[0]
        R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

        return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

    #Heroe recibe golpe de daño
    def es_golpeado(self):
        self.ha_saltado = False
        self.impulso_salto = 8
        self.x = 100
        self.y = 480
        self.contador_pasos = 0
        gato.salud += 20
        pygame.time.delay(2000)
    
class proyectil(object):
    def __init__(self, x, y , radio, color, direccion):
        self.x = x
        self.y = y
        # self.radio = radio
        # self.color = color
        self.direccion = direccion
        self.velocidad = 20 * direccion
        # self.zona_impacto = (self.x -self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        self.corazon = pygame.image.load("img\heart\heart_lleno.png")
        self.ancho = self.corazon.get_width()
        self.alto = self.corazon.get_height()
        self.zona_impacto = (self.x, self.y, self.ancho, self.alto)
        
        
    
    def dibujar(self, cuadro):
        self.zona_impacto = (self.x, self.y, self.ancho, self.alto)
        # self.zona_impacto = (self.x -self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        # pygame.draw.circle(cuadro, self.color, (self.x, self.y), self.radio)
        cuadro.blit(self.corazon, (self.x, self.y))
        #en caso de querer visualizar la zona de impacto
        # pygame.draw.rect(cuadro, (255, 0, 0), self.zona_impacto, 2)

    def impacta_a(self, alguien):
        if alguien.salud >=0:
            alguien.salud -= 5
        else:
            del(alguien)
            


def repintar_cuadro_juego():
    ventana.blit(imagen_fondo, (0, 0))
    
    #dibujar personaje
    heroe.dibujar(ventana)
    #dibujar gato
    gato.dibujar(ventana)
    #dibujar balas
    for bala in balas:
        bala.dibujar(ventana)

    #dibujar los corazones
    vida_jugador()
    #se refresca la imagen
    pygame.display.update()

def vida_jugador():
    c_mitad_dibujado = False
    for i in range(4):
        if gato.salud >= ((i*1)*25):
            ventana.blit(corazon_vacio, (5+i*50, 5))
        elif gato.salud % 25 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_medio, (5+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_lleno, (5 + i * 50, 5))

# Inicio funcion principal
repetir = True
while repetir:

    #inicializacion de elementos del juego
    imagen_fondo = pygame.image.load("img/fondo.png")

    #variables para las figuras
    

    #variables del personaje

    #creacion personaje heroe
    heroe = personaje(100, ventana_y - 230, "heroe", ventana_x)
    gato = personaje(1200, ventana_y - 100, "villano", 200)

    #variables balas
    tanda_disparos = 0
    balas = []

    #seccion del juego 
    esta_jugando = True
    #control de la velocidad del juego
    while esta_jugando:
        reloj.tick(60)
        #evento de cierre
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
        #evento de movimiento del personaje
        teclas = pygame.key.get_pressed()
        heroe.se_mueve_segun(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE)
        gato.se_mueve_solo()
        
        #verificar si choca el heroe con el gato
        if heroe.se_encuentra_con(gato):
            heroe.es_golpeado()
        
        # if heroe.colliderect(gato):
        #     heroe.es_golpeado()

        #manejo de los disparos
        if tanda_disparos >0:
            tanda_disparos += 1
        if tanda_disparos > 3:
            tanda_disparos = 0

        #contacto del proyectil contra el gato
        for bala in balas:
            if gato.se_encuentra_con(bala):
                bala.impacta_a(gato)
                balas.pop(balas.index(bala))
            #movimiento dentro de los limites de la ventana
            if bala.x < ventana_x and bala.x > 0:
                bala.x += bala.velocidad
            else:
                balas.pop(balas.index(bala))
        #capturar evento de disparos
        if teclas[pygame.K_x] and tanda_disparos == 0:
            if heroe.va_izquierda:
                direccion = -1
            elif heroe.va_derecha:
                direccion = 1
            else:
                direccion = 1
            if len(balas) < 5: #balas en pantalla
                balas.append(proyectil(round(heroe.x + heroe.ancho // 2), round(heroe.y + heroe.alto - 10), 6, (0,0,0), direccion))
            tanda_disparos = 1
        repintar_cuadro_juego()
    print(gato.salud)
    if gato.salud < 0:
        esta_jugando == False

#termina el juego
pygame.quit()