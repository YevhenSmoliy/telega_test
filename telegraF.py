import datetime
import telebot
import time
import sys
#from telebot import types
import sqlite3
import configparser

# bot tokken and connection to db
config = configparser.ConfigParser()
config.read('parameters.ini')
api_key = (config['key']['api_key'])
bot = telebot.TeleBot(api_key)
conn = sqlite3.connect('test_v0.3C.db')
cursor = conn.cursor()


# user_dict = {}


class BankAccount:
    # class for balance and take max value from db
    cursor.execute("SELECT balance FROM Doroga1 ORDER BY balance DESC LIMIT 1")
    Full_value_bd = cursor.fetchall()
    Full_value = Full_value_bd[0]
    Full, = Full_value

    def __init__(self, name, amount):  # main function
        self.name = name
        self.amount = amount
        BankAccount.Full += (amount)
        # cursor.execute("INSERT INTO Doroga1 VALUES(?,?,?)",(BankAccount.doroga,self.amount,self.name))
        # conn.commit()


@bot.message_handler(commands=['start', 'Start'])
def echo_msg(message):
    bot.send_message(chat_id=message.chat.id,
                            text='Hello!Nice too see you again. /add - if you wanna ad smth,/info - if you wanna see total minus,/last - to see last 5 inputs.......Version 0.3C)')


# bot start message
@bot.message_handler(commands=['add', 'Add'])
def echo_msg2(message):
    echo = bot.send_message(chat_id=message.chat.id,
                            text='so what you wanna add?')
    bot.register_next_step_handler(message=echo, callback=extract_msg)


# command to add

@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(message.chat.id, 'Total minus:' + str(BankAccount.Full))


@bot.message_handler(commands=['last'])
def last_message(message):
    bot.send_message(message.chat.id, '5 last adds')
    conn = sqlite3.connect('test_v0.3C.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doroga1 ORDER BY balance DESC LIMIT 5")
    last = cursor.fetchall()
    for x in last:
        print(x)
        bot.send_message(message.chat.id, str(x))


def extract_msg(message):
    global Name1  # be global to use it in another function
    msg = (message.text)
    print(msg)
    Name1 = msg
    echo = bot.send_message(message.chat.id, 'price?')
    bot.register_next_step_handler(message=echo, callback=price_d)
    # get first value=name,make it global


def price_d(message):
    conn = sqlite3.connect('test_v0.3C.db')
    cursor1 = conn.cursor()
    msg2 = (message.text)
    print(msg2)
    price1 = msg2
    # take 2 value Price and make it float for object and class
    custumer = BankAccount(Name1, float(price1))
    print(custumer)
    print(BankAccount.Full)
    timec = datetime.datetime.now()
    cursor1.execute("INSERT INTO Doroga1 VALUES(?,?,?,?)", (Name1, price1, BankAccount.Full, timec))
    conn.commit()
    bot.send_message(message.chat.id,
                     'You add: ' + str(Name1) + '\n' + '.With price:' + price1 + '\n' + " Total minus:" + str(
                         BankAccount.Full))
    # add all creatind valuse in db,bot print valus for us,end


def main_loop():
    bot.polling(none_stop=True)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:

        sys.exit(0)
