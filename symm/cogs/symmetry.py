import aiohttp
import io
import re

import discord
from discord.ext import commands
from PIL import Image, ImageOps

habaL = {
    "1": 1.6,
    "2": 1.7,
    "3": 1.8,
    "4": 1.9,
    "5": 2,
    "6": 2.1,
    "7": 2.2,
    "8": 2.3,
    "9": 2.4,
    "10": 2.5,
}


pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+.(jpg|png|gif|bmp)"

class Symm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.img = None
        self.ch_images = dict()

    @commands.Cog.listener()
    async def on_message(self, message):

        self.contents = message.content.split(" ")

        if message.author.bot:
            return

        ch_id = message.channel.id

        if message.attachments:

            for attachment in message.attachments:

                #送られた画像の取得
                if attachment.url.endswith(("png", "jpg", "jpeg", "bmp", "jfif")):

                    attachment = message.attachments[0]

                    img_in = await attachment.read()
                    img_bin = io.BytesIO(img_in)

                    self.img = Image.open(img_bin)

                    self.ch_images[str(ch_id)] = self.img

        elif re.match(pattern, message.content) and message.content.endswith(("png", "jpg", "jpeg")):
            async with aiohttp.ClientSession() as session:
                async with session.get(message.content) as res:
                    if res.status == 200:
                        img_bin = io.BytesIO(await res.read())
                        self.img = Image.open(img_bin)
                        self.ch_images[str(ch_id)] = self.img


    @commands.command()
    async def sym(self, ctx, haba=None):
        await self.execute(ctx, haba)

    @commands.command()
    async def syml(self, ctx, haba=None):
        await self.execute(ctx, haba)

    @commands.command()
    async def symr(self, ctx, haba=None):
        await self.execute(ctx, haba)

    async def execute(self, ctx, haba):
        if str(ctx.channel.id) not in self.ch_images.keys():
            await ctx.send("画像がありません")
        else:
            images = []
            if haba is None:
                images.extend(
                    self.symmetry(ctx.command.name,
                                  self.ch_images[str(ctx.channel.id)]))
            elif haba:
                images.extend(
                    self.symmetry(
                        ctx.command.name,
                        self.ch_images[str(ctx.channel.id)],
                        habaL[haba],
                    ))

            # 変換した画像をチャンネルに送信
            for image in images:
                await ctx.send(file=discord.File(fp=image, filename="res.png"))

    def symmetry(self, command, img, haba=2):
        """シンメトリー処理（画像の左側）"""
        bs = list()

        if command in ("syml", "sym"):

            imgl = img

            imgl_1 = imgl.crop((0, 0, imgl.size[0] // haba, imgl.size[1]))
            imgl_2 = ImageOps.mirror(imgl_1)
            syml = Image.new('RGBA', (imgl_1.width + imgl_2.width, imgl_1.height))
            syml.paste(imgl_1, (0, 0))
            syml.paste(imgl_2, (imgl_1.width, 0))
            b = io.BytesIO()
            syml.save(b, format="PNG")
            bs.append(io.BytesIO(b.getvalue()))


        if command in ('symr', 'sym'):

            imgr = img

            imgr_1 = imgr.crop(
                (imgr.size[0] // haba, 0, imgr.size[0], imgr.size[1]))
            imgr_2 = ImageOps.mirror(imgr_1)

            symr = Image.new('RGBA', (imgr_1.width + imgr_2.width, imgr_1.height))
            symr.paste(imgr_2, (0, 0))
            symr.paste(imgr_1, (imgr_1.width, 0))

            b = io.BytesIO()
            symr.save(b, format='PNG')
            bs.append(io.BytesIO(b.getvalue()))

        return bs


def setup(bot):
    bot.add_cog(Symm(bot))
