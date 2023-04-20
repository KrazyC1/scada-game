import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

class Threat:
    def __init__(self, name, health, attack_strength, reward):
        self.name = name
        self.health = health
        self.attack_strength = attack_strength
        self.reward = reward  # Add this line

    def damage(self):
        return random.randint(1, self.attack_strength)
    
    def take_damage(self, damage):
        self.health -= damage

def spawn_threat(level):
    threat_list = [
        Threat("DoS Attack", 15 * level, 3 * level, 5 * level),
        Threat("SQL Injection", 10 * level, 5 * level, 7 * level),
        Threat("Man in the Middle", 20 * level, 2 * level, 6 * level),
        Threat("Social Engineering", 12 * level, 4 * level, 4 * level),
    ]
    return random.choice(threat_list)


class SCADADefenseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SCADA Defense")
        self.root.geometry("300x400")

        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        self.money = 100
        self.scada_health = 50
        self.level = 1
        self.ids_level = 0
        self.ips_level = 0
        self.threat = spawn_threat(self.level)

        self.threat_image = None
        self.threat_canvas = tk.Canvas(self.main_frame, width=300, height=200)
        self.threat_canvas.grid(row=0, column=0, columnspan=4)

        self.attack_button = ttk.Button(self.main_frame, text="Attack", command=self.attack)
        self.attack_button.grid(row=1, column=0)

        self.upgrade_ids_button = ttk.Button(self.main_frame, text=f"Upgrade IDS (${20 * (self.ids_level + 1)})", command=lambda: self.upgrade(1))
        self.upgrade_ids_button.grid(row=1, column=1)

        self.upgrade_ips_button = ttk.Button(self.main_frame, text=f"Upgrade IPS (${10 * (self.ips_level + 1)})", command=lambda: self.upgrade(2))
        self.upgrade_ips_button.grid(row=1, column=2)

        self.heal_button = ttk.Button(self.main_frame, text="Heal ($10)", command=self.heal)
        self.heal_button.grid(row=1, column=3)

        self.info_label = ttk.Label(self.main_frame, text=f"SCADA Health: {self.scada_health} Money: ${self.money} Level: {self.level}", font=("Arial", 14))
        self.info_label.grid(row=2, column=0, columnspan=4, pady=10)

        self.ids_ips_level_label = ttk.Label(self.main_frame, text=f"IDS Level: {self.ids_level}  IPS Level: {self.ips_level}", font=("Arial", 14))
        self.ids_ips_level_label.grid(row=3, column=0, columnspan=4)

        self.threat_info_label = ttk.Label(self.main_frame, text=f"Threat: {self.threat.name}\nHealth: {self.threat.health}", font=("Arial", 14))
        self.threat_info_label.grid(row=4, column=0, columnspan=4)

        self.damage_info_label = ttk.Label(self.main_frame, text="", font=("Arial", 12))
        self.damage_info_label.grid(row=5, column=0, columnspan=4)

        self.update_gui()

    def attack(self):
        self.damage_info_label["text"] = ""
        damage_dealt = self.attack_threat()
        self.damage_info_label["text"] += f"You attacked for {damage_dealt} damage.\n"
        self.threat_action()
        self.passive_ips_attack()
        self.update_gui()

    def upgrade(self, upgrade_type):
        self.damage_info_label["text"] = ""
        if upgrade_type == 1:  # Upgrade IDS
            if self.money >= 20 * (self.ids_level + 1):
                self.money -= 20 * (self.ids_level + 1)
                self.ids_level += 1
                self.ids_ips_level_label["text"] = f"IDS Level: {self.ids_level}  IPS Level: {self.ips_level}"
                self.upgrade_ids_button["text"] = f"Upgrade IDS (${20 * (self.ids_level + 1)})" 
            else:
                self.damage_info_label["text"] = "Not enough money for upgrade."
        elif upgrade_type == 2:  # Upgrade IPS
            if self.money >= 10 * (self.ips_level + 1):
                self.money -= 10 * (self.ips_level + 1)
                self.ips_level += 1
                self.ids_ips_level_label["text"] = f"IDS Level: {self.ids_level}  IPS Level: {self.ips_level}"
                self.upgrade_ips_button["text"] = f"Upgrade IPS (${10 * (self.ips_level + 1)})"
            else:
                self.damage_info_label["text"] = "Not enough money for upgrade."
        self.threat_action()
        self.passive_ips_attack()
        self.update_gui()

    def heal(self):
        if self.money >= 10:
            self.money -= 10
            self.scada_health += 5
            if self.scada_health > 50:
                self.scada_health = 50
            self.damage_info_label["text"] = f"\nPlayer healed for 5 health."
        else:
            self.damage_info_label["text"] = f"\nNot enough money for healing."
        self.threat_action()
        self.passive_ips_attack()
        self.update_gui()

    def passive_ips_attack(self):
        if self.ips_level > 0:
            damage_dealt = self.ips_level * 2
            self.threat.health -= damage_dealt
            self.damage_info_label["text"] += f"\nIPS attacked for {damage_dealt} passive damage."
            if self.threat.health <= 0:
                self.level_up()
                self.update_gui()

    def threat_action(self):
        dodge_chance = self.ids_level * 10
        if random.randint(1, 100) > dodge_chance:
            damage_taken = self.threat.damage()
            self.scada_health -= damage_taken
            self.damage_info_label["text"] += f"\nYou took {damage_taken} damage from threat."
        else:
            self.damage_info_label["text"] += f"\nThreat attack dodged."

        if self.scada_health <= 0:
            self.game_over()

    def level_up(self):
        self.money += self.threat.health * 5
        self.level += 1
        self.threat = spawn_threat(self.level)
        self.update_gui()

    def game_over(self):
        self.attack_button["state"] = "disabled"
        self.upgrade_ids_button["state"] = "disabled"
        self.upgrade_ips_button["state"] = "disabled"
        self.heal_button["state"] = "disabled"
        self.threat_info_label["text"] = "Game Over"

        self.restart_button = ttk.Button(self.main_frame, text="Restart", command=self.restart)
        self.restart_button.grid(row=6, column=0, columnspan=4)

    def restart(self):
        self.attack_button["state"] = "normal"
        self.upgrade_ids_button["state"] = "normal"
        self.upgrade_ips_button["state"] = "normal"
        self.heal_button["state"] = "normal"

        self.money = 100
        self.scada_health = 50
        self.level = 1
        self.ids_level = 0
        self.ips_level = 0
        self.threat = spawn_threat(self.level)

        self.restart_button.grid_forget()
        self.damage_info_label["text"] = ""

        self.update_gui()

    def update_gui(self):
        self.info_label["text"] = f"SCADA Health: {self.scada_health} Money: ${self.money} Level: {self.level}"
        self.threat_info_label["text"] = f"Threat: {self.threat.name}\nHealth: {self.threat.health}"

        # Enable or disable buttons based on the money available
        if self.money >= 20 * (self.ids_level + 1):
            self.upgrade_ids_button["state"] = "normal"
        else:
            self.upgrade_ids_button["state"] = "disabled"

        if self.money >= 10 * (self.ips_level + 1):
            self.upgrade_ips_button["state"] = "normal"
        else:
            self.upgrade_ips_button["state"] = "disabled"

        if self.money >= 10:
            self.heal_button["state"] = "normal"
        else:
            self.heal_button["state"] = "disabled"

        self.update_threat_image()

    def update_threat_image(self):
        image_path = f"images/{self.threat.name.replace(' ', '_')}.png"
        self.threat_image = Image.open(image_path).resize((200, 200), Image.ANTIALIAS)
        self.threat_image = ImageTk.PhotoImage(self.threat_image)
        self.threat_canvas.delete("all")
        self.threat_canvas.create_image(150, 100, image=self.threat_image)

    def attack_threat(self):
        damage = 5 + random.randint(0, 5)
        self.threat.take_damage(damage)
        if self.threat.health <= 0:
            self.level += 1
            self.money += self.threat.reward
            self.threat = spawn_threat(self.level)
        return damage

if __name__ == "__main__":
    root = tk.Tk()
    app = SCADADefenseGUI(root)
    root.mainloop()
