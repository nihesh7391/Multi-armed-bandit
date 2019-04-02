from flask import Flask, render_template, request
import numpy as np
import qrcode
import random
import socket

def qr_generator(link):
    qr1 = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4)

    qr1.add_data(link)
    qr1.make(fit=True)

    img = qr1.make_image()
    return img

pmfs = np.zeros((5,11))
pmfs[0,:] = [1.66468707e-05, 9.25991435e-05, 1.31090184e-03, 1.29093570e-02,
 6.95071081e-02, 2.00879096e-01, 3.11159002e-01, 2.58287871e-01,
 1.14900360e-01, 2.74089524e-02, 3.52810507e-03] # mean 6, var 40
pmfs[1,:] = [0.00305375, 0.01064562, 0.02968141, 0.06618364, 0.11802284, 0.16831748,
 0.19197291, 0.17510493, 0.1277334,  0.0745175,  0.03476652] # mean 5, var 100
pmfs[2,:] = [1.32094258e-05, 4.63992761e-04, 8.56202160e-03, 6.87744915e-02,
 2.40085160e-01, 3.64203959e-01, 2.40083560e-01, 6.87735717e-02,
 8.56185571e-03, 4.64940309e-04, 1.32386784e-05] # mean 0, var 30
pmfs[3,:] = [2.41857372e-05, 8.88000204e-04, 1.38874849e-02, 9.44110740e-02,
 2.78940248e-01, 3.58164614e-01, 1.99865295e-01, 4.84703692e-02,
 5.10876059e-03, 2.34373605e-04, 5.59400534e-06] # mean -1, var 30
pmfs[4,:] = [7.68850484e-05, 1.65980405e-03, 2.17079411e-02, 1.25197518e-01,
 3.13615930e-01, 3.40903841e-01, 1.60799574e-01, 3.29299044e-02,
 2.95248674e-03, 1.38992240e-04, 1.71235704e-05] # mean -2, var 30

sample_range = [-25, -20, -15, -10, -5, 0, 5 ,10, 15, 20, 25]
permut = np.random.permutation(5)
pmf1 = pmfs[permut[0]]
pmf2 = pmfs[permut[1]]
pmf3 = pmfs[permut[2]]
pmf4 = pmfs[permut[3]]
pmf5 = pmfs[permut[4]]

def generate_random(option):
    option = int(option)
    if option == 1:
        rand = np.random.choice(sample_range, p=pmf1)
    elif option == 2:
        rand = np.random.choice(sample_range, p=pmf2)
    elif option == 3:
        rand = np.random.choice(sample_range, p=pmf3)
    elif option == 4:
        rand = np.random.choice(sample_range, p=pmf4)
    elif option == 5:
        rand = np.random.choice(sample_range, p=pmf5)
    print (rand)
    return (rand)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)) # doesn't even have to be reachable
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

start_game = 0
session_flag  = np.ones(5) # True means session is on...
Round = 0
table_size = 14

total_score = 100*np.ones(5)
number_rounds = 20

# random number store...
random_numbers = np.zeros(shape=(number_rounds, 5))

# option store...
options_store = np.zeros(shape=(number_rounds, 5))

# Generate random links ...
team = ['Air', 'Earth', 'Fire', 'Metal', 'Water']
IP = get_ip()
port_address = '9090'
link = 'http://'+str(IP)+':'+port_address+'/Team' # 'http://10.156.248.26:9090/Team'
random_link = random.randint(1, 999999999999)

for i in range(5):
    team_link = link+str(i+1)+'/'+team[i]+'/'+str(random_link)
    img = qr_generator(team_link)
    save_name = "Team_"+str(i+1)+".png"
    img.save(save_name)

app = Flask(__name__)

def data_entry(Team, arm):
    global session_flag, total_score, random_numbers, options_store, Round
    Team = int(Team)
    if session_flag[Team] == 1 and Round<number_rounds:
        if (int(arm) < 6):
            tmp = generate_random(arm)
        else:
            tmp = -25

        options_store[Round, Team] = int(arm)
        session_flag[Team] = 0
        random_numbers[Round, Team] = tmp
        total_score[Team] += tmp
        tmp_msg = str(Round+1) + " " + str(options_store[Round, Team]) + " " + str(random_numbers[Round, Team]) + " " + str(total_score[Team])

    if (Round==number_rounds):
        tmp_msg = str(Round) + " " + str(options_store[Round-1, Team]) + " " + str(random_numbers[Round-1, Team]) + " " + str(total_score[Team])
    
    return tmp_msg

def table_maker(arrays):
    y = ' '.join(map(str, arrays))
    y = y.replace(' ', ':')
    return y

@app.route('/Team1/Air'+'/'+str(random_link), methods=['GET', 'POST'])
def Air():
    if request.method == 'GET':
        return render_template('Air.html')

    elif request.method == 'POST' and start_game:
        msg = request.form['msg']
        print (msg)
        team, option = msg.split(": ")
        tmp_msg = data_entry(0, option)
        print 'Air: ' + option
        return tmp_msg

