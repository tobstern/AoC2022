from time import perf_counter as pfc


class RockPaperScissors:
    def __init__(self):
        self.mapping = {}
        self.points = 0
        self.won = False
        self.result = 0
        # player 0 encrypted roles
        self.mapping["A"] = "rock"
        self.mapping["B"] = "paper"
        self.mapping["C"] = "scissors"
        # player 1 encrypted roles
        self.mapping["X"] = "rock"
        self.mapping["Y"] = "paper"
        self.mapping["Z"] = "scissors"

    def rules(self, char0, char1):
        if self.mapping[char1] == "rock":
            self.points += 1
        if self.mapping[char1] == "paper":
            self.points += 2
        if self.mapping[char1] == "scissors":
            self.points += 3
        # checking the player's hands
        if self.mapping[char0] == self.mapping[char1]:
            print("draw!")
            self.points += 3
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
        else:
            print("Player Two wins!")
            self.points += 6

    def play(self, guide):
        for char0, char1 in guide:
            RockPaperScissors.rules(self, char0, char1)


day = "02"
test = 1
if test:
    t = "test_"
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
print(f"Part 1 result is: {game.points}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")

# part1: 22880 too high,
