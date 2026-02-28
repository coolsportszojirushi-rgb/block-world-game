import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="絵コンテ自動生成ツール", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")
st.write("台本を入力すると、Googleの最新AIがシーンごとのイメージイラストを自動生成します。")

google_api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。みずみずしいテクスチャーで、透明感のある肌へと導きます。"
script_text = st.text_area("台本を入力してください", value=default_script, height=150)

if st.button("イラストを生成する"):
    if not google_api_key:
        st.warning("左側のメニューからGoogle Gemini APIキーを入力してください。")
    elif not script_text:
        st.warning("台本が入力されていません。")
    else:
        st.info("AIがイラストを生成中です。少々お待ちください。")

        try:
            genai.configure(api_key=google_api_key)
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)

                # 画像生成処理
                result = genai.generate_images(
                    prompt=f"美容やスキンケアに関する高品質なイラスト。以下の文章の内容を分かりやすく表現してください：{sentence}",
                    number_of_images=1,
                    output_mime_type="image/jpeg"
                )

                for generated_image in result.images:
                    st.image(generated_image.image, caption=f"シーン {index + 1} の生成イメージ")

        except Exception as e:
            st.error("エラーが発生しました。APIキーの設定や、利用枠をご確認ください。")
