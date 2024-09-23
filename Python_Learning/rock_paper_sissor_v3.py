
import argparse

def game (Player1,Player2):

    try:

        if Player1 == "rock" or Player1 == "sissor" or Player1 == "paper": 
            if Player2 == "rock" or Player2 == "sissor" or Player2 == "paper":
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
            else:
                print("\n***** Please pass valid input..*****\n")
        else:
            print("\n***** Please pass valid input..*****\n") 
            
    except Exception as error:
        print(f"Got exception: {error}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Passing values to Player1 and Player2')
    parser.add_argument('--player1', metavar='path', required=True,
                        help='Player1 input to game. \neg. --player1 rock')
    parser.add_argument('--player2', metavar='path', required=True,
                        help='Player2 input to game. \neg. --player2 rock')
    args = parser.parse_args()
    Player1=args.player1 
    Player2=args.player2
    game(Player1,Player2)
    while True: 
        usr_command = input("\n**Type 'enter' to play again... (or) Type 'quit' to exit the game..**\n\nWaiting for input: ")
        if usr_command == "enter":
            print("playing again..") 
            Player1 = input("\nPlayer1, Enter any one input from (rock,paper,sissor) : " )
            Player2 = input("Player2, Enter any one input from (rock,paper,sissor) : " )
            game(Player1,Player2)
           
        elif usr_command == "quit": 
            print("\n\n******** Played Well!! Good Bye!! ********\n\n")
            break
    


 
    

