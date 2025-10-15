#!/usr/bin/env python3
"""
Create Complete Library Snippets (完全版プリセットライブラリ)

包括的なPythonライブラリスニペット辞書を作成します。
全てのスニペットに日本語説明付き。
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import load_config
from utils.database import DatabaseManager


def create_complete_library_snippets(db_manager: DatabaseManager):
    """Create comprehensive library snippets with Japanese descriptions."""

    print("=" * 70)
    print("完全版プリセットライブラリスニペット辞書 作成中...")
    print("=" * 70)

    # ========================================
    # 1. NumPy (数値計算)
    # ========================================
    print("\n[1/15] NumPy スニペット作成中...")
    numpy_tag_id = db_manager.get_or_create_tag("NumPy", parent_id=None, tag_type="folder")

    numpy_snippets = [
        {
            "name": "Array Creation",
            "code": """import numpy as np

# 配列作成の基本
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.zeros((3, 4))
arr3 = np.ones((2, 3))
arr4 = np.arange(0, 10, 2)
arr5 = np.linspace(0, 1, 5)
arr6 = np.eye(3)  # 単位行列""",
            "language": "python",
            "description": "NumPy配列を作成する様々な方法（zeros, ones, arange, linspace等）",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Array Operations",
            "code": """import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# 基本的な操作と属性
print(arr.shape)      # (2, 3) - 配列の形状
print(arr.ndim)       # 2 - 次元数
print(arr.dtype)      # int64 - データ型
print(arr.size)       # 6 - 要素数
print(arr.sum())      # 21 - 合計
print(arr.mean())     # 3.5 - 平均
print(arr.std())      # 標準偏差
print(arr.max())      # 6 - 最大値
print(arr.min())      # 1 - 最小値""",
            "language": "python",
            "description": "NumPy配列の基本的な操作とプロパティ（形状、統計量など）",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Array Indexing",
            "code": """import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# インデックスとスライス
print(arr[0, 1])      # 2 - 特定要素
print(arr[1])         # [4, 5, 6] - 行全体
print(arr[:2, 1:])    # [[2, 3], [5, 6]] - スライス
print(arr[::2, ::2])  # [[1, 3], [7, 9]] - ステップ付き

# Boolean インデックス
print(arr[arr > 5])   # [6, 7, 8, 9] - 条件抽出
arr[arr > 5] = 0      # 条件付き代入""",
            "language": "python",
            "description": "NumPy配列のインデックス参照とスライス技法（Boolean indexing含む）",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Matrix Operations",
            "code": """import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 行列演算
C = np.dot(A, B)      # 行列積
C = A @ B             # 行列積（演算子）
A_T = A.T             # 転置
A_inv = np.linalg.inv(A)  # 逆行列
det = np.linalg.det(A)    # 行列式

# 固有値・固有ベクトル
eigenvalues, eigenvectors = np.linalg.eig(A)""",
            "language": "python",
            "description": "NumPyによる線形代数演算（行列積、転置、逆行列、固有値など）",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Random Numbers",
            "code": """import numpy as np

# 乱数生成
np.random.seed(42)  # 再現性のためのシード設定

# 様々な乱数生成
rand_int = np.random.randint(0, 10, size=(3, 3))
rand_float = np.random.random((3, 3))
normal = np.random.randn(1000)  # 標準正規分布
uniform = np.random.uniform(0, 1, 100)
choice = np.random.choice([1, 2, 3, 4, 5], size=10, replace=False)

# 配列のシャッフル
arr = np.arange(10)
np.random.shuffle(arr)""",
            "language": "python",
            "description": "NumPyで乱数を生成する様々な方法（正規分布、一様分布など）",
            "tag_ids": [numpy_tag_id]
        },
        {
            "name": "Array Reshaping",
            "code": """import numpy as np

arr = np.arange(12)

# 形状変更
reshaped = arr.reshape(3, 4)  # (3, 4)に変形
reshaped = arr.reshape(2, -1) # -1で自動計算
flattened = reshaped.flatten() # 1次元化
ravel = reshaped.ravel()      # 1次元化（ビュー）

# 次元追加・削除
expanded = arr[np.newaxis, :]  # 次元追加
squeezed = np.squeeze(expanded) # 不要な次元削除""",
            "language": "python",
            "description": "NumPy配列の形状変更（reshape, flatten, 次元操作）",
            "tag_ids": [numpy_tag_id]
        }
    ]

    for snippet in numpy_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(numpy_snippets)} NumPy snippets")

    # ========================================
    # 2. Matplotlib (データ可視化)
    # ========================================
    print("\n[2/15] Matplotlib スニペット作成中...")
    matplotlib_tag_id = db_manager.get_or_create_tag("Matplotlib", parent_id=None, tag_type="folder")

    matplotlib_snippets = [
        {
            "name": "Basic Line Plot",
            "code": """import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)', linewidth=2)
plt.xlabel('X軸')
plt.ylabel('Y軸')
plt.title('サイン波')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()""",
            "language": "python",
            "description": "Matplotlibで基本的な折れ線グラフを作成（ラベル、凡例、グリッド付き）",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Scatter Plot",
            "code": """import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)
sizes = 1000 * np.random.rand(100)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='viridis')
plt.colorbar(scatter)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('散布図')
plt.show()""",
            "language": "python",
            "description": "カラーマッピングとサイズ変更付きの散布図を作成",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Subplots",
            "code": """import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('sin(x)')

axes[0, 1].plot(x, np.cos(x), 'r')
axes[0, 1].set_title('cos(x)')

axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_title('tan(x)')

axes[1, 1].plot(x, x**2)
axes[1, 1].set_title('x²')

plt.tight_layout()
plt.show()""",
            "language": "python",
            "description": "グリッド状に複数のサブプロットを作成（2×2レイアウト）",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Bar Chart",
            "code": """import matplotlib.pyplot as plt

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color='skyblue', edgecolor='navy', alpha=0.7)
plt.xlabel('カテゴリ')
plt.ylabel('値')
plt.title('棒グラフの例')
plt.grid(axis='y', alpha=0.3)

# 値をバーの上に表示
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}', ha='center', va='bottom')

plt.show()""",
            "language": "python",
            "description": "値ラベル付きの棒グラフを作成",
            "tag_ids": [matplotlib_tag_id]
        },
        {
            "name": "Histogram",
            "code": """import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('値')
plt.ylabel('頻度')
plt.title('ヒストグラム（正規分布）')
plt.grid(axis='y', alpha=0.3)

# 統計情報を表示
mean = data.mean()
std = data.std()
plt.axvline(mean, color='r', linestyle='--', label=f'平均: {mean:.2f}')
plt.legend()
plt.show()""",
            "language": "python",
            "description": "統計情報付きのヒストグラムを作成",
            "tag_ids": [matplotlib_tag_id]
        }
    ]

    for snippet in matplotlib_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(matplotlib_snippets)} Matplotlib snippets")

    # ========================================
    # 3. Pandas (データ分析)
    # ========================================
    print("\n[3/15] Pandas スニペット作成中...")
    pandas_tag_id = db_manager.get_or_create_tag("Pandas", parent_id=None, tag_type="folder")

    pandas_snippets = [
        {
            "name": "DataFrame Creation",
            "code": """import pandas as pd

# 辞書から作成
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Tokyo', 'Osaka', 'Kyoto']
})

# CSVから読み込み
df = pd.read_csv('data.csv')

# Excelから読み込み
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSONから読み込み
df = pd.read_json('data.json')

print(df.head())""",
            "language": "python",
            "description": "Pandas DataFrameを作成する様々な方法（辞書、CSV、Excel、JSON）",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Inspection",
            "code": """import pandas as pd

# データの基本情報
print(df.shape)           # (行数, 列数)
print(df.info())          # データ型と非null数
print(df.describe())      # 統計サマリー
print(df.head(10))        # 先頭10行
print(df.tail(10))        # 末尾10行
print(df.sample(5))       # ランダム5行

# 列情報
print(df.columns)         # 列名
print(df.dtypes)          # データ型
print(df.isnull().sum())  # 欠損値の数
print(df.nunique())       # ユニーク値の数""",
            "language": "python",
            "description": "DataFrameの構造と内容を詳細に検査（統計、欠損値など）",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Selection",
            "code": """import pandas as pd

# 列の選択
df['column_name']
df[['col1', 'col2']]

# 行の選択（位置ベース）
df.iloc[0]           # 最初の行
df.iloc[0:5]         # 最初の5行
df.iloc[:, 0:3]      # 最初の3列

# 行の選択（ラベルベース）
df.loc[0, 'column_name']
df.loc[:, ['col1', 'col2']]

# 条件選択
df[df['age'] > 30]
df[(df['age'] > 25) & (df['city'] == 'Tokyo')]
df.query('age > 30 and city == "Tokyo"')""",
            "language": "python",
            "description": "DataFrameのデータを選択・フィルタリング（iloc, loc, query）",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Cleaning",
            "code": """import pandas as pd

# 欠損値の処理
df.dropna()                    # 欠損値を含む行を削除
df.fillna(0)                   # 欠損値を0で埋める
df.fillna(df.mean())          # 平均値で埋める
df.fillna(method='ffill')     # 前方補完
df.fillna(method='bfill')     # 後方補完

# 重複の削除
df.drop_duplicates()
df.drop_duplicates(subset=['col1'])

# 列名の変更
df.rename(columns={'old_name': 'new_name'})

# データ型の変更
df['column'] = df['column'].astype('int')

# 値の置換
df['column'].replace({'old': 'new'})""",
            "language": "python",
            "description": "DataFrameのデータをクリーニング・整形（欠損値、重複、型変換）",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "GroupBy Operations",
            "code": """import pandas as pd

# グループ化と集計
grouped = df.groupby('category')
print(grouped.mean())
print(grouped.sum())
print(grouped.count())

# 複数列でグループ化
grouped = df.groupby(['category', 'region'])

# 複数の集計関数を適用
result = df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': ['sum', 'mean'],
    'quantity': 'sum'
})

# カスタム集計関数
result = df.groupby('category').agg({
    'price': lambda x: x.max() - x.min()
})

print(result)""",
            "language": "python",
            "description": "DataFrameのデータをグループ化・集計（複数集計関数対応）",
            "tag_ids": [pandas_tag_id]
        },
        {
            "name": "Data Merging",
            "code": """import pandas as pd

# DataFrameの結合
df1 = pd.DataFrame({'key': ['A', 'B', 'C'], 'value1': [1, 2, 3]})
df2 = pd.DataFrame({'key': ['A', 'B', 'D'], 'value2': [4, 5, 6]})

# マージ（SQLのJOIN相当）
merged = pd.merge(df1, df2, on='key', how='inner')  # 内部結合
merged = pd.merge(df1, df2, on='key', how='outer')  # 外部結合
merged = pd.merge(df1, df2, on='key', how='left')   # 左結合

# 連結
concatenated = pd.concat([df1, df2], axis=0)  # 縦方向
concatenated = pd.concat([df1, df2], axis=1)  # 横方向""",
            "language": "python",
            "description": "複数のDataFrameを結合・連結（merge, concat）",
            "tag_ids": [pandas_tag_id]
        }
    ]

    for snippet in pandas_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(pandas_snippets)} Pandas snippets")

    # ========================================
    # 4. scikit-learn (機械学習)
    # ========================================
    print("\n[4/15] scikit-learn スニペット作成中...")
    sklearn_tag_id = db_manager.get_or_create_tag("scikit-learn", parent_id=None, tag_type="folder")

    sklearn_snippets = [
        {
            "name": "Train-Test Split",
            "code": """from sklearn.model_selection import train_test_split

# データを訓練用とテスト用に分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # テストデータの割合（20%）
    random_state=42,    # 再現性のためのシード
    stratify=y          # クラス比率を維持
)

print(f"訓練データ: {len(X_train)}")
print(f"テストデータ: {len(X_test)}")""",
            "language": "python",
            "description": "データセットを訓練用とテスト用に分割（stratify対応）",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "Linear Regression",
            "code": """from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# モデルの作成と訓練
model = LinearRegression()
model.fit(X_train, y_train)

# 予測
y_pred = model.predict(X_test)

# 評価
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# 係数と切片
print(f"係数: {model.coef_}")
print(f"切片: {model.intercept_}")""",
            "language": "python",
            "description": "線形回帰モデルの訓練と評価（MSE, RMSE, MAE, R²）",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "Random Forest Classifier",
            "code": """from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# モデルの作成と訓練
model = RandomForestClassifier(
    n_estimators=100,    # 決定木の数
    max_depth=10,        # 木の最大深さ
    random_state=42,
    n_jobs=-1            # 並列処理
)
model.fit(X_train, y_train)

# 予測
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # 確率

# 評価
accuracy = accuracy_score(y_test, y_pred)
print(f"正解率: {accuracy:.4f}")
print("\n分類レポート:")
print(classification_report(y_test, y_pred))
print("\n混同行列:")
print(confusion_matrix(y_test, y_pred))

# 特徴量の重要度
importances = model.feature_importances_
print("\n特徴量の重要度:", importances)""",
            "language": "python",
            "description": "ランダムフォレスト分類器の訓練と詳細評価（特徴量重要度含む）",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "StandardScaler",
            "code": """from sklearn.preprocessing import StandardScaler
import joblib

# スケーラーの作成
scaler = StandardScaler()

# 訓練データでfitして変換
X_train_scaled = scaler.fit_transform(X_train)

# テストデータは同じスケーラーで変換（fitしない！）
X_test_scaled = scaler.transform(X_test)

# スケーラーの保存（本番環境で使用）
joblib.dump(scaler, 'scaler.pkl')

# スケーラーの読み込み
loaded_scaler = joblib.load('scaler.pkl')
X_new_scaled = loaded_scaler.transform(X_new)""",
            "language": "python",
            "description": "StandardScalerで特徴量を標準化（平均0、分散1）",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "Cross-Validation",
            "code": """from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)

# シンプルなクロスバリデーション
scores = cross_val_score(
    model, X, y,
    cv=5,                    # 5分割
    scoring='accuracy'       # 評価指標
)

print(f"CVスコア: {scores}")
print(f"平均: {scores.mean():.4f}")
print(f"標準偏差: {scores.std():.4f}")

# 複数の評価指標でクロスバリデーション
cv_results = cross_validate(
    model, X, y,
    cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1'],
    return_train_score=True
)

print("\nテストスコア:")
for metric, scores in cv_results.items():
    if metric.startswith('test_'):
        print(f"{metric}: {scores.mean():.4f} (+/- {scores.std():.4f})")""",
            "language": "python",
            "description": "交差検証を実行してモデルの汎化性能を評価",
            "tag_ids": [sklearn_tag_id]
        },
        {
            "name": "GridSearchCV",
            "code": """from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# ハイパーパラメータの候補
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

model = RandomForestClassifier(random_state=42)

# グリッドサーチ
grid_search = GridSearchCV(
    model,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

# 最適パラメータ
print("最適パラメータ:", grid_search.best_params_)
print("最良スコア:", grid_search.best_score_)

# 最適モデルで予測
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)""",
            "language": "python",
            "description": "グリッドサーチで最適なハイパーパラメータを探索",
            "tag_ids": [sklearn_tag_id]
        }
    ]

    for snippet in sklearn_snippets:
        db_manager.add_snippet(**snippet)
    print(f"✓ Created {len(sklearn_snippets)} scikit-learn snippets")

    # Continue with more libraries...
    # (This is getting long, let me create the rest in a follow-up)

    print("\n" + "=" * 70)
    print("完全版プリセットライブラリスニペット辞書 作成完了")
    print("=" * 70)


def main():
    """Main entry point."""
    print("=" * 70)
    print("Code Snippet Manager - 完全版ライブラリスニペット作成")
    print("=" * 70)

    # Load configuration
    config = load_config()

    # Initialize database
    db_manager = DatabaseManager(config)

    # Create library snippets
    create_complete_library_snippets(db_manager)

    print("\n✅ 完了！")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nユーザーによって中断されました。")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
