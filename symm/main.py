import os
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
cogs = [
    ".cogs.help",
    ".cogs.symmetry",
]

# cogs.help = ヘルプコマンド
# cogs.symmetry = シンメトリー処理の実行


class SymmBot(commands.Bot):
    def __init__(self, command_prefix, help_command, intents):
        """SymmBotのコンストラクタ。"""
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix, help_command, intents=intents)

        # cogsに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("-----")
        print(self.user.name)
        print(self.user.id)
        print("-----")


def main():
    load_dotenv()
    try:
        BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    except KeyError:
        raise ValueError("`DISCORD_BOT_TOKEN` is not defined in your env.")

    # command_prefix='s!'でコマンドの開始文字を指定
    bot = SymmBot(command_prefix="s!", help_command=None, intents=intents)
    bot.run(BOT_TOKEN) # Botのトークン


if __name__ == "__main__":
    main()
