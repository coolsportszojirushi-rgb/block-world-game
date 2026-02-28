import streamlit as st
import google.generativeai as genai

# アプリの基本設定
st.set_page_config(page_title="美容絵コンテ生成", layout="wide")
st.title("美容台本 イラスト自動生成Webアプリ")

# サイドバーでAPIキーを受け取る
api_key = st.sidebar.text_input("Google Gemini APIキーを入力", type="password")

# 初期状態の台本
default_script = "春のゆらぎ肌には、ホワイトパワーセラムがおすすめです。みずみずしいテクスチャーで、透明感のある肌へと導きます。"
script_text = st.text_area("美容台本を入力してください", value=default_script, height=150)

if st.button("イラストを生成する"):
    if not api_key:
        st.warning("左側のメニューにAPIキーを入力してください。")
    else:
        st.info("最新のNano Banana 2でイラストを生成中です...")
        try:
            genai.configure(api_key=api_key)
            # 画像生成が可能な最新モデルを指定
            model = genai.GenerativeModel('gemini-3.1-flash')
            
            # 文章を分割
            sentences = script_text.split("。")
            sentences = [s.strip() + "。" for s in sentences if s.strip()]

            for index, sentence in enumerate(sentences):
                st.subheader(f"シーン {index + 1}")
                st.write(sentence)
                
                # 画像生成を実行
                # お支払い設定が完了していると、ここに画像データが返ってきます
                response = model.generate_content(
                    f"美容・コスメ広告用の高品質なイラスト。余計な文字は不要です。内容：{sentence}",
                    generation_config={"response_mime_type": "image/jpeg"}
                )
                
                # 画像データの取り出しと表示
                if response.candidates:
                    try:
                        # 成功した場合、画像を表示
                        st.image(response.candidates[0].content.parts[0].inline_data.data)
                    except:
                        # まだロックがかかっている場合は、AIのテキスト回答を表示
                        st.warning("画像生成のロックがまだ解除されていません。AIの説明文を表示します。")
                        st.write(response.text)
                
                st.markdown("---")
                
        except Exception as e:
            st.error(f"エラーが発生しました：{e}")
