from scrap import scrape_witanime
import telebot
from telebot import types
from dn import get_decoded_urls
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6991610719:AAFe95FKTVzXKJIB8RDklWrlynIa-tkTQQA'
bot = telebot.TeleBot(TOKEN)
episodes_list = []
servers_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://witanime.cyou/',
    'Upgrade-Insecure-Requests': '1'
}
# Define the command handler for /get_animes
@bot.message_handler(commands=['gtsrv'])
def handle_get_animes(message):
    chat_id = message.chat.id
    data_list = scrape_witanime("https://witanime.cyou")
    global episodes_list
    episodes_list = data_list
    data_list  = data_list[:4]
    send_images_with_buttons(chat_id, data_list)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    helper  = """   *Welcome To you with scapy Bot*\n
We Provide You With The most recent 
anime and episodes 
real time videos or links to the
download videos

💻 *for servers* 👉 /gtsrv

🎥 *for videos*  👉 /getvid

🔥 *Enjoy My Friend*
"""
    
    bot.send_message(message.chat.id,helper,parse_mode="Markdown")



# Function to send images with captions and inline keyboards
def send_images_with_buttons(chat_id, data_list):
    for idx,data in enumerate(data_list):
        # Extract information from the dictionary
        img_url = data.get('img_url')
        title = data.get('title')
        episode = data.get('episode')
        url = data.get('url')
        print(url)

        # Ensure url is properly encoded and within length limit
        #callback_data = url[:64]  # Truncate if necessary
        if img_url and title and episode and url:
            # Create inline keyboard button
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text=episode, callback_data=str(idx))
            markup.add(button)

            # Send the photo with caption and inline keyboard
            bot.send_message(chat_id,title,reply_markup=markup)

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global servers_list
    # Handle the callback data
    if is_integer(call.data):
        global episodes_list
        

        ep = episodes_list[int(call.data)]
        urls_servers = get_decoded_urls(ep["url"])
        servers_list = urls_servers
        markup = types.InlineKeyboardMarkup()
        bot.send_photo(chat_id=call.message.chat.id,photo=ep["img_url"],caption=f'{ep["title"]} \n.\n.\n.\n🎞*Servers list*💻',parse_mode="Markdown")
        for idx,url in enumerate(urls_servers):
            srv_title = url.split("/")[2]
            srv_url   = f"server:{idx}"

            button = types.InlineKeyboardButton(text=srv_title, callback_data=srv_url)
            markup.add(button)

        bot.send_message(call.message.chat.id,"📺Magic🚀",reply_markup=markup)


    elif "server" in call.data:

        if len(servers_list) > 0: 
            tx1 = call.data.replace("server:","")
            srv_int = int(tx1)
            srv = servers_list[srv_int]
            print(srv)
            bot.send_message(call.message.chat.id,srv)
        else:
            bot.send_message(call.message.chat.id,"🧹 *Bot Server list is Empty*",parse_mode="Markdown")

    



def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False








# Polling loop to keep the bot running
if __name__ == "__main__":
    bot.polling(none_stop=True)
