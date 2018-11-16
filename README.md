# Shell
Allows you to generate a shell and start programs just as a shell does. 
The program has different commands such as "quitter", "tuer" and "liste"
Otherwise, You can run any other Liniux commands you want.

The command "tuer" takes one parameter, which is the PID of a process you might want to kill

    Usage: tuer <PID> 
      The PID has to be an integer and also has to exist in the List of Processes running in the program.


The only way to quit the program is by entering the command "quitter" or buy closing the terminal
    
        Usage: quitter
        After that, you have to choose between yes (o or O) to exit 
        Or anything else to keep running the program
        
lister command usage;
     
            Usage: lister

The program uses signal to capture the SIGCHLD signal and redirect erroers into a file named "erreurs.txt" 
