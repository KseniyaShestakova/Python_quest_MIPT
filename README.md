# Quest
A small console quest. It makes you able to create a console quest with your own scenario writing file with the format similar to the ones presented in parameters_study.txt/ rules_parameters.txt (file with parameter description) and study_quest.txt / rules_quest.txt (file with the description of positions) 

### Execution
To run the quest:
```
git clone git@github.com:KseniyaShestakova/Python_quest_MIPT.git
cd Python_quest_MIPT/
git checkout quest
python3 main.py parameters_study.txt study_quest.txt
```
(for playing a quest about MIPT life)
or 
```
cd Python_quest_MIPT/
git checkout quest
python3 main.py rules_parameters.txt rules_quest.txt
```
(for playing a quest with rules explanation)
or
```
cd Python_quest_MIPT/
git checkout quest
python3 main.py <my_parameters> <my_position>
```
(if you have your own file with parameters and positions)

### Installing necessary libraries:
Make sure you have installed python libraries, which are necessary for running this quest!
They are 'keyboard','termcolor','random' and 'sys'
```
apt install python3 python3-pip
apt install python3-termcolor
pip3 install keyboard
pip3 install random
pip install os-sys
```
Note: if you write 'sudo' before installing one of this libraries you should execute the project with 'sudo' also:
```
sudo python3 main.py <parameters> <position>
```
### Something about playing the quest
You can choose the right option in this quest pressing Ctrl and confirm your choice pressing Enter![
###Example
Screenshot from 2022-04-15 11-43-45](https://user-images.githubusercontent.com/91065721/163548416-7ab0d810-2cf1-4020-953a-90259cfa807c.png)

