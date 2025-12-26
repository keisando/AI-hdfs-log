import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import gc
import re

# --- 設定 ---
MODEL_PATH = 'models/lstm_model.h5'
CHUNK_SIZE = 50000   # 5万行ずつ高速処理
MICRO_BATCH = 256    # 計算バッチサイズ
MAX_SEQ_LEN = 20

st.set_page_config(page_title="HDFS 10M Analysis", layout="wide")
st.title("🛡️ HDFS 10M Log Analysis (Final Production)")

# --- モデルロード ---
@st.cache_resource
def load_ai_model():
    with tf.device('/CPU:0'):
        return load_model(MODEL_PATH)

try:
    model = load_ai_model()
    st.sidebar.success("✅ Model Loaded (16GB RAM)")
except Exception as e:
    st.error(f"Model Error: {e}")
    st.stop()

threshold = st.sidebar.slider("Anomaly Threshold", 0.0, 5.0, 0.35)

# --- 翻訳機能（ここが修正ポイント！） ---
def preprocess_events_robust(event_series):
    """
    "E5 E22" (文字) が来ても [5, 22] (数字) に強制変換する。
    データの形式が少し違ってもエラーを出さない。
    """
    processed_seqs = []
    for item in event_series:
        tokens = []
        # 文字列でもリストでも対応できるように統一
        if isinstance(item, str):
            item_list = [item]
        elif isinstance(item, list) or isinstance(item, np.ndarray):
            item_list = item
        else:
            item_list = [str(item)]

        for sub_item in item_list:
            # カンマやスペースで分解
            parts = str(sub_item).replace(',', ' ').split()
            for p in parts:
                # 数字だけ抜き出す (E5 -> 5)
                clean_t = re.sub(r'[^0-9]', '', p)
                if clean_t.isdigit():
                    tokens.append(int(clean_t))
        
        # 万が一空っぽなら0を入れる
        if not tokens: tokens = [0]
        processed_seqs.append(tokens)
    return processed_seqs

# --- 高速計算関数 ---
def calculate_anomaly_score_fast(model, X_data):
    scores = []
    dataset = tf.data.Dataset.from_tensor_slices(X_data).batch(MICRO_BATCH)
    scce = tf.keras.losses.SparseCategoricalCrossentropy(reduction=tf.keras.losses.Reduction.NONE)
    for batch in dataset:
        preds = model(batch, training=False)
        loss = scce(batch, preds)
        scores.extend(np.mean(loss.numpy(), axis=1))
        del preds, loss
    gc.collect()
    return np.array(scores)

# --- メイン処理 ---
st.info("💡 1000万行対応済み (Max 2GB Upload)")
uploaded_file = st.file_uploader("Upload CSV (BlockId, EventId)", type=['csv'])

if uploaded_file is not None:
    if st.button("🚀 Start 10M Analysis"):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        anomalies_only = []
        total_processed = 0
        
        # チャンク読み込み
        chunk_iter = pd.read_csv(uploaded_file, chunksize=CHUNK_SIZE)
        
        for i, df_chunk in enumerate(chunk_iter):
            status_text.text(f"Processing... {total_processed:,} lines done.")
            
            try:
                # 列チェック
                if 'EventId' not in df_chunk.columns:
                    st.error("CSVに 'EventId' 列がありません！変換スクリプトで作ったCSVを使ってください。")
                    st.stop()

                # ★翻訳実行
                sequences = preprocess_events_robust(df_chunk['EventId'])
                
                # AI用データ作成
                X = pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post', truncating='post')
                
                # 推論
                scores = calculate_anomaly_score_fast(model, X)
                
                df_chunk['Anomaly Score'] = scores
                df_chunk['Prediction'] = df_chunk['Anomaly Score'].apply(lambda x: 'Anomaly' if x > threshold else 'Normal')
                
                # 異常だけ保存
                anomaly_df = df_chunk[df_chunk['Prediction'] == 'Anomaly']
                if not anomaly_df.empty:
                    anomalies_only.append(anomaly_df)
                
                total_processed += len(df_chunk)
                del X, sequences, scores
                gc.collect()

            except Exception as e:
                st.warning(f"Chunk {i} warning: {e}")
                continue

            # プログレスバー
            progress = min((i + 1) / 200.0, 1.0)
            progress_bar.progress(progress)

        # --- 完了後 ---
        progress_bar.progress(1.0)
        status_text.success(f"✅ Analysis Complete! Processed {total_processed:,} lines.")
        
        if anomalies_only:
            final_df = pd.concat(anomalies_only)
            # 上位50件だけ表示
            st.dataframe(final_df.sort_values('Anomaly Score', ascending=False).head(50))
            # 全件ダウンロード
            csv = final_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Report", csv, "anomaly_report.csv", "text/csv")
        else:
            st.success("🎉 No anomalies found in this dataset.")