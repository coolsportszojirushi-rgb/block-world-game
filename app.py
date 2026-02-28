import streamlit as st
import google.generativeai as genai

# アプリの基本設定
st.set_page_config(page_title="美容絵コンテ自動生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

# サイドバー設定
api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

# 春のホワイトパワーセラム向けの初期台本
default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。みずみずしいテクスチャーで、透明感のある肌へと導きます。"
script_text = st.text_area("美容台本を入力してください", value=default_script, height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("APIキーを入力してください。")
    else:
        st.info("Nano Banana 2（最新の画像生成AI）を呼び出し中です...")
        try:
            genai.configure(api_key=api_key)
            
            # 1. 文章を1文ずつに分ける
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                # 2. 画像生成モデル（ナノバナナ2の実体であるImagen）を呼び出す
                # ※APIキーにお支払い情報が設定されている必要があります
                model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                
                # 3. 画像生成を実行
                response = model.generate_images(
                    prompt=f"美容・コスメ広告用の高品質な正方形イラスト。余計な文字は不要。内容：{sentence}",
                    number_of_images=1
                )
                
                # 4. 生成された画像を表示
                if response.images:
                    st.image(response.images[0].image, caption=f"シーン {index + 1} の生成イメージ")
                
                st.markdown("---")
                
        except Exception as e:
            # エラーの詳細を表示（お支払い情報未設定の場合はここで通知されます）
            st.error(f"エラーが発生しました。Google AI Studioで『お支払い情報（本人確認）』の設定が完了しているかご確認ください。\n\n詳細：{e}")
