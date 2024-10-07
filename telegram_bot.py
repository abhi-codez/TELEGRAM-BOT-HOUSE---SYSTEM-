
import telebot
from telebot import types

# Replace with your own API Token
API_TOKEN = '7372346462:AAEtSat9xXGGoIDSKNBC0t73E6yT61aup4I'

bot = telebot.TeleBot(API_TOKEN)

# Updated Data including phone numbers and house name correction to "Raja Krishnadevaraya"
houses = {
    "Maharana Pratap": {
        "Faculty In-Charge": "Dr. Ashwini Sapkal",
        "Faculty Representatives": ["Mr. Girish Kapse", "Ms. Sushma Shirke", "Mr. Anand Ramgude", "Rohan Sonawane"],
        "House BE Mentor": [("Pranay Puniya", "7581847604"), ("Aditi More", "9501501733")],
        "Captains": [("Krishna Kumar", "8941918900"), ("Ashritha Reddy", "7386705828")],
        "Vice-Captains": [("Shivam Sharma", "8354099643"), ("Ritika Kumari", "8824693065")]
    },
    "Chhatrapati Shivaji Maharaj": {
        "Faculty In-Charge": "Prof MB Lonare",
        "Faculty Representatives": ["Mr. Vijay Karra", "Mr. Sandeep Sampleti", "Dr. SM Gaikwad", "Prakash K"],
        "House BE Mentor": [("Piyush", "7905061506"), ("Anushna Panwar", "9971081972")],
        "Captains": [("Pratham Kumar", "7037719984"), ("Khushia", "7850005774")],
        "Vice-Captains": [("Shivang Kumar", "6395926392"), ("Khushi Yadav", "9256517911")]
    },
    "Raja Krishnadevaraya": {
        "Faculty In-Charge": "Dr. Pritee Purohit",
        "Faculty Representatives": ["Mr. Sukumar Chaughule", "Mr. Yuvraj Gholap", "Ms. Sita Yadav", "A Jirgale"],
        "House BE Mentor": [("Shivram", "9351447398"), ("Ritika", "8983829429")],
        "Captains": [("Rohit Kumar", "9462007399"), ("Shaikh Haseena", "8459258517")],
        "Vice-Captains": [("Piyush Saini", "9599478220"), ("Kratika Rai", "6267007012")]
    },
    "Samrat Ashoka": {
        "Faculty In-Charge": "Prof JB Jawale",
        "Faculty Representatives": ["Dr. Dipika Birari", "Mr. Anup Kadam", "Ms. Gouri Bhasale", "Pravin Sangle"],
        "House BE Mentor": [("Ayush Ojha", "6264389700"), ("Akriti Singh", "7457924466")],
        "Captains": [("Ankit Yadav", "7494924041"), ("Tanisha Sharma", "9419604895")],
        "Vice-Captains": [("Akash Singh", "9571266507"), ("Sunandha", "9571067672")]
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    markup.add('Maharana Pratap', 'Chhatrapati Shivaji Maharaj', 'Raja Krishnadevaraya', 'Samrat Ashoka')
    msg = bot.reply_to(message, "Choose your house:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_house_choice)

def process_house_choice(message):
    house = message.text
    if house in houses:
        user_house = house
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
        markup.add('Faculty In-Charge', 'Faculty Representatives', 'House BE Mentor', 'Captains', 'Vice-Captains')
        msg = bot.reply_to(message, f"You chose {house}. Now select representative type:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_representative_choice, user_house)
    else:
        bot.reply_to(message, "Invalid house choice. Please try again.")

def process_representative_choice(message, house):
    rep_type = message.text
    if rep_type in houses[house]:
        reps = houses[house][rep_type]
        markup = types.InlineKeyboardMarkup()

        # If it's a list of tuples (with names and phone numbers), display the names as buttons
        if isinstance(reps, list) and isinstance(reps[0], tuple):
            for name, phone in reps:
                # Create a button for each name, and the callback data will be the phone number
                markup.add(types.InlineKeyboardButton(text=name, callback_data=phone))
        elif isinstance(reps, list):
            # For a simple list, no phone numbers, just display as text
            reps_list = '\n'.join(reps)
            bot.reply_to(message, f"The {rep_type} for {house} are:\n{reps_list}")
            return
        else:
            bot.reply_to(message, f"The {rep_type} for {house} is {reps}.")
            return

# Send the list of names as buttons
        bot.send_message(message.chat.id, f"Select a name to see the phone number for {rep_type} in {house}:", reply_markup=markup)
    else:
        bot.reply_to(message, "Invalid representative type. Please try again.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # When the user clicks a button, reveal the phone number
    bot.answer_callback_query(call.id, f"Phone number: {call.data}")

# Polling the bot
bot.polling()
