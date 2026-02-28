import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")
script_text = st.text_area("美容台本を入力してください", "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。透明感のある肌へと導きます。", height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        st.info("最新のNano Banana 2でイラストを生成中。少々お待ちください。")
        try:
            genai.configure(api_key=api_key)
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                # 画像生成機能の有無をチェックして実行
                if hasattr(genai, 'ImageGenerationModel'):
                    model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                    response = model.generate_images(
                        prompt=f"美容広告用の高品質なイラスト。余計な文字は不要。内容：{sentence}",
                        number_of_images=1
                    )
                    if response.images:
                        st.image(response.images[0].image, caption=f"シーン {index + 1}")
                else:
                    st.error("エラー：サーバーの道具がまだ古いです。アプリの『Delete & Recreate』を試してください。")
                
                st.markdown("---")
        except Exception as e:
            st.error(f"詳細エラー：{e}")
