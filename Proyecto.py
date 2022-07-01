import os

print("Bienvevnido a su consulta Bancaria. ")

# c = 5467

# x = int(input("ingrese su contraseña: "))
def contraseña():
	contra = False
	# respuesta = None
	while contra == False :
		try:
			passs = input("Ingrese su contraseña: ")
			# print("la contra es:",contra)
		except ValueError:
			print("Tienes que ingresar la contra correcta.")
		# 	respuesta=input("Desea ingresar otro par de valores?[s/n]")
		# if respuesta=="n":
		if passs == "54689":
			contra = True


	# contador = 54689
	# contra = 54689
	# while contador = contra:
	# 	print("Contraseña correcta")



	# if (x == c):

	# 	print("contraseña correcta")
	# else:
	# 	print("contraseña incorrecta")

contraseña()

# os.system("clear")

# def menu():
# 	print("menu")
# 	print("1. Depositar")
# 	print("2. Retirar")
# 	print("3. Consulta de saldo")
# 	print("4. Salir")
# 	opcion= int (input("escoja opcion: "))
# menu()

# monto=50000

# def depositar():
# 	if opcion == 1:
# 	dep = int(input("Ingrese su monto a depositar: "))
# 	print("Su deposito fue de: ",dep)
# depositar()

# input("")
# os.system("clear")

# def retirar():
# 	if opcion == 2:
# 	retirar=int(input("cuanto desea agregar: "))
# 	print("su monto actual es", monto - retirar)
# 	print("usted a retirado" , retirar)
# retirar()

# input("")

# os.system("clear")


# def ver():
# 	if opcion == 3:
# 	print("su saldo es" , monto)
# ver()


# sin def


# """cajero automatico"""
# import os
# name="claudio"
# print("bienvenido")

# contra = "5467"

# pasword=int(input("ingrese su contraseña:"))



# if pasword == contra:
# 	print("contraseña correcta","bienvenido",name)


# else:
# 	print("contraseña incorrecta")




"""menu"""
os.system("clear")
print("menu")
print("1.depositar")
print("2.retirar")
print("3.ver saldo")
opcion= int (input("escoja opcion: "))


os.system("clear")

#deposito
if opcion == 1:
	depositar=int(input("cuanto desea depositar:"))

	print("usted a depositado",depositar)


#retirar dinero
saldo = 50000

if opcion==2:
	giro=int(input("cuanto desea retirar:"))
	print("su saldo actual es" , saldo - giro)
	print("usted a retirado" , giro)

#ver saldo
if opcion==3:
	print("su saldo es", saldo)