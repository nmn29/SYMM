import discord
from discord import file
from discord.flags import PublicUserFlags 
from PIL import Image, ImageOps
import io



# load .env file
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

habaL = {'1':1.6, '2':1.7, '3':1.8, '4':1.9, '5':2, '6':2.1, '7':2.2, '8':2.3, '9':2.4, '10':2.5}
ch_images = dict()
ch_id = -1



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
    global ch_id

    contents = message.content.split(' ')

    if message.author.bot:
        return

    ch_id = message.channel.id

    if message.attachments:
        

        for attachment in message.attachments:

            #送られた画像の取得
            if attachment.url.endswith(("png", "jpg", "jpeg")):

                attachment = message.attachments[0]

                img_in = await attachment.read()
                img_bin = io.BytesIO(img_in)

                img = Image.open(img_bin)

                ch_images[str(ch_id)] = img

    if contents[0] in ('/sym', '/syml', '/symr'):

        if str(ch_id) not in ch_images.keys():
            await message.channel.send('画像がありません')
        else:
            if len(contents) == 1:
                images = symmetry(contents[0], ch_images[str(ch_id)])
            elif contents[1]:
                images = symmetry(contents[0], ch_images[str(ch_id)], habaL[contents[1]])

            # 変換した画像をチャンネルに送信
            for image in images:
                await message.channel.send(file=discord.File(fp=image, filename='res.png'))

#シンメトリー変換関数
def symmetry(command, img, haba=2):
    
    bs = list()
    
    if command in ('/syml', '/sym'):

        imgl = img

        imgl_1 = imgl.crop((0, 0, imgl.size[0] // haba, imgl.size[1]))
        imgl_2 = ImageOps.mirror(imgl_1)

        syml = Image.new('RGB', (imgl_1.width + imgl_2.width, imgl_1.height))
        syml.paste(imgl_1, (0, 0))
        syml.paste(imgl_2, (imgl_1.width, 0))
        b = io.BytesIO()
        syml.save(b, format='PNG')
        bs.append(io.BytesIO(b.getvalue()))

    if command in ('/symr', '/sym'):

        imgr = img

        imgr_1 = imgr.crop((imgr.size[0] // haba, 0, imgr.size[0], imgr.size[1]))
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


