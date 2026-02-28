import streamlit as st
from google import genai
from PIL import Image
import io
import os

st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

# サイドバーの設定
api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("合成する商品の設定")

# 商品の選択肢と画像ファイル名の対応表
product_options = {
    "ホワイトパワーセラム": "wps_bottle.png",
    "レッドパワーセラム": "rps_bottle.png",
    "アイビーコスモス2": "cosmos2_bottle.png",
    "アトラクティ": "attracty_bottle.png",
    "メンズワン": "mensone_bottle.png",
    "自分で画像をアップロードする": "upload",
    "合成しない（背景のみ）": "none"
}

# プルダウンメニューで商品を選択
selected_product = st.sidebar.selectbox("商品を選んでください", list(product_options.keys()))

# アップロード機能の表示
uploaded_file = None
if product_options[selected_product] == "upload":
    uploaded_file = st.sidebar.file_uploader("商品の切り抜き画像（PNG形式）を選択してください", type=["png"])

# 台本の入力エリア
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
                
                # AIには背景だけを作らせる専用の指示
                prompt_text = f"美容コスメ広告用の美しい背景画像。中央には何も描かずスペースを空けておくこと。文字やボトルは不要。内容：{sentence}"
                
                result = client.models.generate_images(
                    model='imagen-4.0-generate-001',
                    prompt=prompt_text,
                    config=dict(number_of_images=1)
                )
                
                for generated_image in result.generated_images:
                    # AIが生成した背景画像を準備
                    bg_image = Image.open(io.BytesIO(generated_image.image.image_bytes)).convert("RGBA")
                    
                    # 合成する商品画像の準備
                    product_img = None
                    
                    if product_options[selected_product] == "upload" and uploaded_file is not None:
                        # ユーザーがアップロードした画像を使用
                        product_img = Image.open(uploaded_file).convert("RGBA")
                    elif product_options[selected_product] not in ["upload", "none"]:
                        # 登録済みの画像を使用
                        file_path = product_options[selected_product]
                        if os.path.exists(file_path):
                            product_img = Image.open(file_path).convert("RGBA")
                        else:
                            st.warning(f"商品画像 {file_path} が見つかりません。背景のみ表示します。")
                    
                    # 背景と商品の合成処理
                    if product_img is not None:
                        # 商品が背景の高さの半分になるようにサイズを自動調整
                        target_height = bg_image.height // 2
                        aspect_ratio = product_img.width / product_img.height
                        target_width = int(target_height * aspect_ratio)
                        product_img = product_img.resize((target_width, target_height))
                        
                        # 画像のど真ん中に配置する計算
                        x = (bg_image.width - target_width) // 2
                        y = (bg_image.height - target_height) // 2
                        
                        # 重ね合わせる
                        bg_image.paste(product_img, (x, y), product_img)
                        st.image(bg_image, caption=f"シーン {index + 1}（商品合成版）")
                    else:
                        # 合成しない場合、または画像がない場合は背景のみを表示
                        st.image(bg_image, caption=f"シーン {index + 1}（背景のみ）")
                
                st.markdown("---")
        except Exception as e:
            st.error(f"詳細エラーが発生しました：{e}")
