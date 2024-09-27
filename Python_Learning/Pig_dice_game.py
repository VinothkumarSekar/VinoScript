import random
player_score = 0
computer_score = 0
Welcome_message = "\nWelcome to the DICE GAME!!\n>> In this game, a user and a computer opponent roll a 6-sided dice each round.\n>> If the value of the dice is a 1, the player that rolled the 1 loses all of their points.\n>> Otherwise, the player gets the value of the dice added to their points.\n>> The first player to reach 30 points wins!"

print(Welcome_message)   

UserName = input("\nEnter your name: ")

def scores (score,dice_value):
        if dice_value == 1:
            return 0
        else:
            return score + dice_value

def score_board (UserName,player_score,computer_score):
    print()
    print("*" * 20)
    print(f"{UserName} Score: {player_score}")
    print(f"Computer Score: {computer_score}")
    print("*" * 20)
    print()

while True:
            usr_inp = input(f'\nHey {UserName}, press "Enter" to roll the dice..')
            usr_dice = random.randint(1,6)
            print(f"\n{UserName}! rolls a : {usr_dice}")

            computer_dice = random.randint(1,6)
            print(f"Computer! rolls a : {computer_dice}\n")

            player_score = scores(player_score,usr_dice)
            computer_score = scores(computer_score,computer_dice)
            score_board (UserName,player_score,computer_score)

            if player_score >= 30:
                print(f"{UserName} : WINS! \U0001f600 \U0001f600 \n")
                break
            elif computer_score >= 30:
                print("Computer : WINS! \U0001F923 \U0001F923 \n")  
                break  



