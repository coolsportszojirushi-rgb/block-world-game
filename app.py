import streamlit as st
from google import genai
from PIL import Image
import io
import os

st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")
st.sidebar.write("---")
st.sidebar.subheader("合成する商品の設定")

product_options = {
    "ホワイトパワーセラム": "wps.png",
    "レッドパワーセラム": "rps.png",
    "ベーシックプラス": "basicplus.png",
    "アイビーコスモス2": "cosmos2.png",
    "アトラクティ": "attracty.png",
    "メンズワン": "mensone.png",
    "ブライト＆クリアマスク": "brightmask.png",
    "サーマンスボディエステ": "thermince.png",
    "ステムシグナル": "stemsignal.png",
    "グルコサミンNA": "glucosamine.png",
    "モイストシートエンリッチ": "moistsheet.png",
    "エクラデュール": "eclatdure.png",
    "ピーリングローション": "peeling.png",
    "ホワイトスティックC": "whitestick.png",
    "リップリペアクリーム": "liprepair.png",
    "ガーランド": "garland.png",
    "自分で画像をアップロードする": "upload",
    "合成しない（背景のみ）": "none"
}

selected_product = st.sidebar.selectbox("商品を選んでください", list(product_options.keys()))

uploaded_file = None
if product_options[selected_product] == "upload":
    uploaded_file = st.sidebar.file_uploader("商品の切り抜き画像（PNG形式）を選択してください", type=["png"])

default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。透明感のある肌へと導きます。"
script_text = st.text_area("美容台本を入力してください", value=default_script, height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("左側のメニューからAPIキーを入力してください。")
    else:
        st.info("最新のAIで背景を生成し、商品を合成しています。少々お待ちください。")
        try:
            client = genai.Client(api_key=api_key)
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                if len(sentence) <= 1:
                    continue
                    
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                prompt_text = f"美容コスメ広告用の美しい背景画像。中央には何も描かずスペースを空けておくこと。文字やボトルは不要。内容：{sentence}"
                
                result = client.models.generate_images(
                    model='imagen-4.0-generate-001',
                    prompt=prompt_text,
                    config=dict(number_of_images=1)
                )
                
                for generated_image in result.generated_images:
                    bg_image = Image.open(io.BytesIO(generated_image.image.image_bytes)).convert("RGBA")
                    product_img = None
                    
                    if product_options[selected_product] == "upload" and uploaded_file is not None:
                        product_img = Image.open(uploaded_file).convert("RGBA")
                    elif product_options[selected_product] not in ["upload", "none"]:
                        file_path = product_options[selected_product]
                        if os.path.exists(file_path):
                            product_img = Image.open(file_path).convert("RGBA")
                        else:
                            st.warning(f"【画像の準備が必要です】 {file_path} という名前の画像ファイルがGitHubにありません。Canva等で商品を切り抜き、この名前で保存してGitHubに追加してください。今回は背景のみを表示します。")
                    
                    if product_img is not None:
                        target_height = bg_image.height // 2
                        aspect_ratio = product_img.width / product_img.height
                        target_width = int(target_height * aspect_ratio)
                        product_img = product_img.resize((target_width, target_height))
                        
                        x = (bg_image.width - target_width) // 2
                        y = (bg_image.height - target_height) // 2
                        
                        bg_image.paste(product_img, (x, y), product_img)
                        st.image(bg_image, caption=f"シーン {index + 1}（商品合成版）")
                    else:
                        st.image(bg_image, caption=f"シーン {index + 1}（背景のみ）")
                
                st.write("---")
        except Exception as e:
            st.error(f"詳細エラーが発生しました：{e}")
