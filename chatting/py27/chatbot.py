from random import randint
# from srl import srl
# from Ner import Ner

# Class bot : the main class of the question generator
class bot:
    def __init__(self, name):
        self.name = name
        self.base = {}
        self.read_file('/home/ahmed/django/bot/chatting/py27/r.txt')
        self.user_name = "User"
        self.input = ""
        self.raw_input = ""
        self.last_input = ""
        self.last_response = ""
        self.emotions = ['joy', 'fear', 'anger', 'sadness', 'disgust', 'neutral']
        self.input_tokens = []
        
        self.end_conv = 0
        self.empty_input = 0

        # self.srl = srl()
        # self.Ner = Ner()

    def set_bot_name(self, name):
        self.name = name

    def read_file(self,path):
        f = open(path, 'r')
        self.base = {}
        keys = []
        resp = []
        i = 0
        for l in f:
            init_char = l[0]
            line = l[1:]
            line = line.replace("\n", "") #remove slash n from line end

            if(init_char == 'K'):
                keys.append(line)
            elif(init_char == 'R'):
                # print 'Res'
                resp.append(line)
            elif(init_char == '#'):
                if resp and keys:
                    obj = {}
                    obj['keys'] = keys
                    obj['responses'] = resp
                    self.base[i] = obj
                    # for k in keys:
                    #     self.base[k] = resp

                # clearing keys and resp lists
                keys = []
                resp = []
                i+=1
    def get_base(self):
        return self.base
    def print_response(self):
        inp = self.input

        response_list = self.get_response()
        
        resp_size = len(response_list)
        rand = randint(0, resp_size-1)
        rand_em = randint(0, 5)
        while(response_list[rand] == self.last_response):
            rand = randint(0, resp_size-1)
        response = response_list[rand] #select random response
        self.last_response = response # saving last response
        response = self.response_process(response)
        return response
        # return (response,'| emotion: ', self.emotions[rand_em])
    def get_response(self):
        input = self.input
        found_resp = False
        if(self.input == self.last_input and self.input != "BOT DON'T UNDERSTAND**" and self.input !="NULL INPUT**"):
            input = "REPETITION T1**"
        for record_key in self.base:
            record = self.base[record_key]
            for key in record['keys']:
                if(input == key):
                    found_resp = True
                    response_list = record['responses']
                    if(record_key == 32):
                        self.end_conv = 1
                    break
        if not found_resp:
            self.tokenize(self.input)
            response_list = self.find_best_key()
            if(not response_list):
                self.input = "BOT DON'T UNDERSTAND**"
                return self.get_response()
        self.last_input = self.input
        return response_list

    def set_input(self, inp):
        self.input = inp
        self.raw_input = self.input
        # self.srl.record(self.input)
        # self.Ner.record(self.input)
        # self.input_tokens = self.tokenize(self.input)
        # self.find_best_key()
        # print(self.get_sub_phrase(self.input_tokens, 0, 2))
    def response_process(self, response):
        response = response.lower()
        return response.replace("@", self.name) #replace '@' with bot name

    def check_empty_input(self):
        if(self.input == ""):
            self.empty_input = 1
        else:
            self.empty_input = 0
    def validate_input(self):
        self.check_empty_input()
        if(self.empty_input == 1):
            self.input = "NULL INPUT**"
    def preprocess_input(self):
        self.remove_punc()
        self.input = self.input.upper()
    def remove_punc(self):
        input_m = self.input
        delim = "?!;,"
        for d in delim:
            input_m = input_m.replace(d, "")
        self.input = input_m.strip()
    def find_best_key(self):
        found_resp = False
        n = len(self.input_tokens)
        for i in range(0, n):
            j = n-i-1
            for k in range(0, n-j):
                size = k+j+1
                phrase = self.get_sub_phrase(self.input_tokens, k, size)
                for record_key in self.base:
                    record = self.base[record_key]
                    for key in record['keys']:
                        if(phrase == key):
                            found_resp = True
                            response_list = record['responses']
                            if(record_key == 32):
                                self.end_conv = 1
                            break
                    if found_resp:
                        break
                if found_resp:
                    break
            if found_resp:
                break
        if found_resp:
            return response_list
        else:
            return False
    def tokenize(self, input_m):
        self.input_tokens = []
        buffer = ""
        for i in input_m:
            if(not self.is_punc(i) and not self.is_space(i)):
                buffer = buffer + i
            else:
                self.input_tokens.append(buffer)
                buffer = ""
        if( len(buffer) > 0) :
            self.input_tokens.append(buffer) 
        return self.input_tokens
    def get_sub_phrase(self, arr, start, end):
        buffer = "";
        for i in range(start,end) :
            buffer += arr[i];
            buffer = buffer + " "
        buffer = buffer.strip()
        return buffer;
    def is_punc(self, char):
        delim = "?!;,"
        for d in delim:
            if(char == d):
                return True
        return False
    def is_space(self, char):
        return char==" "
    # def start(self):
        # print("Hi, I am "+self.name+" !")
        # while( 1 ):
            # self.set_input()
            # self.validate_input()
            # self.preprocess_input()
            # self.print_response()
            # if( self.end_conv == 1 ):
            #     break;
# End of Class bot