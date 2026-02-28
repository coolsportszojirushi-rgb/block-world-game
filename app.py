import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import base64

# 基本設定
st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

# サイドバー設定
api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。みずみずしいテクスチャーで、透明感のある肌へと導きます。"
script_text = st.text_area("美容台本を入力してください", value=default_script, height=150)

# 参考イラストの読み込み
reference_image = st.file_uploader("参考イラストをアップロード（任意）", type=["png", "jpg", "jpeg"])

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        st.info("Gemini でイラストを生成中...")
        try:
            client = genai.Client(api_key=api_key)

            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)

                try:
                    prompt = f"""
Create a high quality square beauty cosmetics advertisement illustration in the following style:
- Soft, clean Japanese illustration style (like fashion magazine or cosmetics brand illustration)
- Simple line art with light, delicate coloring
- A beautiful Japanese woman naturally depicted in a scene matching the content
- Elegant and minimal composition
- No text, no letters, no words anywhere in the image
- Pastel and soft color palette
- The woman should look natural, graceful, and match the mood of the scene

Scene content: {sentence}

Draw the woman interacting with or expressing the mood of this beauty scene.
"""

                    contents = [prompt]

                    # 参考イラストがある場合は追加
                    if reference_image is not None:
                        image_bytes = reference_image.read()
                        reference_image.seek(0)
                        contents = [
                            {
                                "parts": [
                                    {"text": prompt},
                                    {
                                        "inline_data": {
                                            "mime_type": reference_image.type,
                                            "data": base64.b64encode(image_bytes).decode("utf-8")
                                        }
                                    }
                                ]
                            }
                        ]

                    response = client.models.generate_content(
                        model="gemini-2.0-flash-exp-image-generation",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            response_modalities=["IMAGE", "TEXT"]
                        )
                    )

                    for part in response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            image = Image.open(io.BytesIO(part.inline_data.data))
                            st.image(image, caption=f"シーン {index + 1}")

                except Exception as inner_e:
                    st.error(f"画像生成エラー：{inner_e}")

                st.markdown("---")

        except Exception as e:
            st.error(f"システム全体のエラー：{e}")
