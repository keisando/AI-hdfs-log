import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ファイルパス（必要なら変更してください）
file_path = 'anomaly_report.csv'

print("🔄 データを読み込んでいます... (重いので待ちます)")
# 全部読むと重いので、必要な列だけ読み込む工夫
df = pd.read_csv(file_path, usecols=['BlockId', 'EventId', 'Anomaly Score'])

print(f"✅ 読み込み完了: {len(df):,} 行")

# グラフのスタイル設定
sns.set(style="whitegrid")

# --- 1. 異常スコアのヒストグラム ---
plt.figure(figsize=(10, 6))
sns.histplot(df['Anomaly Score'], bins=30, kde=False, color='red')
plt.title('Distribution of Anomaly Scores (N=9.95M)', fontsize=16)
plt.xlabel('Anomaly Score', fontsize=12)
plt.ylabel('Count (Log Scale)', fontsize=12)
plt.yscale('log') # 数が多いので対数グラフにする
plt.tight_layout()
plt.savefig('graph1_score_distribution.png')
print("📸 graph1_score_distribution.png を保存しました")

# --- 2. 異常イベントのトップ10（棒グラフ） ---
plt.figure(figsize=(12, 8))
top_events = df['EventId'].value_counts().head(10)
sns.barplot(x=top_events.values, y=top_events.index, palette='viridis')
plt.title('Top 10 Anomaly Event Patterns', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Event Sequence', fontsize=12)
plt.tight_layout()
plt.savefig('graph2_top_events.png')
print("📸 graph2_top_events.png を保存しました")

# --- 3. 分析結果の要約テキスト出力 ---
with open('summary_report.txt', 'w') as f:
    f.write(f"Total Processed Anomalies: {len(df):,}\n")
    f.write(f"Most Frequent Pattern: {top_events.index[0]}\n")
    f.write(f"Count of Most Freq: {top_events.values[0]:,}\n")
    f.write(f"Percentage of Top 1: {top_events.values[0]/len(df)*100:.2f}%\n")

print("📄 summary_report.txt に要約を書き出しました")
print("🎉 完了！フォルダを確認してください")