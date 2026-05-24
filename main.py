import random
import tkinter as tk
from tkinter import messagebox

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Blackjack")
        self.root.geometry("1400x900")
        self.root.configure(bg="dark green")

        self.setup_cards()
        self.money = 1000
        self.create_intro_screen()

    def setup_cards(self):
        self.card_values = {
            '2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,
            'J':10,'Q':10,'K':10,'A':11
        }

        self.suits = ['Hearts','Diamonds','Clubs','Spades']

        self.suit_symbols = {
            'Hearts':'♥',
            'Diamonds':'♦',
            'Clubs':'♣',
            'Spades':'♠'
        }

        self.deck = [
            f'{v} of {s}'
            for v in self.card_values
            for s in self.suits
        ]

        random.shuffle(self.deck)

    def create_intro_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="dark green")
        frame.pack(expand=True, fill="both")

        tk.Label(
            frame,
            text="Professional Blackjack",
            font=("Arial",36,"bold"),
            bg="dark green",
            fg="gold"
        ).pack(pady=50)

        tk.Label(
            frame,
            text=f"Money: ${self.money:.2f}",
            font=("Arial",18),
            bg="dark green",
            fg="white"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Select number of hands:",
            font=("Arial",16),
            bg="dark green",
            fg="white"
        ).pack(pady=5)

        self.hands_var = tk.IntVar(value=1)

        hands_frame = tk.Frame(frame, bg="dark green")
        hands_frame.pack(pady=5)

        for i in range(1, 4):
            tk.Radiobutton(
                hands_frame,
                text=f"{i} Hand{'s' if i>1 else ''}",
                variable=self.hands_var,
                value=i,
                font=("Arial",14),
                bg="dark green",
                fg="white",
                selectcolor="dark green"
            ).pack(anchor="w", pady=2)

        tk.Label(
            frame,
            text="Enter bet amount ($0.1-$1000):",
            font=("Arial",16),
            bg="dark green",
            fg="white"
        ).pack(pady=5)

        self.bet_entry = tk.Entry(frame, font=("Arial",14))
        self.bet_entry.insert(0, "10")
        self.bet_entry.pack(pady=5)

        tk.Button(
            frame,
            text="Start Game",
            font=("Arial",16),
            bg="green",
            fg="white",
            command=self.validate_and_start
        ).pack(pady=30)

    def validate_and_start(self):
        try:
            bet = float(self.bet_entry.get())
            total_bet = bet * self.hands_var.get()

            if 0.1 <= bet <= 1000 and total_bet <= self.money:

                # TAKE BET IMMEDIATELY
                self.money -= total_bet

                self.start_game(self.hands_var.get(), bet)

            else:
                if total_bet > self.money:
                    messagebox.showerror(
                        "Invalid Bet",
                        "Not enough money!"
                    )
                else:
                    messagebox.showerror(
                        "Invalid Bet",
                        "Bet must be $0.1-$1000"
                    )

        except:
            messagebox.showerror(
                "Invalid Bet",
                "Enter a valid number"
            )

    def start_game(self, num_hands, bet):

        self.num_hands = num_hands
        self.bet = bet
        self.current_hand = 0

        self.player_hands = [[] for _ in range(num_hands)]
        self.hand_bets = [bet for _ in range(num_hands)]

        self.dealer_hand = []

        self.insurance_taken = False
        self.insurance_bet = 0

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_game_layout()
        self.deal_initial_cards()

    def create_game_layout(self):

        # DEALER
        self.dealer_frame = tk.Frame(self.root, bg="dark green")
        self.dealer_frame.pack(pady=20)

        tk.Label(
            self.dealer_frame,
            text="Dealer's Hand",
            font=("Arial",16),
            bg="dark green",
            fg="white"
        ).pack()

        self.dealer_cards_frame = tk.Frame(
            self.dealer_frame,
            bg="dark green"
        )

        self.dealer_cards_frame.pack()

        # PLAYER HANDS
        self.hands_container = tk.Frame(
            self.root,
            bg="dark green"
        )

        self.hands_container.pack(
            expand=True,
            fill="both",
            pady=20
        )

        self.hand_frames = []
        self.hand_bet_labels = []

        for i in range(self.num_hands):

            frame = tk.Frame(
                self.hands_container,
                bg="dark green",
                highlightthickness=2,
                highlightbackground="white"
            )

            frame.pack(side="left", expand=True, padx=10)

            tk.Label(
                frame,
                text=f"Hand {i+1}",
                font=("Arial",14),
                bg="dark green",
                fg="white"
            ).pack()

            cards_frame = tk.Frame(frame, bg="dark green")
            cards_frame.pack(pady=10)

            self.hand_frames.append(frame)

            bet_label = tk.Label(
                frame,
                text=f"Bet: ${self.hand_bets[i]:.2f}",
                font=("Arial",14),
                bg="dark green",
                fg="gold"
            )

            bet_label.pack()

            self.hand_bet_labels.append(bet_label)

        # CONTROLS
        self.controls = tk.Frame(self.root, bg="dark green")
        self.controls.pack(pady=15)

        self.hit_button = tk.Button(
            self.controls,
            text="Hit",
            font=("Arial",14),
            bg="green",
            fg="white",
            command=self.hit
        )

        self.hit_button.pack(side="left", padx=5)

        self.stand_button = tk.Button(
            self.controls,
            text="Stand",
            font=("Arial",14),
            bg="green",
            fg="white",
            command=self.stand
        )

        self.stand_button.pack(side="left", padx=5)

        self.double_button = tk.Button(
            self.controls,
            text="Double",
            font=("Arial",14),
            bg="green",
            fg="white",
            command=self.double_down
        )

        self.double_button.pack(side="left", padx=5)

        self.split_button = tk.Button(
            self.controls,
            text="Split",
            font=("Arial",14),
            bg="green",
            fg="white",
            command=self.split,
            state="disabled"
        )

        self.split_button.pack(side="left", padx=5)

        self.insurance_button = tk.Button(
            self.controls,
            text="Insurance",
            font=("Arial",14),
            bg="green",
            fg="white",
            command=self.take_insurance,
            state="disabled"
        )

        self.insurance_button.pack(side="left", padx=5)

        # MONEY
        self.money_label = tk.Label(
            self.root,
            text=f"Money: ${self.money:.2f}",
            font=("Arial",14),
            bg="dark green",
            fg="white"
        )

        self.money_label.pack(pady=5)

        self.hand_indicator = tk.Label(
            self.root,
            text=f"Playing Hand 1 of {self.num_hands}",
            font=("Arial",14),
            bg="dark green",
            fg="gold"
        )

        self.hand_indicator.pack()

    def deal_card(self):

        if len(self.deck) < 20:

            self.deck = [
                f'{v} of {s}'
                for v in self.card_values
                for s in self.suits
            ]

            random.shuffle(self.deck)

        return self.deck.pop()

    def display_card(self, card, frame):

        value, suit = card.split(" of ")

        symbol = self.suit_symbols[suit]

        color = "red" if suit in ["Hearts","Diamonds"] else "black"

        tk.Label(
            frame,
            text=f"{value}\n{symbol}",
            font=("Arial",20),
            width=4,
            height=2,
            bg="white",
            fg=color,
            relief="raised",
            borderwidth=2
        ).pack(side="left", padx=2)

    def deal_initial_cards(self):

        for hand in self.player_hands:
            hand.extend([self.deal_card(), self.deal_card()])

        self.dealer_hand.extend([self.deal_card(), self.deal_card()])

        self.display_card(
            self.dealer_hand[0],
            self.dealer_cards_frame
        )

        self.hidden_label = tk.Label(
            self.dealer_cards_frame,
            text="[Hidden]",
            font=("Arial",20),
            bg="dark green",
            fg="white"
        )

        self.hidden_label.pack(side="left", padx=2)

        self.player_cards_frames = []

        for i, hand in enumerate(self.player_hands):

            cf = tk.Frame(self.hand_frames[i], bg="dark green")
            cf.pack(pady=5)

            self.player_cards_frames.append(cf)

            for c in hand:
                self.display_card(c, cf)

        self.update_hand_indicator()
        self.update_split_button()
        self.check_insurance_available()

    def hand_value(self, hand):

        value = 0
        aces = 0

        for c in hand:

            val = c.split()[0]

            if val == 'A':
                aces += 1

            value += self.card_values[val]

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def hit(self):

        hand = self.player_hands[self.current_hand]

        hand.append(self.deal_card())

        self.display_card(
            hand[-1],
            self.player_cards_frames[self.current_hand]
        )

        if self.hand_value(hand) >= 21:
            self.stand()

        self.update_split_button()

    def stand(self):

        self.current_hand += 1

        if self.current_hand >= len(self.player_hands):
            self.dealer_play()

        else:
            self.update_hand_indicator()
            self.update_split_button()
            self.check_insurance_available()

    def double_down(self):

        hand = self.player_hands[self.current_hand]

        if self.money < self.hand_bets[self.current_hand]:

            messagebox.showinfo(
                "Cannot Double",
                "Not enough money!"
            )

            return

        self.money -= self.hand_bets[self.current_hand]

        self.hand_bets[self.current_hand] *= 2

        self.hand_bet_labels[self.current_hand].config(
            text=f"Bet: ${self.hand_bets[self.current_hand]:.2f}"
        )

        self.money_label.config(
            text=f"Money: ${self.money:.2f}"
        )

        hand.append(self.deal_card())

        self.display_card(
            hand[-1],
            self.player_cards_frames[self.current_hand]
        )

        self.stand()

    def split(self):

        hand = self.player_hands[self.current_hand]

        if (
            len(hand) != 2
            or self.money < self.hand_bets[self.current_hand]
        ):

            messagebox.showinfo(
                "Cannot Split",
                "Cannot split this hand"
            )

            return

        self.money -= self.hand_bets[self.current_hand]

        self.money_label.config(
            text=f"Money: ${self.money:.2f}"
        )

        new_card = hand.pop()

        new_hand = [new_card, self.deal_card()]

        hand.append(self.deal_card())

        self.player_hands.append(new_hand)

        self.hand_bets.append(
            self.hand_bets[self.current_hand]
        )

        frame = tk.Frame(
            self.hands_container,
            bg="dark green",
            highlightthickness=2,
            highlightbackground="white"
        )

        frame.pack(side="left", expand=True, padx=10)

        tk.Label(
            frame,
            text=f"Hand {len(self.hand_frames)+1}",
            font=("Arial",14),
            bg="dark green",
            fg="white"
        ).pack()

        cards_frame = tk.Frame(frame, bg="dark green")
        cards_frame.pack(pady=5)

        self.hand_frames.append(frame)
        self.player_cards_frames.append(cards_frame)

        bet_label = tk.Label(
            frame,
            text=f"Bet: ${self.hand_bets[-1]:.2f}",
            font=("Arial",14),
            bg="dark green",
            fg="gold"
        )

        bet_label.pack()

        self.hand_bet_labels.append(bet_label)

        for c in hand:
            self.display_card(
                c,
                self.player_cards_frames[self.current_hand]
            )

        for c in new_hand:
            self.display_card(c, cards_frame)

    def check_insurance_available(self):

        insurance_cost = self.hand_bets[self.current_hand] / 2

        if (
            self.dealer_hand[0].split()[0] == 'A'
            and not self.insurance_taken
            and self.money >= insurance_cost
        ):

            self.insurance_button.config(state="normal")

        else:
            self.insurance_button.config(state="disabled")

    def take_insurance(self):

        bet = self.hand_bets[self.current_hand] / 2

        if self.money < bet:

            messagebox.showinfo(
                "Cannot take insurance",
                "Not enough money"
            )

            return

        self.money -= bet

        self.insurance_bet = bet

        self.money_label.config(
            text=f"Money: ${self.money:.2f}"
        )

        self.insurance_taken = True

        self.insurance_button.config(state="disabled")

        dealer_val = self.hand_value(self.dealer_hand)

        if dealer_val == 21:

            self.money += bet * 3

            messagebox.showinfo(
                "Insurance Win",
                "Dealer has Blackjack!"
            )

            self.dealer_play()

        else:

            messagebox.showinfo(
                "Insurance Lost",
                "Dealer does not have Blackjack"
            )

    def update_split_button(self):

        hand = self.player_hands[self.current_hand]

        if (
            len(hand) == 2
            and self.card_values[hand[0].split()[0]]
            == self.card_values[hand[1].split()[0]]
            and self.money >= self.hand_bets[self.current_hand]
        ):

            self.split_button.config(state="normal")

        else:
            self.split_button.config(state="disabled")

    def update_hand_indicator(self):

        self.hand_indicator.config(
            text=f"Playing Hand {self.current_hand+1} of {self.num_hands}"
        )

        for i, frame in enumerate(self.hand_frames):

            frame.config(
                highlightbackground="gold"
                if i == self.current_hand
                else "white"
            )

        # DISABLE DOUBLE IF BROKE
        if self.money < self.hand_bets[self.current_hand]:
            self.double_button.config(state="disabled")
        else:
            self.double_button.config(state="normal")

    def dealer_play(self):

        self.hidden_label.destroy()

        for card in self.dealer_hand:
            self.display_card(card, self.dealer_cards_frame)

        while True:

            val = self.hand_value(self.dealer_hand)

            soft17 = (
                val == 17
                and any(c.split()[0] == 'A'
                for c in self.dealer_hand)
            )

            if val < 17 or soft17:

                self.dealer_hand.append(self.deal_card())

                self.display_card(
                    self.dealer_hand[-1],
                    self.dealer_cards_frame
                )

            else:
                break

        self.settle_bets()

    def settle_bets(self):

        dealer_val = self.hand_value(self.dealer_hand)

        results = []

        for i, hand in enumerate(self.player_hands):

            val = self.hand_value(hand)
            bet = self.hand_bets[i]

            # LOSE
            if val > 21:

                results.append(
                    f"Hand {i+1}: Bust - Lost ${bet:.2f}"
                )

            # WIN
            elif dealer_val > 21 or val > dealer_val:

                self.money += bet * 2

                results.append(
                    f"Hand {i+1}: Won ${bet:.2f}"
                )

            # PUSH
            elif val == dealer_val:

                self.money += bet

                results.append(
                    f"Hand {i+1}: Push"
                )

            # LOSE
            else:

                results.append(
                    f"Hand {i+1}: Lost ${bet:.2f}"
                )

        self.money_label.config(
            text=f"Money: ${self.money:.2f}"
        )

        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.split_button.config(state="disabled")
        self.double_button.config(state="disabled")
        self.insurance_button.config(state="disabled")

        res_frame = tk.Frame(self.root, bg="dark green")
        res_frame.pack(pady=20)

        tk.Label(
            res_frame,
            text="\n".join(results),
            font=("Arial",14),
            bg="dark green",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            res_frame,
            text="Play Again",
            font=("Arial",14),
            bg="green",
            fg="white",
            command=self.create_intro_screen
        ).pack(pady=10)

        tk.Button(
            res_frame,
            text="Quit",
            font=("Arial",14),
            bg="red",
            fg="white",
            command=self.root.quit
        ).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
