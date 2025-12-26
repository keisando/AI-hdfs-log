import pandas as pd
import matplotlib.pyplot as plt

# ファイル名（もし違う場所に置いてあるならパスを変更してください）
file_path = 'anomaly_report.csv'

print("🔄 データを読み込んでいます... (700MBなので数秒かかります)")

# CSVを読み込む
df = pd.read_csv(file_path)

# --- 1. 基本データの表示 ---
total_anomalies = len(df)
print("-" * 30)
print(f"✅ 読み込み完了！")
print(f"📊 異常検知された総行数: {total_anomalies:,} 行")
print("-" * 30)

# --- 2. 異常スコアの統計 ---
print("📈 異常スコアの統計情報:")
print(df['Anomaly Score'].describe())

# --- 3. スコアのヒストグラムを作成（画像保存） ---
plt.figure(figsize=(10, 6))
plt.hist(df['Anomaly Score'], bins=50, color='salmon', edgecolor='black')
plt.title('Distribution of Anomaly Scores (10M Log Analysis)', fontsize=16)
plt.xlabel('Anomaly Score', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.grid(axis='y', alpha=0.75)
plt.savefig('anomaly_distribution.png') # 画像として保存
print(f"\n🖼️ 分布図を 'anomaly_distribution.png' に保存しました。")

# --- 4. 最も危険な異常トップ10を表示 ---
print("\n🔥 スコアが高い危険な異常トップ10:")
top_10 = df.sort_values(by='Anomaly Score', ascending=False).head(10)
print(top_10[['BlockId', 'Anomaly Score', 'EventId']])

# --- 5. 異常の種類（イベントパターン）ランキング ---
print("\n🏆 よくある異常パターン（EventId）トップ5:")
print(df['EventId'].value_counts().head(5))

print("-" * 30)
print("🎉 分析終了！")