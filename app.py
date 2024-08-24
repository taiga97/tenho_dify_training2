from logging import getLogger, DEBUG, StreamHandler
from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd

import gradio as gr
import openai

load_dotenv()

logger = getLogger()
logger.setLevel(DEBUG)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.addHandler(handler)

dify_api_key = os.environ["DIFY_API_KEY"]

def get_QA_table(web_url, number):

    url = 'https://api.dify.ai/v1/workflows/run'
    headers = {
        'Authorization': f'Bearer {dify_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "inputs": {
              "campany_web_url": web_url,
              "question_num": number,
        },
        "response_mode": "blocking",
        "user": "abc-123"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # res.textがJSON形式の文字列であることを仮定
    try:
        res_dict = json.loads(response.text)  # JSON文字列を辞書に変換
        logger.info(f"response dict：{res_dict}")
        res_output = res_dict["data"]["outputs"]["result"]
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")

    q_list = res_output["q_list"]
    a_list = res_output["a_list"]


    # 仮にデータを作成（ここではURLや数字に基づいて動的にデータを生成できる）
    # データフレームを作成
    df = pd.DataFrame({
        'Question': q_list,
        'Answer': a_list
    })
    
    # 表をHTMLにして返す
    return df.to_html()

# Gradioのインターフェース
with gr.Blocks() as demo:
    gr.Markdown("営業想定質問&回答生成ツール")

    # URL入力ボックス
    url_input = gr.Textbox(label="営業先URLを入力", placeholder="https://example.com")
    
    # 数字入力ボックス
    number_input = gr.Number(label="質問数を入力", value=1)
    
    # 実行ボタン
    submit_button = gr.Button("実行")
    
    # 表の出力エリア
    table_output = gr.HTML()

    # 実行ボタンが押されたときのアクションを定義
    submit_button.click(
        fn=get_QA_table,          # 実行される関数
        inputs=[url_input, number_input],  # 関数の入力
        outputs=table_output        # 関数の出力
    )


if __name__ == "__main__":
    demo.launch(show_api=False, server_name="0.0.0.0", share=True)
    # demo.launch(share=True)