@app.route('/Team2/Earth'+'/'+str(random_link), methods=['GET', 'POST'])
def Earth():
    if request.method == 'GET':
        return render_template('Earth.html')

    elif request.method == 'POST' and start_game:
        msg = request.form['msg']
        team, option = msg.split(": ")
        tmp_msg = data_entry(1, option) 
        print 'Earth: ' + option
        return tmp_msg
        

@app.route('/Team3/Fire'+'/'+str(random_link), methods=['GET', 'POST'])
def Fire():
    if request.method == 'GET':
        return render_template('Fire.html')

    elif request.method == 'POST' and start_game:
        msg = request.form['msg']
        team, option = msg.split(": ")
        tmp_msg = data_entry(2, option)
        print 'Fire: ' + option 
        return tmp_msg
       

@app.route('/Team4/Metal'+'/'+str(random_link), methods=['GET', 'POST'])
def Metal():
    if request.method == 'GET':
        return render_template('Metal.html')

    elif request.method == 'POST' and start_game:
        msg = request.form['msg']
        team, option = msg.split(": ")
        tmp_msg = data_entry(3, option) 
        print 'Metal: ' + option
        return tmp_msg

@app.route('/Team5/Water'+'/'+str(random_link), methods=['GET', 'POST'])
def Water():
    if request.method == 'GET':
        return render_template('Water.html')

    elif request.method == 'POST' and start_game:
        msg = request.form['msg']
        team, option = msg.split(": ")
        tmp_msg = data_entry(4, option)
        print 'Water: ' + option
        return tmp_msg

@app.route('/Scoreboard'+'/'+str(random_link), methods=['GET', 'POST'])
def Scoreboard():
    global session_flag, total_score, lap, random_numbers, options_store, Round, start_game

    if request.method == 'GET':
        return render_template('Scoreboard.html')

    elif request.method == 'POST' and Round<number_rounds:
        msg = request.form['msg']
        print (msg)
        if msg == 'begin_game!':
            if start_game == 0:
                start_game = 1
                tmp_msg = 'game_started!'
                return tmp_msg
            else:
                tmp_msg = 'game_inprogress!'
                return tmp_msg


        if msg == 'T_over':
            tmp_msg = str(Round+2)
            if (Round==number_rounds-1):
                tmp_msg = 'Finished!'

            for i in range(5):
                if session_flag[i] == 1:
                    # Generate a random number between 1 to 5...
                    option = 6 # random.randint(1, 5) # 6
                    tmp = data_entry(i, option) # Change it to -10...
                    
            for i in range(5):
                tmp_msg = tmp_msg + " " + str(total_score[i]) 
            
            o1 = str( options_store[0, 0] )
            o2 = str( options_store[0, 1] )
            o3 = str( options_store[0, 2] )
            o4 = str( options_store[0, 3] )
            o5 = str( options_store[0, 4] )
            t1 = str( random_numbers[0, 0] )
            t2 = str( random_numbers[0, 1] )
            t3 = str( random_numbers[0, 2] )
            t4 = str( random_numbers[0, 3] )
            t5 = str( random_numbers[0, 4] )

            if (Round<=table_size and Round >= 1):
                o1 = table_maker(options_store[0:Round+1, 0])
                o2 = table_maker(options_store[0:Round+1, 1])
                o3 = table_maker(options_store[0:Round+1, 2])
                o4 = table_maker(options_store[0:Round+1, 3])
                o5 = table_maker(options_store[0:Round+1, 4])

                t1 = table_maker(random_numbers[0:Round+1, 0])
                t2 = table_maker(random_numbers[0:Round+1, 1])
                t3 = table_maker(random_numbers[0:Round+1, 2])
                t4 = table_maker(random_numbers[0:Round+1, 3])
                t5 = table_maker(random_numbers[0:Round+1, 4])
            
            elif (Round>table_size and Round > 1):
                o1 = table_maker(options_store[Round-table_size+1:Round+1, 0])
                o2 = table_maker(options_store[Round-table_size+1:Round+1, 1])
                o3 = table_maker(options_store[Round-table_size+1:Round+1, 2])
                o4 = table_maker(options_store[Round-table_size+1:Round+1, 3])
                o5 = table_maker(options_store[Round-table_size+1:Round+1, 4])

                t1 = table_maker(random_numbers[Round-table_size+1:Round+1, 0])
                t2 = table_maker(random_numbers[Round-table_size+1:Round+1, 1])
                t3 = table_maker(random_numbers[Round-table_size+1:Round+1, 2])
                t4 = table_maker(random_numbers[Round-table_size+1:Round+1, 3])
                t5 = table_maker(random_numbers[Round-table_size+1:Round+1, 4])

            tmp_msg = tmp_msg+" "+o1+"$"+t1+"|"+o2+"$"+t2+"|"+o3+"$"+t3+"|"+o4+"$"+t4+"|"+o5+"$"+t5
            session_flag = np.ones(5)
            Round += 1
            return tmp_msg
    
    elif request.method == 'POST' and Round>=number_rounds:
        tmp_msg = 'Finished!'
        start_game = 0
        for i in range(5):
            tmp_msg = tmp_msg + " " + str(total_score[i]) 
        return tmp_msg

if __name__ == "__main__":
    print "IP: "+str(IP)
    print "Secret Key: "+str(random_link)+"\n\n"
    app.run(debug=False, host='0.0.0.0', port='9090')
