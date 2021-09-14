import os


class InitVariables():
    def __init__(self, dir_path):
        self.script_path = dir_path
        self.open_data()

    def open_data(self):
        with open(self.script_path + '\datas.txt') as f:
            lines = f.read().splitlines() 
        print(lines)

        if len(lines) == 4:
            self.ligue_data = lines[1].split('ligue_name : ')[1]
            self.player_token = lines[2].split('token : ')[1]
        else:
            self.ligue_data = ''
            self.player_token = ''
        print(self.ligue_data)
        print(self.player_token)
# league='1'
# # String_url = "https://api.monpetitgazon.com/championship/" + league + "/calendar/16"
# String_url="https://api.monpetitgazon.com/league/"+ ligue_data +"/mercato"
# # # print(String_url)
# i=0

# token = player_token