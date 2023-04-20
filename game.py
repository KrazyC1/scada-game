import random

class Threat:
    def __init__(self, level, name, damage_multiplier):
        self.level = level
        self.name = name
        self.damage_multiplier = damage_multiplier
        self.health = random.randint(level * 5, level * 10)

    def damage(self):
        return random.randint(self.level * self.damage_multiplier, self.level * 2 * self.damage_multiplier)

threat_types = [
    {"name": "DoS Attack", "damage_multiplier": 1},
    {"name": "SQL Injection", "damage_multiplier": 2},
    {"name": "Man in the Middle", "damage_multiplier": 3},
    {"name": "Social Engineering", "damage_multiplier": 4}
]

def spawn_threat(level):
    threat_type = random.choice(threat_types)
    return Threat(level, threat_type["name"], threat_type["damage_multiplier"])

def main():
    print("Welcome to SCADA Defense!")
    print("Defend your SCADA system from a variety of threats using IDS and IPS.")
    print("You start with $100 and 50 health. Use 'attack' to kill threats, 'upgrade' to improve your defenses, and 'heal' to restore health.")
    print("Good luck!")

    money = 100
    scada_health = 50
    level = 1
    ids_level = 0
    ips_level = 0

    while scada_health > 0:
        print("\n" + "=" * 50)
        print(f"Round {level}: SCADA Health: {scada_health}, Money: ${money}")
        threat = spawn_threat(level)
        print(f"A threat of level {threat.level} ({threat.name}) with {threat.health} health has appeared!")

        while threat.health > 0 and scada_health > 0:
            action = input("Type 'attack', 'upgrade', or 'heal': ")

            if action == "attack":
                damage = random.randint(level, level * 2)
                threat.health -= damage
                print(f"You dealt {damage} damage to the threat. It has {threat.health} health remaining.")
            elif action == "upgrade":
                print("Upgrade options:")
                print(f"1. IDS (Level {ids_level}): Cost ${10 * (ids_level + 1)} - Increases chance to dodge an attack")
                print(f"2. IPS (Level {ips_level}): Cost ${10 * (ips_level + 1)} - Automatically deals damage to threats")
                upgrade_choice = input("Enter the number of the upgrade you want to buy: ")

                if upgrade_choice == "1":
                    cost = 10 * (ids_level + 1)
                    if money >= cost:
                        money -= cost
                        ids_level += 1
                        print(f"Upgraded IDS to Level {ids_level}. Money left: ${money}")
                    else:
                        print("You don't have enough money!")
                elif upgrade_choice == "2":
                    cost = 10 * (ips_level + 1)
                    if money >= cost:
                        money -= cost
                        ips_level += 1
                        print(f"Upgraded IPS to Level {ips_level}. Money left: ${money}")
                    else:
                        print("You don't have enough money!")
                else:
                    print("Invalid choice.")
            elif action == "heal":
                heal_cost = 5 + level
                if money >= heal_cost:
                    money -= heal_cost
                    scada_health += 5 + level
                    print(f"You restored {5 + level} health. SCADA Health: {scada_health}, Money left: ${money}")
                else:
                    print("You don't have enough money!")
            else:
                print("Invalid action.")
                continue

            if ips_level > 0:
                ips_damage = ips_level * random.randint(1, 3)
                threat.health -= ips_damage
                print(f"Your IPS dealt {ips_damage} damage to the threat. It has {threat.health} health remaining.")

            if threat.health <= 0:
                reward = random.randint(level * 5, level * 10)
                money += reward
                print(f"You defeated the threat and earned ${reward}! Money: ${money}")
                level += 1
            else:
                if random.randint(1, 100) > ids_level * 10:
                    threat_damage = threat.damage()
                    scada_health -= threat_damage
                    print(f"The threat attacked your SCADA system for {threat_damage} damage. Health: {scada_health}")
                else:
                    print("Your IDS helped you dodge the attack!")

    print("Game Over! Your SCADA system has been breached.")

if __name__ == "__main__":
    main()

