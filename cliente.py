import socket as sock
from constantes import *

nome_servidor = '192.168.0.7'
porta_servidor = 9000

class Cliente:
	def __init__(self, nome_servidor, porta_servidor):
		self.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
		self.endereco_servidor = (nome_servidor, porta_servidor)

	def enviar_mensagem(self, mensagem):
		if type(mensagem) == str: 
			mensagem_byte = mensagem.encode()
		else:
			mensagem_byte = str(mensagem).encode()
		self.socket.sendto(mensagem_byte, self.endereco_servidor)

	def receber_mensagem(self):
		mensagem, endereco = self.socket.recvfrom(2048)

		if endereco == self.endereco_servidor:
			mensagem_decodificada = mensagem.decode()
			try:
				mensagem_final = int(mensagem_decodificada)
			except ValueError as error:
				mensagem_final = mensagem_decodificada
			except Exception as error:
				print(error)
		return mensagem_final

def main():
	cliente = Cliente(nome_servidor, porta_servidor)

	while True:
		print('Deseja continuar? [s/n]')
		entrada = input('>> ')
		if entrada == 'n':
			break
		elif entrada != 's':
			print('Entrada inválida')
			continue

		cliente.enviar_mensagem(MSG_ENTRAR_PARTIDA)
		mensagem = cliente.receber_mensagem()
		if mensagem == MSG_ENTRADA_ACEITA:
			print('Entrando partida...')
			empartida = True

		while empartida:
			mensagem = cliente.receber_mensagem()
			if mensagem == MSG_REQUISITAR_JOGADA:
				print('## ESCOLHA UMA OPÇÃO')
				print('[1] par')
				print('[2] ímpar')
				entrada = input(">> ")

				if entrada == '1':
					cliente.enviar_mensagem(MSG_PAR)
				elif entrada == '2':
					cliente.enviar_mensagem(MSG_IMPAR)
				else:
					print('Entrada inválida.')

			if mensagem == MSG_REQUISITAR_NUMERO:
				print('## DIGITE UM NÚMERO ENTRE 0 e 10')
				entrada = input('>> ')

				try:
					numero = int(entrada)
				except ValueError as e:
					print('Entrada inválida')
				else:
					if numero > 10 or numero < 0:
						print('Entrada inválida')
					cliente.enviar_mensagem(numero)

			if mensagem == MSG_VENCEDOR:
				print('Você venceu.')

			if mensagem == MSG_PERDEDOR:
				print('Você perdeu.')



if __name__ == '__main__':
	main()