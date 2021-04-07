import socket as sock
from constantes import *

class Servidor:
	def __init__(self, porta_servidor):
		self.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
		self.socket.bind(('', porta_servidor))
		self.porta_servidor = porta_servidor
		self.clientes = []

	def receber_mensagem(self):
		mensagem, endereco = self.socket.recvfrom(2048)
		mensagem_decodificada = mensagem.decode()

		try:
			mensagem_final = int(mensagem_decodificada)
		except ValueError as error:
			mensagem_final = mensagem_decodificada

		pacote = {'mensagem': mensagem_final, 'endereco': endereco}
		return pacote

	def enviar_mensagem(self, mensagem, destino):
		if type(mensagem) == str: 
			mensagem_byte = mensagem.encode()
		else:
			mensagem_byte = str(mensagem).encode()
		self.socket.sendto(mensagem_byte, destino)

def calcular_vencedor(jogadas):
	print(jogadas)
	total = 0
	for jogada in jogadas:
		total += jogada['numero']

	if total % 2 == 0:
		resultado_vencedor = MSG_PAR
	else:
		resultado_vencedor = MSG_IMPAR

	resultado_final = []
	for jogada in jogadas:
		if jogada['jogada'] == resultado_vencedor:
			resultado = MSG_VENCEDOR
		else:
			resultado = MSG_PERDEDOR
		resultado_final.append(resultado)
	return resultado_final

def main():
	servidor = Servidor(9000)

	TOTAL_JOGADORES = 2
	lista_jogadores = []
	numero_jogadores = 0
	primeiro_ajogar = 1
	ultimo_ajogar = 0

	while True:
		esperando_jogadores = True
		while esperando_jogadores:
			pacote = servidor.receber_mensagem()

			if pacote['mensagem'] == MSG_ENTRAR_PARTIDA:
				lista_jogadores.append(pacote['endereco'])

				servidor.enviar_mensagem(MSG_ENTRADA_ACEITA, pacote['endereco'])
				numero_jogadores += 1

				if numero_jogadores == TOTAL_JOGADORES:
					esperando_jogadores = False

		while numero_jogadores == TOTAL_JOGADORES:
			[primeiro_ajogar, ultimo_ajogar] = [ultimo_ajogar, primeiro_ajogar]
			ordem_jogadores = [primeiro_ajogar, ultimo_ajogar]

			lista_jogadas = []
			for jogador in ordem_jogadores:
				if jogador == ordem_jogadores[0]:
					servidor.enviar_mensagem(MSG_REQUISITAR_JOGADA, lista_jogadores[jogador])
					pacote = servidor.receber_mensagem()
					jogada = pacote['mensagem']
				else:
					if lista_jogadas[0]['jogada'] == MSG_IMPAR:
						jogada = MSG_PAR
					else:
						jogada = MSG_IMPAR

				servidor.enviar_mensagem(MSG_REQUISITAR_NUMERO, lista_jogadores[jogador])
				pacote = servidor.receber_mensagem()
				numero = pacote['mensagem']
				lista_jogadas.append({'jogada': jogada, 'numero': numero})

			resultado_final = calcular_vencedor(lista_jogadas)
			for resultado, jogador in zip(resultado_final, ordem_jogadores):
				servidor.enviar_mensagem(resultado, lista_jogadores[jogador])

if __name__ == '__main__':
	main()