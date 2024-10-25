from random import randint
# Diccionario global para almacenar los usuarios
users = {}

# Variable global para almacenar el usuario actual loggeado
current_user = None

# Función para guardar los datos en un archivo de texto
def saveData():
    try:
        with open('users_data.txt', 'w') as file:
            for name, data in users.items():
                line = f"{name}:{data['password']}:{data['score']}:{data['logged_in']}\n"
                file.write(line)
    except Exception as e:
        print(f"Error guardando los datos: {e}")

# Función para cargar los datos desde un archivo de texto
def loadData():
    global users
    try:
        with open('users_data.txt', 'r') as file:
            for line in file:
                name, password, score, logged_in = line.strip().split(':')
                users[name] = {
                    'password': password,
                    'score': int(score),
                    'logged_in': logged_in == 'True'
                }
    except FileNotFoundError:
        print("El archivo no existe. Creando nuevo archivo.")
        users = {}
    except Exception as e:
        print(f"Error cargando los datos: {e}")
        users = {}

# Función para registrar un usuario con nombre y contraseña
def registerUser(name, password):
    if name in users:
        return "User already exists"
    users[name] = {'password': password, 'score': 0, 'logged_in': False}
    saveData()
    return "User registered successfully"

# Función que abre o cierra una sesión
def openCloseSession(name, password, flag):
    global current_user



    if name in users and users[name]['password'] == password:
        if flag == "open" and not users[name]['logged_in']:
            users[name]['logged_in'] = True
            current_user = name
            saveData()
            return "Session was successfully opened"
        elif flag == "close" and users[name]['logged_in']:
            users[name]['logged_in'] = False
            current_user = None
            saveData()
            return "Session was successfully closed"
        else:
            return "error"
    return "error"

# Función que permite la actualización del puntaje
def updateScore(score):
    if current_user:
        users[current_user]['score'] = score
        saveData()
        return "Score was successfully updated"
    return "error"

# Función que retorna y/o muestra el puntaje del usuario
def getScore():
    if current_user:
        return users[current_user]['score']
    return "error"

# Función que retorna la lista de usuarios conectados
def usersList():
    connected_users = [(user, data['score']) for user, data in users.items() if data['logged_in']]
    if connected_users:
        return connected_users
    return "Error: No users connected"

# Función que genera una pregunta en una categoría
def question(cat):
    question_answers = {}
    if current_user:
     try:
      file2=open('q.txt', 'r')
      contenido = file2.readlines()
      question_answers = contenido
      for line in question_answers:
          line.strip().split(',')
      return definecategory(cat,question_answers)
      
     except FileNotFoundError:
        print("El archivo no existe. Creando nuevo archivo.")
        
        raise ValueError("Programador, cree el archivo y alimentelo con las preguntas, guardelo en bibliotecas (Aún no se cómo hacerlas)")
    
    return "error: No user logged in"

def definecategory(option,Questions_answers):
    option=randint(1,2)
    if (option==1):
     question=randint(0,9)
     print(f"Question #{question+1} from the sports section")
    else:
        question=randint(10,19)
        print(f"Question #{question-9} from the Geography section")
    
    cat = Questions_answers[question][0]
    return cat
    #while (answer!="a" and answer!="b" and answer!="c" and answer!="d"): 
     #   answer=str(input("Choose a, b, c or d, any other letter or character isn't permitted")).lower()





# Función interactiva para probar el sistema
def menu():
    global current_user
    while True:
        print("\nMENU:")
        print("1. Registrar Usuario")
        print("2. Iniciar Sesión")
        print("3. Cerrar Sesión")
        print("4. Actualizar Puntaje")
        print("5. Ver Puntaje")
        print("6. Ver Usuarios Conectados")
        print("7. Hacer Pregunta")
        print("8. Salir")
        
        choice = input("\nSelecciona una opción: ")
        match choice:
            case "1":
                name = input("Ingresa el nombre de usuario: ")
                password = input("Ingresa la contraseña: ")
                print(registerUser(name, password))
            
            case "2":
                if current_user:
                    print(f"Ya hay un usuario loggeado: {current_user}")
                else:
                    name = input("Ingresa el nombre de usuario: ")
                    password = input("Ingresa la contraseña: ")
                    print(openCloseSession(name, password, "open"))
            
            case "3":
                if current_user:
                    print(openCloseSession(current_user, users[current_user]['password'], "close"))
                else:
                    print("No hay ningún usuario loggeado.")
            
            case "4":
                if current_user:
                    score = int(input("Ingresa el nuevo puntaje: "))
                    print(updateScore(score))
                else:
                    print("error: No user logged in")

            case "5":
                print("Puntaje: ", getScore())
            
            case "6":
                print("Connecter Users",usersList())
            
            case "7":
                if current_user:
                    cat = randint(1,2)
                    print("Pregunta: ", question(cat))
                else:
                    print("error: No user logged in")

            case "8":
                print("Saliendo...")
                break
            
            case _:
                print("Opción no válida. Inténtalo de nuevo.")

# Cargar los datos al iniciar el programa
loadData()

# Ejecutar el menú interactivo
menu()