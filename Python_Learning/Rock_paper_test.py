import Rock_paper_sissor
Player1 = input("Player1, Enter any one input from (rock,paper,sissor) : " )
Player2 = input("Player2, Enter any one input from (rock,paper,sissor) : " )

Rock_paper_sissor.game(Player1,Player2) 

while True: 
    usr_command = input("**Type 'enter' to play again... (or) Type 'quit' to exit the game..**\n\nWaiting for input: ")
    if usr_command == "enter":
        print("playing again..") 
        Player1 = input("Player1, Enter any one input from (rock,paper,sissor) : " )
        Player2 = input("Player2, Enter any one input from (rock,paper,sissor) : " )
        Rock_paper_sissor.game(Player1,Player2)   
    elif usr_command == "quit": 
        print("\n\n******** Played Well!! Good Bye!! ********\n\n")
        break