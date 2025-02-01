from VK_Bot import Bot, group_id
from Token import token

if __name__ == '__main__':
    bot = Bot(group_id, token)
    bot.run()
