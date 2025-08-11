import random

class Character:
    def __init__(self, hp, damage, defense, crit_chance):
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.defense = defense
        self.crit_chance = crit_chance
        self.abilities = []
        self.used_abilities = []
    
    def attack(self, target):
        damage_dealt = self.damage
        if random.random() < self.crit_chance:
            damage_dealt *= 2
            print("¡Golpe crítico!")
        
        actual_damage = max(1, damage_dealt - (target.defense * damage_dealt))
        target.hp -= actual_damage
        return actual_damage
    
    def use_ability(self, ability_index, target):
        if ability_index >= len(self.abilities):
            return 0
        
        ability = self.abilities[ability_index]
        
        if ability['uses'] <= 0:
            print("¡No te quedan usos para esta habilidad!")
            return 0
        
        ability['uses'] -= 1
        effect = ability['effect']
        
        if effect['type'] == 'damage':
            damage = effect['value']
            if random.random() < self.crit_chance:
                damage *= 2
                print("¡Golpe crítico!")
            
            actual_damage = max(1, damage - (target.defense * damage))
            target.hp -= actual_damage
            print(f"¡Habilidad {ability['name']} usada! Causó {actual_damage} de daño.")
            return actual_damage
        
        elif effect['type'] == 'heal':
            heal_amount = min(effect['value'], self.max_hp - self.hp)
            self.hp += heal_amount
            print(f"¡Habilidad {ability['name']} usada! Recuperaste {heal_amount} de HP.")
            return heal_amount
        
        elif effect['type'] == 'buff':
            self.damage += effect['value']
            print(f"¡Habilidad {ability['name']} usada! Aumentó tu daño en {effect['value']}.")
            return effect['value']
        
        return 0

def mostrar_roles():
    print("\nROLES DISPONIBLES:")
    print("1. Rogue: daño alto, baja defensa, vida media")
    print("   Habilidades: Ataque sigiloso (doble daño, 1 ), Esquivar (aumenta defensa, 2 )")
    print("2. Tank: daño medio, defensa alta, vida normal, crítico")
    print("   Habilidades: Golpe fortificado (daño + defensa, 2 ), Proteger (reduce daño recibido, 1)")
    print("3. Wizard: daño bajo, defensa baja, vida alta, crítico")
    print("   Habilidades: Bola de fuego (daño alto, 1), Curación (recupera HP, 2 )")
    print("4. Paladin: daño bajo, defensa alta, vida baja, crítico")
    print("   Habilidades: Golpe sagrado (daño + curación, 2), Escudo divino (reduce daño, 1)")

def crear_jugador(nombre, rol):
    if rol == "rogue":
        character = Character(100, 25, 0.1, 0.4)
        character.abilities = [
            {'name': 'Ataque sigiloso', 'uses': 1, 'effect': {'type': 'damage', 'value': 50}},
            {'name': 'Esquivar', 'uses': 2, 'effect': {'type': 'buff', 'value': 0.2}}
        ]
    elif rol == "tank":
        character = Character(150, 15, 0.4, 0.2)
        character.abilities = [
            {'name': 'Golpe fortificado', 'uses': 2, 'effect': {'type': 'damage', 'value': 30}},
            {'name': 'Proteger', 'uses': 1, 'effect': {'type': 'buff', 'value': 0.3}}
        ]
    elif rol == "wizard":
        character = Character(200, 10, 0.1, 0.3)
        character.abilities = [
            {'name': 'Bola de fuego', 'uses': 1, 'effect': {'type': 'damage', 'value': 40}},
            {'name': 'Curación', 'uses': 2, 'effect': {'type': 'heal', 'value': 50}}
        ]
    elif rol == "paladin":
        character = Character(80, 12, 0.5, 0.2)
        character.abilities = [
            {'name': 'Golpe sagrado', 'uses': 2, 'effect': {'type': 'damage', 'value': 20}},
            {'name': 'Escudo divino', 'uses': 1, 'effect': {'type': 'buff', 'value': 0.4}}
        ]
    else:
        print("Rol inválido. Se asigna Rogue por defecto.")
        character = Character(100, 25, 0.1, 0.4)
        character.abilities = [
            {'name': 'Ataque sigiloso', 'uses': 1, 'effect': {'type': 'damage', 'value': 50}},
            {'name': 'Esquivar', 'uses': 2, 'effect': {'type': 'buff', 'value': 0.2}}
        ]
    
    character.nombre = nombre
    character.rol = rol
    return character

