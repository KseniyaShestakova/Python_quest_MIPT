# Quest
A small console quest. It makes you able to create a console quest with your own scenario writing file with the format similar to the ones presented in parameters.txt / parameters_again.txt (file with parameter description) and positions.txt / nodes_again.txt (file with the description of positions) 

### Execution
To run the quest:
```

cd Python_quest_MIPT
git checkout quest
python3 main.py parameters.txt positions.txt
```
(for playing a quest about MIPT life)
or 
```

cd Python_quest_MIPT
git checkout quest
python3 main.py parameters_again.txt nodes_again.txt
```
(for playing a quest with rules explanation)

### Installing necessary libraries:
Make sure you have installed python libraries, which are necessary for running this quest!
They are 'keyboard','termcolor' and 'random'
```
apt install python3 python3-pip
apt install python3-termcolor
pip3 install keyboard
pip3 install random
```
### Something about playing the quest
You can choose the right option in this quest pressing Ctrl and confirm your choice pressing Enter
