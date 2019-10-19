import numpy as np
import random
import pygame
import sys
import math

PLAYER = 0
AI = 1
PRAZNO_POLJE = 0
PLAYER_TOKEN = 1
AI_TOKEN = 2

BELA = (255,255,255)
SIVA = (200,200,200)
CRNA = (0,0,0)
ZUTA = (255,255,0)

BROJ_REDOVA = 6
BROJ_KOLONA = 6
POVRSINA_ZA_POBEDU = 4


#F-ja koja kreira matricu 6 puta 6 koja predstavlja tablu
def kreiraj_tablu():
	tabla = np.zeros((BROJ_REDOVA,BROJ_KOLONA))
	return tabla

#F-ja koja stampa tablu u konzolu
def stampaj_tablu(tabla):
	print(np.flip(tabla, 0))

def postavi_token(tabla, red, kolona, token):
	tabla[red][kolona] = token

#Proveravamo da li je 5 red prosledjene kolone slobodan, tj necemo dozvoliti da se odigra u punu kolonu
def da_li_je_popunjena_kolona(tabla, kolona):
	return tabla[BROJ_REDOVA-1][kolona] == 0

#vraca nam index prvog slobodnog reda
def get_sledeci_slobodan_red(tabla, kolona):
	for r in range(BROJ_REDOVA):
		if tabla[r][kolona] == 0:
			return r

def winning_move(tabla, token):
	# proveri horizontalne lokacije
	for c in range(BROJ_KOLONA-3):
		for r in range(BROJ_REDOVA):
			if tabla[r][c] == token and tabla[r][c+1] == token and tabla[r][c+2] == token and tabla[r][c+3] == token:
				return True

	# proveri vertikalne lokacije
	for c in range(BROJ_KOLONA):
		for r in range(BROJ_REDOVA-3):
			if tabla[r][c] == token and tabla[r+1][c] == token and tabla[r+2][c] == token and tabla[r+3][c] == token:
				return True

	# proveri dijagonalno pozitivne lokacije
	for c in range(BROJ_KOLONA-3):
		for r in range(BROJ_REDOVA-3):
			if tabla[r][c] == token and tabla[r+1][c+1] == token and tabla[r+2][c+2] == token and tabla[r+3][c+3] == token:
				return True

	#proveri dijagonalno negativne lokacije
	for c in range(BROJ_KOLONA-3):
		for r in range(3, BROJ_REDOVA):
			if tabla[r][c] == token and tabla[r-1][c+1] == token and tabla[r-2][c+2] == token and tabla[r-3][c+3] == token:
				return True

def proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token):
	score = 0
	protivnicki_token = PLAYER_TOKEN
	if token == PLAYER_TOKEN:
		protivnicki_token = AI_TOKEN

	if povrsina_za_pobedu.count(token) == 4:
		score += 100
	elif povrsina_za_pobedu.count(token) == 3 and povrsina_za_pobedu.count(PRAZNO_POLJE) == 1:
		score += 5
	elif povrsina_za_pobedu.count(token) == 2 and povrsina_za_pobedu.count(PRAZNO_POLJE) == 2:
		score += 2

	if povrsina_za_pobedu.count(protivnicki_token) == 3 and povrsina_za_pobedu.count(PRAZNO_POLJE) == 1:
		score -= 4

	return score

