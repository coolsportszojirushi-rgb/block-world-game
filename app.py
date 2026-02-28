import streamlit as st
from google import genai
from PIL import Image
import io

st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")
script_text = st.text_area("美容台本を入力してください", "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。透明感のある肌へと導きます。", height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        st.info("最新のImagen 3でイラストを生成中。少々お待ちください。")
        try:
            # 完全に新しい「google-genai」の呼び出し方
            client = genai.Client(api_key=api_key)
            
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                # 空の行を無視する
                if len(sentence) <= 1:
                    continue
                    
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                # 画像生成（新しい専用の関数を使用）
                result = client.models.generate_images(
                    model='imagen-3.0-generate-001',
                    prompt=f"美容広告用の高品質なイラスト。余計な文字は不要。内容：{sentence}",
                    config=dict(number_of_images=1)
                )
                
                # 画像データを復元して画面に表示
                for generated_image in result.generated_images:
                    image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                    st.image(image, caption=f"シーン {index + 1}")
                
                st.markdown("---")
        except Exception as e:
            st.error(f"詳細エラー：{e}")
