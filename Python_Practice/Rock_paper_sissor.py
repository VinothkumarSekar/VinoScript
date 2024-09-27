
def game (Player1,Player2):
    # Player1 = input("Player1, Enter any one input from (rock,paper,sissor) : " )
    # Player2 = input("Player2, Enter any one input from (rock,paper,sissor) : " ) 

    if Player1 == "rock" and Player2 == "sissor" :
        print(f"\n****** Player1 '{Player1}' is winner ******\n")
    elif Player1 == "sissor" and Player2 == "rock" :
        print(f"\n****** Player2 '{Player2}' is winner ******\n")
    elif Player1 == "rock" and Player2 == "rock" : 
        print ("\n****** Match Draw. play again!! ******\n" )


    if Player1 == "rock" and Player2 == "paper":
        print (f"\n****** Player2 '{Player2}' is winner ******\n") 
    elif Player1 == "paper" and Player2 == "rock" :
        print(f"\n****** Player1 '{Player1}' is winner ******\n") 
    elif Player1 == "paper" and Player2 == "paper": 
        print("\n****** Match Draw. play again!! ******\n" )


    if Player1 == "paper" and Player2 == "sissor":
        print(f"\n****** Player2 '{Player2}' is winner ******\n")
    elif Player1 == "sissor" and Player2 == "paper" :
        print(f"\n****** Player1 '{Player1}' is winner ******\n")
    elif Player1 == "sissor" and Player2 == "sissor" :
        print("\n****** Match Draw. play again!! ******\n")

if __name__ == "__main__":
    game(input("Player1, Enter any one input from (rock,paper,sissor) : " ),input("Player2, Enter any one input from (rock,paper,sissor) : " ))
