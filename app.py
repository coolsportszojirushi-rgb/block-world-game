import streamlit as st
from google import genai
from google.genai import types

# 基本設定
st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

# サイドバー設定
api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。みずみずしいテクスチャーで、透明感のある肌へと導きます。"
script_text = st.text_area("美容台本を入力してください", value=default_script, height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        st.info("Imagen 3 でイラストを生成中...")
        try:
            client = genai.Client(api_key=api_key)

            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)

                try:
                    response = client.models.generate_images(
                        model="imagen-3.0-generate-001",
                        prompt=f"美容・コスメ広告用の高品質な正方形イラスト。余計な文字は不要。内容：{sentence}",
                        config=types.GenerateImagesConfig(number_of_images=1)
                    )

                    if response.generated_images:
                        for img in response.generated_images:
                            st.image(img.image.image_bytes, caption=f"シーン {index + 1}")

                except Exception as inner_e:
                    st.error(f"画像生成エラー：{inner_e}")

                st.markdown("---")

        except Exception as e:
            st.error(f"システム全体のエラー：{e}")
