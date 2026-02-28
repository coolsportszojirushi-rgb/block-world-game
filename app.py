import streamlit as st
import google.generativeai as genai
from PIL import Image

# 基本設定
st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

# サイドバー設定
api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

# 春の主力、ホワイトパワーセラムの初期台本
default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。みずみずしいテクスチャーで、透明感のある肌へと導きます。"
script_text = st.text_area("美容台本を入力してください", value=default_script, height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        st.info("最新のNano Banana 2 (Imagen 3) でイラストを生成中...")
        try:
            genai.configure(api_key=api_key)
            
            # 文章を分割
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                # 画像生成モデルの呼び出し（最新の記述方法）
                try:
                    # モデル名の指定
                    model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                    
                    # 生成実行
                    response = model.generate_images(
                        prompt=f"美容・コスメ広告用の高品質な正方形イラスト。余計な文字は不要。内容：{sentence}",
                        number_of_images=1
                    )
                    
                    # 画像の表示
                    if response.images:
                        st.image(response.images[0].image, caption=f"シーン {index + 1}")
                
                except Exception as inner_e:
                    st.error(f"画像生成中にエラーが発生しました。設定が反映されるまで数分かかる場合があります。詳細: {inner_e}")
                
                st.markdown("---")
                
        except Exception as e:
            st.error(f"システム全体のエラー：{e}")
