import discord
from discord import file
from discord.flags import PublicUserFlags 
from PIL import Image, ImageOps
import io



# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'OTA5MjU5NTM1NDY4ODU5NDIy.YZBr7g.1zPB0NoAxYa7LW6sQ5CsBDFbi10'

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

@client.event
async def on_message(message):

    global img

    if message.author.bot:
        return

    if message.attachments:

        for attachment in message.attachments:

            #送られた画像の取得
            if attachment.url.endswith(("png", "jpg", "jpeg")):

                attachment = message.attachments[0]

                img_in = await attachment.read()
                img_bin = io.BytesIO(img_in)

                img = Image.open(img_bin)

    if message.content in ('/sym', '/syml', '/symr'):

        # 取得した画像をコマンドに応じてシンメトリーに変換
        images = symmetry(message, img)

        # 変換した画像をチャンネルに送信
        for image in images:
            await message.channel.send(file=discord.File(fp=image, filename='res.png'))


#シンメトリー変換関数
def symmetry(message, img):
    bs = list()
    if message.content in ('/syml', '/sym'):

        imgl = img

        imgl_1 = imgl.crop((0, 0, imgl.size[0] // 2, imgl.size[1]))
        imgl_2 = ImageOps.mirror(imgl_1)

        syml = Image.new('RGB', (imgl_1.width + imgl_2.width, imgl_1.height))
        syml.paste(imgl_1, (0, 0))
        syml.paste(imgl_2, (imgl_1.width, 0))
        b = io.BytesIO()
        syml.save(b, format='PNG')
        bs.append(io.BytesIO(b.getvalue()))

    if message.content in ('/symr', '/sym'):

        imgr = img

        imgr_1 = imgr.crop((imgr.size[0] // 2, 0, imgr.size[0], imgr.size[1]))
        imgr_2 = ImageOps.mirror(imgr_1)

        syml = Image.new('RGB', (imgr_1.width + imgr_2.width, imgr_1.height))
        syml.paste(imgr_1, (0, 0))
        syml.paste(imgr_2, (imgr_1.width, 0))
        b = io.BytesIO()
        syml.save(b, format='PNG')
        bs.append(io.BytesIO(b.getvalue()))

    return bs





# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)


