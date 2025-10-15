# CodeSnippetManager

プログラマー向け高機能コードスニペット管理アプリケーション

## 概要

CodeSnippetManagerは、Cliborのようなクリップボード管理の利便性に、プログラマー特化の機能を追加したアプリケーションです。複数の言語やライブラリの関数・コードを階層的に管理し、素早く検索・挿入できます。

## 現在の開発状況

**Phase 2.1 (基本GUI) 完了** - 2025-10-15

✅ **Phase 1 (基盤)** - 完了
- データベースモデル（Tag, Snippet, TagSnippet, Session, SearchIndex）
- 設定管理システム（Pydantic、型安全）
- マルチデータベースマネージャー（ローカル + 共有DB対応）
- 全テスト合格 (9/9)

✅ **Phase 2.1 (基本GUI)** - 完了
- ガジェット風メインウィンドウ（半透明、画面端固定）
- 階層タグツリー表示（アイコン・色対応）
- スニペットプレビュー機能
- 検索機能（インクリメンタル）
- クリップボードコピー

🚀 **次のステップ**: Phase 2.2 - ツリーウィジェット改善、Phase 3 - ホットキー・自動挿入

## 主な機能

- **階層的スニペット管理**: 言語 → ライブラリ → カテゴリで整理
- **高速検索**: インクリメンタルサーチ、あいまい検索
- **ホットキー起動**: `Ctrl+Shift+V` でクイックアクセス
- **自動挿入**: アクティブウィンドウに直接コードを挿入
- **シンタックスハイライト**: 見やすいコード表示
- **タグ管理**: 柔軟な分類とフィルタリング
- **使用統計**: よく使うスニペットを自動追跡

## インストール

### 必要要件

- Python 3.9+
- pip

### セットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd code-snippet-manager

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

## 使用方法

### GUIモード（推奨）

```bash
# 仮想環境を有効化
source venv/bin/activate  # Windows: venv\Scripts\activate

# GUIモードで起動
python gui_main.py
```

### CLIモード（テスト用）

```bash
# コマンドラインモードで起動（サンプルデータ投入・テスト）
python main.py
```

### GUI操作方法

1. **検索**: 検索ボックスにキーワードを入力
2. **選択**: タグまたはスニペットをクリック
3. **コピー**: スニペットをダブルクリック → クリップボードにコピー
4. **プレビュー**: 下部パネルでコードを確認

詳細は [GUI_GUIDE.md](GUI_GUIDE.md) を参照してください。

### スニペットの登録（Phase 2.3で実装予定）

1. 「+ New」ボタンをクリック
2. 言語、名前、コード、説明を入力
3. タグを選択
4. 「保存」をクリック

## プロジェクト構造

```
code-snippet-manager/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py      # データベース接続
│   │   └── snippet.py       # スニペットモデル
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py   # メインウィンドウ
│   │   └── quick_access.py  # クイックアクセスウィンドウ
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── snippet_controller.py  # スニペット管理
│   │   └── search_controller.py   # 検索機能
│   └── utils/
│       ├── __init__.py
│       ├── hotkey.py        # ホットキー管理
│       ├── clipboard.py     # クリップボード操作
│       └── auto_insert.py   # 自動挿入
├── data/
│   └── snippets.db          # SQLiteデータベース
├── config/
│   └── settings.json        # 設定ファイル
├── main.py                  # エントリーポイント
├── requirements.txt         # 依存パッケージ
├── REQUIREMENTS.md          # 要件定義書
└── README.md                # このファイル
```

## 設定

`config/settings.json` で設定をカスタマイズできます：

```json
{
  "hotkey": "ctrl+shift+v",
  "theme": "dark",
  "auto_insert": true,
  "database_path": "./data/snippets.db"
}
```

## 開発ロードマップ

### Phase 1: 基盤（完了）
- [x] 要件定義・詳細設計
- [x] データベースモデル設計・実装
- [x] 設定管理システム（Pydantic）
- [x] マルチDB対応（ローカル + 共有）
- [x] 基本構造セットアップ

### Phase 2: GUI開発（次のステップ）
- [ ] ガジェット風メインウィンドウ
- [ ] 階層タグツリービュー
- [ ] スニペット詳細表示
- [ ] 基本的なCRUD操作

### Phase 3: コア機能
- [ ] ホットキー機能（Ctrlダブルタップ）
- [ ] 自動挿入機能
- [ ] インクリメンタルサーチ
- [ ] シンタックスハイライト
- [ ] 透明度アニメーション

### Phase 4: 拡張機能
- [ ] インポート/エクスポート
- [ ] お気に入り機能
- [ ] 使用統計
- [ ] ダークモード

### Phase 5: 配布・デプロイ
- [ ] Windows EXE化（PyInstaller）
- [ ] インストーラー作成（Inno Setup）
- [ ] 本部配信システム
- [ ] ドキュメント整備

## 技術スタック

- **言語**: Python 3.9+
- **GUI**: tkinter / PyQt6
- **データベース**: SQLite3 + SQLAlchemy
- **ホットキー**: keyboard / pynput
- **クリップボード**: pyperclip
- **シンタックスハイライト**: Pygments

## サンプルスニペット

アプリケーションには以下のサンプルスニペットが含まれています：

### Python - NumPy
```python
import numpy as np
arr = np.array([1, 2, 3])
```

### Python - Pandas
```python
import pandas as pd
df = pd.read_csv('data.csv')
```

### JavaScript - React
```javascript
const [state, setState] = useState(initialValue);
```

## トラブルシューティング

### ホットキーが動作しない

管理者権限で実行してください：

```bash
# Windows
右クリック → 「管理者として実行」

# macOS/Linux
sudo python main.py
```

### データベースエラー

データベースをリセット：

```bash
rm data/snippets.db
python main.py
```

## 貢献

プルリクエストを歓迎します！

1. Fork する
2. Feature ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. Commit する (`git commit -m 'Add amazing feature'`)
4. Push する (`git push origin feature/amazing-feature`)
5. Pull Request を作成

## ライセンス

MIT License

## 作成者

Sekine53629

## 謝辞

- Clibor - インスピレーション元
- SnippetsLab - UI/UXの参考

---

**作成日**: 2025-10-15
