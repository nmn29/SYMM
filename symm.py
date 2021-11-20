import discord
from discord.ext import commands
import traceback
import os

intents = discord.Intents.all()
cogs = [
   'cogs.help', 
   'cogs.symmetry',
    ]

#cogs.help = ヘルプコマンド
#cogs.symmetry = シンメトリー処理の実行

class MyBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self, command_prefix,help_command,intents):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix,help_command,intents=intents)

        # cogsに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()
        
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

if __name__ == '__main__':
    BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
    bot = MyBot(command_prefix='s!', help_command=None, intents=intents)
    #command_prefix='/'でコマンドの開始文字を指定
    
    bot.run(BOT_TOKEN) # Botのトークン