def esta_vivo(personaje):
    return personaje.hp > 0

def elegir_objetivo(jugador_idx, jugadores, nombres):
    print(f"\nTurno de {nombres[jugador_idx]}. ¿A quién quieres atacar?")
    opciones = []
    for i, j in enumerate(jugadores):
        if i != jugador_idx and esta_vivo(j):
            print(f"{len(opciones)+1}. {nombres[i]} (HP: {j.hp}/{j.max_hp})")
            opciones.append(i)
    
    if not opciones:
        return -1
    
    while True:
        try:
            eleccion = int(input("Número del jugador a atacar: ")) - 1
            if 0 <= eleccion < len(opciones):
                return opciones[eleccion]
            print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número.")

def elegir_accion(jugador):
    print(f"\nAcciones disponibles para {jugador.nombre} ({jugador.rol}):")
    print("1. Ataque normal")
    
    for i, ability in enumerate(jugador.abilities):
        if ability['uses'] > 0:
            print(f"{i+2}. {ability['name']} (Usos restantes: {ability['uses']})")
    
    while True:
        try:
            eleccion = int(input("Elige una acción: "))
            if 1 <= eleccion <= len(jugador.abilities) + 1:
                return eleccion - 1  
            print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número.")

def mostrar_ganadores(jugadores, nombres):
    vivos = [i for i in range(len(jugadores)) if esta_vivo(jugadores[i])]
    if len(vivos) == 0:
        print("¡Todos han perdido!")
    elif len(vivos) == 1:
        print(f"¡El ganador es {nombres[vivos[0]]} con {jugadores[vivos[0]].hp} HP!")
    else:
        print("¡Empate entre los siguientes jugadores!")
        for i in vivos:
            print(f"- {nombres[i]} (HP: {jugadores[i].hp})")

print("Bienvenido al juego por turnos entre 2 a 4 jugadores.")
num_jugadores = int(input("¿Cuántos jugadores? (2-4): "))

jugadores = []
nombres = []

for i in range(num_jugadores):
    print(f"\nJugador {i + 1}:")
    nombre = input("Ingresa tu nombre: ")
    mostrar_roles()
    rol = input("Elige tu rol (rogue/tank/wizard/paladin): ").lower()
    jugador = crear_jugador(nombre, rol)
    jugadores.append(jugador)
    nombres.append(nombre)

orden = list(range(num_jugadores))
random.shuffle(orden)

print("\nOrden de turnos aleatorio:")
for i in orden:
    print(f"- {nombres[i]}")

n_turns = int(input("\n¿Cuántos turnos deseas jugar?: "))

for turno in range(n_turns):
    print(f"\n--- TURNO {turno + 1} ---")
    
    for i in orden:
        jugador_actual = jugadores[i]
        
        if not esta_vivo(jugador_actual):
            continue
            
        print(f"\nEstado actual:")
        for idx, jugador in enumerate(jugadores):
            if esta_vivo(jugador):
                print(f"{nombres[idx]}: {jugador.hp}/{jugador.max_hp} HP")
        
        vivos = [j for j in range(num_jugadores) if j != i and esta_vivo(jugadores[j])]
        if len(vivos) == 0:
            break
            
        accion = elegir_accion(jugador_actual)
        objetivo_idx = elegir_objetivo(i, jugadores, nombres)
        
        if objetivo_idx == -1:
            break
            
        objetivo = jugadores[objetivo_idx]
        
        if accion == 0:  
            danio = jugador_actual.attack(objetivo)
            print(f"{nombres[i]} atacó a {nombres[objetivo_idx]} causando {danio} de daño.")
        else: 
            habilidad_usada = jugador_actual.abilities[accion-1]['name']
            jugador_actual.use_ability(accion-1, objetivo)
        
        print(f"{nombres[objetivo_idx]} ahora tiene {objetivo.hp} HP")
        
        if not esta_vivo(objetivo):
            print(f"¡{nombres[objetivo_idx]} ha sido derrotado!")

print("\n--- FIN DEL JUEGO ---")
mostrar_ganadores(jugadores, nombres)