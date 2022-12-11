import os, argparse
import openai

HISTORY_PATH='history.log'
openai.api_key =os.environ['OPEN_AI_KEY']

parser = argparse.ArgumentParser(description='会話内容を入力してください')
parser.add_argument('input')
parser.add_argument('-r', '--reset', action='store_true',help='会話履歴(history.log)を初期化して実行する')
args = parser.parse_args()

history=''
# リセットフラグが立っていない&ファイルが存在する場合履歴を読み込む
if os.path.isfile(HISTORY_PATH) and not args.reset:
  with open(HISTORY_PATH, 'r') as f:
    history = f.read()

print(args.input)
# 会話として推論するため、会話ログを付け足してリクエストする
prompt = history + args.input

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
print(texts)

# 会話履歴の保存
with open(HISTORY_PATH, 'w') as f:
  f.write(prompt)
  f.write(texts)
  # 文の切れ目に改行を追加
  f.write('\n\n')