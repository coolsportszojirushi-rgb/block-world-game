import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

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
        st.warning("左側のメニューにAPIキーを入力してください。")
    else:
        st.info("最新のNano Banana 2 (Imagen 3) を呼び出し中です...")
        try:
            genai.configure(api_key=api_key)
            
            # 文章を1文ずつに分ける
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                # 画像生成を実行する最新かつ最も安定した記述
                # 注意：お支払い設定（本人確認）が完了している必要があります
                model = genai.GenerativeModel('gemini-1.5-flash') # 構造解析用
                
                # 画像生成専用のプロンプトを作成
                prompt = f"美容・コスメ広告用の高品質な正方形イラスト。余計な文字は不要。内容：{sentence}"
                
                # 画像生成モデル（Imagen 3）を直接指定して呼び出し
                imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")
                response = imagen.generate_images(
                    prompt=prompt,
                    number_of_images=1
                )
                
                # 生成された画像を表示
                if response.images:
                    st.image(response.images[0].image, caption=f"シーン {index + 1} の生成イメージ")
                
                st.markdown("---")
                
        except Exception as e:
            # エラーの詳細を分かりやすく表示
            if "ImageGenerationModel" in str(e):
                st.error("システム準備中です。requirements.txtの更新が反映されるまで1分ほどお待ちください。")
            elif "403" in str(e) or "permission" in str(e).lower():
                st.error("Google AI Studioでの『お支払い情報（本人確認）』の設定が完了していない可能性があります。設定をご確認ください。")
            else:
                st.error(f"詳細エラー：{e}")
