import os
import discord
import openai

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
CHANNELID = os.environ['PRIME_CHANNELID']
openai.api_key =os.environ['OPEN_AI_KEY']
HISTORY_PATH='history.log'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print('ログインしました')

# @client.event
# async def on_message(message):
#     if not message.author.bot:
#         channel = client.get_channel(CHANNELID)
#         if(message.channel==channel):
#             print(message.content)
#             if str(message.content).isdigit():
#                 await channel.send(prime_factorize(int(message.content)))
#             elif str(message.content)[0]=='=':
#                 await channel.send('ans='+str(eval(str(message.content)[1:])))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('?history_reset'):
        await message.channel.send('会話データをリセットします')
        with open(HISTORY_PATH, 'w') as f:
            f.write('')
        return
    
    if message.content.startswith('?'):
        history=''
        # リセットフラグが立っていない&ファイルが存在する場合履歴を読み込む
        if os.path.isfile(HISTORY_PATH):
            with open(HISTORY_PATH, 'r') as f:
                history = f.read()

        print(str(message.content)[1:])
        # 会話として推論するため、会話ログを付け足してリクエストする
        prompt = history + str(message.content)[1:]

        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0, # ランダム性の制御[0-1]
            max_tokens=1000, # 返ってくるレスポンストークンの最大数
            top_p=1.0, # 多様性の制御[0-1]
            frequency_penalty=0.0, # 周波数制御[0-2]：高いと同じ話題を繰り返さなくなる
            presence_penalty=0.0 # 新規トピック制御[0-2]：高いと新規のトピックが出現しやすくなる
        )

        texts = ''.join([choice['text'] for choice in response.choices])

        await message.channel.send(texts)

        # 会話履歴の保存
        with open(HISTORY_PATH, 'w') as f:
            f.write(prompt)
            f.write(texts)
            # 文の切れ目に改行を追加
            f.write('\n\n')

client.run(DISCORD_TOKEN)
