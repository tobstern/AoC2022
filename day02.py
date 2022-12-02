from time import perf_counter as pfc


class RockPaperScissors:
    def __init__(self):
        self.mapping = {}
        self.score1 = 0
        self.score2 = 0
        # aim is the state of outcome (for part 2):
        # X := loose, Y := draw, Z := win
        # player 0 encrypted roles
        self.mapping["A"] = "rock"
        self.mapping["B"] = "paper"
        self.mapping["C"] = "scissors"
        # player 1 encrypted roles
        self.mapping["X"] = "rock"
        self.mapping["Y"] = "paper"
        self.mapping["Z"] = "scissors"

    def rules(self, char0, char1):
        draw = False
        if self.mapping[char1] == "rock":
            self.score1 += 1
        elif self.mapping[char1] == "paper":
            self.score1 += 2
        elif self.mapping[char1] == "scissors":
            self.score1 += 3
        # checking the player's hands
        if self.mapping[char0] == self.mapping[char1]:
            print("draw!")
            draw = True
            self.score1 += 3
        if (
            (
                self.mapping[char0] == "rock"
                and "scissors" == self.mapping[char1]
            )
            or (
                self.mapping[char0] == "paper"
                and "rock" == self.mapping[char1]
            )
            or (
                self.mapping[char0] == "scissors"
                and "paper" == self.mapping[char1]
            )
        ):
            print("Player Two loses!")
        elif not draw:
            print("Player Two wins!")
            self.score1 += 6

    def rules2(self, char0, char1):
        if char1 == "X":
            # aim is to loose
            if self.mapping[char0] == "rock":
                # choose scissors:
                self.score2 += 3
            elif self.mapping[char0] == "scissors":
                # choose paper:
                self.score2 += 2
            elif self.mapping[char0] == "paper":
                # choose rock:
                self.score2 += 1
        elif char1 == "Y":
            # aim is to draw
            self.score2 += 3
            if self.mapping[char0] == "rock":
                # choose rock:
                self.score2 += 1
            elif self.mapping[char0] == "scissors":
                # choose scissors:
                self.score2 += 3
            elif self.mapping[char0] == "paper":
                # choose paper:
                self.score2 += 2
        elif char1 == "Z":
            # aim is to win
            self.score2 += 6
            if self.mapping[char0] == "rock":
                # choose paper:
                self.score2 += 2
            elif self.mapping[char0] == "scissors":
                # choose rock:
                self.score2 += 1
            elif self.mapping[char0] == "paper":
                # choose scissors:
                self.score2 += 3

    def play(self, guide):
        for char0, char1 in guide:
            RockPaperScissors.rules(self, char0, char1)
            RockPaperScissors.rules2(self, char0, char1)


day = "02"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
i = [
    l.split(" ")
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]
print(i)

# Part 1:
start1 = pfc()
game = RockPaperScissors()
game.play(i)
print(f"Part 1 result is: {game.score1}, t = {pfc() - start1}")

# Part 2:
print(f"Part 2 result is: {game.score2}, t = {pfc() - start1}")