def score_position(tabla, token):
	score = 0

	## Boduj centralnu kolonu
	center_array = [int(i) for i in list(tabla[:, BROJ_KOLONA//2])]
	centaralni_brojac = center_array.count(token)
	score += centaralni_brojac * 3

	## Boduj horizontalno
	for r in range(BROJ_REDOVA):
		red_array = [int(i) for i in list(tabla[r,:])]
		for c in range(BROJ_KOLONA-3):
			povrsina_za_pobedu = red_array[c:c+POVRSINA_ZA_POBEDU]
			score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

	## Boduj vertiaklno u pozitivno smeru(na gore)
	for c in range(BROJ_KOLONA):
		kolona_array = [int(i) for i in list(tabla[:,c])]
		for r in range(BROJ_REDOVA-3):
			povrsina_za_pobedu = kolona_array[r:r+POVRSINA_ZA_POBEDU]
			score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

	## Boduj vertiaklno u negativnom smeru(na dole)
	for r in range(BROJ_REDOVA-3):
		for c in range(BROJ_KOLONA-3):
			povrsina_za_pobedu = [tabla[r+i][c+i] for i in range(POVRSINA_ZA_POBEDU)]
			score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

	for r in range(BROJ_REDOVA-3):
		for c in range(BROJ_KOLONA-3):
			povrsina_za_pobedu = [tabla[r+3-i][c+i] for i in range(POVRSINA_ZA_POBEDU)]
			score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

	return score

def is_terminal_node(tabla):
	return winning_move(tabla, PLAYER_TOKEN) or winning_move(tabla, AI_TOKEN) or len(get_validne_lokacije(tabla)) == 0

def minimax(tabla, depth, alpha, beta, maximizingPlayer):
	validne_lokacije = get_validne_lokacije(tabla)
	is_terminal = is_terminal_node(tabla)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(tabla, AI_TOKEN):
				return (None, 100000000000000)
			elif winning_move(tabla, PLAYER_TOKEN):
				return (None, -10000000000000)
			else: # Kraj igre, zatos to nema vise validnih poteza
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(tabla, AI_TOKEN))
	if maximizingPlayer:
		value = -math.inf
		kolonaumn = random.choice(validne_lokacije)
		for kolona in validne_lokacije:
			red = get_sledeci_slobodan_red(tabla, kolona)
			b_copy = tabla.copy()
			postavi_token(b_copy, red, kolona, AI_TOKEN)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				kolonaumn = kolona
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return kolonaumn, value

	else: # Minimizing player
		value = math.inf
		kolonaumn = random.choice(validne_lokacije)
		for kolona in validne_lokacije:
			red = get_sledeci_slobodan_red(tabla, kolona)
			b_copy = tabla.copy()
			postavi_token(b_copy, red, kolona, PLAYER_TOKEN)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				kolonaumn = kolona
			beta = min(beta, value)
			if alpha >= beta:
				break
		return kolonaumn, value
#funkcija koja trazi sve validne(prazne) lokacije i smesta ih u niz, npr ako ako ni jedna kolona nije popunjena niz izgleda valid_location = [0,1,2,3,4,5]
def get_validne_lokacije(tabla):
	validne_lokacije = []
	for kolona in range(BROJ_KOLONA):
		if da_li_je_popunjena_kolona(tabla, kolona):
			validne_lokacije.append(kolona)
	return validne_lokacije

def izaberi_najbolji_potez(tabla, token):

	validne_lokacije = get_validne_lokacije(tabla)
	best_score = -10000
	best_kolona = random.choice(validne_lokacije)
	for kolona in validne_lokacije:
		red = get_sledeci_slobodan_red(tabla, kolona)
		temp_tabla = tabla.copy()
		postavi_token(temp_tabla, red, kolona, token)
		score = score_position(temp_tabla, token)
		if score > best_score:
			best_score = score
			best_kolona = kolona

	return best_kolona

def iscrtaj_tablu(tabla):
	for c in range(BROJ_KOLONA):
		for r in range(BROJ_REDOVA):
			pygame.draw.rect(screen, BELA, (c*VELICINA_KVADRATA, r*VELICINA_KVADRATA+VELICINA_KVADRATA, VELICINA_KVADRATA, VELICINA_KVADRATA))
			pygame.draw.circle(screen, SIVA, (int(c*VELICINA_KVADRATA+VELICINA_KVADRATA/2), int(r*VELICINA_KVADRATA+VELICINA_KVADRATA+VELICINA_KVADRATA/2)), RADIUS)
	
	for c in range(BROJ_KOLONA):
		for r in range(BROJ_REDOVA):		
			if tabla[r][c] == PLAYER_TOKEN:
				pygame.draw.circle(screen, CRNA, (int(c*VELICINA_KVADRATA+VELICINA_KVADRATA/2), height-int(r*VELICINA_KVADRATA+VELICINA_KVADRATA/2)), RADIUS)
			elif tabla[r][c] == AI_TOKEN: 
				pygame.draw.circle(screen, ZUTA, (int(c*VELICINA_KVADRATA+VELICINA_KVADRATA/2), height-int(r*VELICINA_KVADRATA+VELICINA_KVADRATA/2)), RADIUS)
	pygame.display.update()

tabla = kreiraj_tablu()
stampaj_tablu(tabla)
game_over = False

pygame.init()

VELICINA_KVADRATA = 90

width = BROJ_KOLONA * VELICINA_KVADRATA
height = (BROJ_REDOVA+1) * VELICINA_KVADRATA

size = (width, height)

RADIUS = int(VELICINA_KVADRATA/2 - 5)

screen = pygame.display.set_mode(size)
iscrtaj_tablu(tabla)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 55)

turn = random.randint(PLAYER, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BELA, (0,0, width, VELICINA_KVADRATA))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, CRNA, (posx, int(VELICINA_KVADRATA/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BELA, (0,0, width, VELICINA_KVADRATA))


			if turn == PLAYER:
				posx = event.pos[0]
				kolona = int(math.floor(posx/VELICINA_KVADRATA))

				if da_li_je_popunjena_kolona(tabla, kolona):
					red = get_sledeci_slobodan_red(tabla, kolona)
					postavi_token(tabla, red, kolona, PLAYER_TOKEN)

					if winning_move(tabla, PLAYER_TOKEN):
						label = myfont.render("POBEDILI STE!!!", 1, CRNA)
						screen.blit(label, (10,5))
						game_over = True

					turn += 1
					turn = turn % 2

					stampaj_tablu(tabla)
					iscrtaj_tablu(tabla)


	if turn == AI and not game_over:				

		kolona, minimax_score = minimax(tabla, 5, -math.inf, math.inf, True)

		if da_li_je_popunjena_kolona(tabla, kolona):

			red = get_sledeci_slobodan_red(tabla, kolona)
			postavi_token(tabla, red, kolona, AI_TOKEN)

			if winning_move(tabla, AI_TOKEN):
				label = myfont.render("AI je pobedio :(", 1, ZUTA)
				screen.blit(label, (10,5))
				game_over = True

			stampaj_tablu(tabla)
			iscrtaj_tablu(tabla)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)