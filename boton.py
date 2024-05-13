class Boton:
	def __init__(self, imagen=None, posicion=(0, 0), texto="", font=None, color_principal=None, color_sobrepuesto=None):
		self.imagen = imagen
		self.posicion_x = posicion[0]
		self.posicion_y = posicion[1]
		self.font = font
		self.color_principal = color_principal
		self.color_sobrepuesto =  color_sobrepuesto
		self.texto_input = texto
		self.texto = self.font.render(self.texto_input, False, self.color_principal)
		if self.imagen is None:
			self.imagen = self.texto
		self.rect = self.imagen.get_rect(center=(self.posicion_x, self.posicion_y))
		self.texto_rect = self.texto.get_rect(center=(self.posicion_x, self.posicion_y))

	def actualizar(self, pantalla):
		if self.imagen is not None:
			pantalla.blit(self.imagen, self.rect)
		pantalla.blit(self.texto, self.texto_rect)

	def obtener_evento(self, posicion):
		if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def cambiar_color(self, posicion):
		if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.bottom):
			self.texto = self.font.render(self.texto_input, True, self.color_sobrepuesto)
		else:
			self.texto = self.font.render(self.texto_input, True, self.color_principal)
