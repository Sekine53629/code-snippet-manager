# Code Snippet Manager

プログラマー向け高機能コードスニペット管理アプリケーション

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/PyQt6-6.0+-green.svg" alt="PyQt6">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License MIT">
</p>

## 概要

Code Snippet Managerは、Cliborのようなクリップボード管理の利便性に、プログラマー特化の機能を追加したデスクトップアプリケーションです。複数の言語やライブラリのコードを階層的に管理し、素早く検索・挿入できます。

### 主な特徴

- 🎯 **ホットキー起動**: Ctrlキー2回連続押しで即座にアクセス
- 🌲 **階層的管理**: タグで柔軟に分類・整理
- 🔍 **ファジー検索**: タイポも考慮した賢い検索
- 🎨 **シンタックスハイライト**: 48種類のテーマで見やすく表示
- 📊 **使用統計**: よく使うスニペットを自動追跡
- 💾 **インポート/エクスポート**: JSON・Markdown形式でデータ管理
- ⭐ **お気に入り**: 頻繁に使うスニペットに素早くアクセス

---

## 開発状況

**Phase 7 (統合とテスト) 完了** - 2025-10-15

✅ **全Phase完了**: Phase 1-7 すべての機能実装完了
🎉 **統合テスト**: 6/6 テスト合格
📦 **配布準備中**: Phase 8 (ドキュメント・配布) 作業中

### 完了したフェーズ

<details>
<summary><b>✅ Phase 1: 基盤構築</b></summary>

- データベースモデル（Tag, Snippet, TagSnippet, Session, SearchIndex）
- 設定管理システム（Pydantic、型安全）
- マルチデータベースマネージャー（ローカル + 共有DB対応）
- CRUD操作（Create, Read）
- 全テスト合格 (9/9)

</details>

<details>
<summary><b>✅ Phase 2: 基本UI</b></summary>

**Phase 2.1: ガジェットウィンドウ**
- 半透明ガジェット風メインウィンドウ
- 階層タグツリー表示（アイコン・色対応）
- スニペットプレビュー機能
- インクリメンタル検索
- クリップボードコピー

**Phase 2.2: ツリー改善**
- スニペットカウント表示
- ツリー内スニペット表示
- コンテキストメニュー（右クリック）
- 使用回数トラッキング
- 全テスト合格 (8/8)

**Phase 2.3: ダイアログ実装**
- スニペット作成・編集・削除ダイアログ
- マルチタグ選択
- 入力バリデーション
- 全テスト合格 (5/5)

</details>

<details>
<summary><b>✅ Phase 3: コア機能</b></summary>

- あいまい検索（Fuzzy Search）- typo tolerant
- クリップボード操作ユーティリティ
- 自動挿入機能（アクティブウィンドウ検出）
- クロスプラットフォーム対応
- 全テスト合格 (6/6)

</details>

<details>
<summary><b>✅ Phase 4: 高度な機能</b></summary>

- ホットキーシステム（Ctrlダブルタップ検出）
- アニメーションコントローラー
  - フェードイン/アウト
  - 展開・縮小
  - エッジドッキング
- 全テスト合格 (6/6)

</details>

<details>
<summary><b>✅ Phase 5: UI/UX改善</b></summary>

- シンタックスハイライト（Pygments統合、48スタイル）
- Qt統合ハイライター（リアルタイム）
- 設定ダイアログ（外観・動作・データベース）
- ダーク/ライトテーマ対応
- 全テスト合格 (5/5)

</details>

<details>
<summary><b>✅ Phase 6: 拡張機能</b></summary>

- インポート/エクスポート（JSON, Markdown）
- バックアップ/リストア機能
- 統計ダイアログ（使用状況の可視化）
- お気に入りスニペット機能
- 全テスト合格 (5/5)

</details>

<details>
<summary><b>✅ Phase 7: 統合とテスト</b></summary>

- メインアプリケーションエントリーポイント
- 全コンポーネント統合
- ホットキー連携
- テーマシステム
- 統合テストスクリプト
- 全テスト合格 (6/6)

</details>

🚀 **次のステップ**: Phase 8 - ドキュメント・配布

---

## インストール

### 必要要件

- Python 3.9以上
- pip

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/Sekine53629/code-snippet-manager.git
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

---

## 使い方

### 起動方法

```bash
# 仮想環境を有効化
source venv/bin/activate  # Windows: venv\Scripts\activate

# アプリケーションを起動
python main.py
```

### 基本操作

1. **ホットキーで表示**: Ctrlキーを素早く2回連続押し
2. **検索**: 検索ボックスにキーワードを入力
3. **選択**: タグまたはスニペットをクリック
4. **プレビュー**: 下部パネルでコードを確認（シンタックスハイライト付き）
5. **コピー**: スニペットをダブルクリックでクリップボードにコピー

### スニペット管理

**新規作成**:
1. 「+ New」ボタンをクリック
2. 言語、名前、コード、説明を入力
3. タグを選択（複数可）
4. 「Save」をクリック

**編集・削除**:
1. スニペットを右クリック
2. 「Edit」で編集、「Delete」で削除

**お気に入り**:
1. スニペットを右クリック
2. 「Add to Favorites」を選択

### データ管理

**エクスポート（別環境へのデータ移行）**:
```bash
# 現在のスニペットを全てJSONにエクスポート
python export_snippets.py

# カスタムファイル名を指定
python export_snippets.py my_snippets.json
```

出力ファイル: `library_snippets.json` (デフォルト) または指定したファイル名
- タグとスニペットの全データを含む
- 29個のライブラリスニペット (NumPy, Matplotlib, Pandas, scikit-learn, TensorFlow/Keras, Django)
- 日本語の説明文付き

**インポート（別環境でデータを復元）**:
```bash
# JSONファイルからインポート（既存データを置き換え）
python import_snippets.py library_snippets.json

# マージモード（既存データを保持）
python import_snippets.py library_snippets.json --merge
```

**バックアップ**:
- 自動バックアップ: `backups/` ディレクトリに保存
- 手動バックアップ: 設定 → Create Backup

---

## プロジェクト構造

```
code-snippet-manager/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # データベースモデル
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py           # 設定管理
│   │   ├── database.py         # データベースマネージャー
│   │   ├── fuzzy_search.py     # あいまい検索
│   │   ├── clipboard.py        # クリップボード操作
│   │   ├── auto_insert.py      # 自動挿入
│   │   ├── syntax_highlighter.py  # シンタックスハイライト
│   │   └── import_export.py    # インポート/エクスポート
│   ├── views/
│   │   ├── __init__.py
│   │   ├── gadget_window.py    # メインウィンドウ
│   │   ├── snippet_dialog.py   # スニペットダイアログ
│   │   ├── settings_dialog.py  # 設定ダイアログ
│   │   ├── statistics_dialog.py  # 統計ダイアログ
│   │   └── code_highlighter.py   # Qtハイライター
│   └── controllers/
│       ├── __init__.py
│       ├── hotkey_controller.py    # ホットキー管理
│       └── animation_controller.py  # アニメーション
├── data/
│   └── snippets.db             # SQLiteデータベース
├── config/
│   └── config.json             # 設定ファイル
├── main.py                     # メインエントリーポイント
├── test_integration.py         # 統合テスト
├── requirements.txt            # 依存パッケージ
├── REQUIREMENTS.md             # 要件定義書
├── TECHNICAL_DESIGN.md         # 技術設計書
├── IMPLEMENTATION_ROADMAP.md   # 実装ロードマップ
└── README.md                   # このファイル
```

---

## 設定

設定ファイル: `config/config.json`

### 外観設定

```json
{
  "appearance": {
    "theme": "dark",           // "dark" または "light"
    "position": "right",       // "left", "right", "top", "bottom"
    "opacity_active": 0.95,    // アクティブ時の透明度 (0.0-1.0)
    "width_max": 400,          // 最大幅
    "height_max": 600          // 最大高さ
  }
}
```

### 動作設定

```json
{
  "behavior": {
    "hotkey_enabled": true,         // ホットキー有効化
    "auto_insert": false,           // 自動挿入
    "auto_minimize": true,          // 自動最小化
    "confirm_delete": true,         // 削除確認
    "double_click_action": "copy"   // ダブルクリック動作
  }
}
```

### データベース設定

```json
{
  "database": {
    "mode": "local",                      // "local" または "shared"
    "local": {
      "path": "~/snippets/local.db"
    },
    "shared": {
      "enabled": false,
      "path": "~/shared/snippets.db"
    }
  }
}
```

---

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| **言語** | Python 3.9+ |
| **GUI** | PyQt6 |
| **データベース** | SQLite3 + SQLAlchemy |
| **設定管理** | Pydantic |
| **クリップボード** | pyperclip |
| **シンタックスハイライト** | Pygments |
| **あいまい検索** | difflib + fuzzywuzzy |
| **ビルド** | PyInstaller |

---

## テスト

### 統合テスト実行

```bash
python test_integration.py
```

### テストカバレッジ

- **Configuration**: ✅
- **Database Operations**: ✅
- **Fuzzy Search**: ✅
- **Import/Export**: ✅
- **Syntax Highlighter**: ✅
- **Favorite Snippets**: ✅

**結果**: 6/6 テスト合格 (100%)

---

## トラブルシューティング

### ホットキーが動作しない

**原因**: アクセシビリティ権限が必要な場合があります

**解決策**:
- macOS: システム環境設定 → セキュリティとプライバシー → プライバシー → アクセシビリティ
- Windows: 管理者として実行

### データベースエラー

**原因**: データベースファイルが破損している可能性があります

**解決策**:
```bash
# データベースをリセット
rm data/snippets.db
python main.py
```

### インポートエラー

**原因**: モジュールパスの問題

**解決策**:
```bash
# 仮想環境を再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 開発

### 開発環境のセットアップ

```bash
# 開発用依存関係をインストール
pip install -r requirements-dev.txt

# テストを実行
pytest

# コードフォーマット
black src/
```

### ブランチ戦略

- `main`: 安定版
- `develop`: 開発版
- `feature/*`: 機能開発
- `hotfix/*`: 緊急修正

---

## 貢献

プルリクエストを歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

---

## 作成者

**Sekine53629**
- GitHub: [@Sekine53629](https://github.com/Sekine53629)

---

## 謝辞

- **Clibor** - インスピレーション元
- **SnippetsLab** - UI/UXの参考
- **VS Code** - テーマデザインの参考

---

## サポート

問題や質問がある場合:
- [Issue Tracker](https://github.com/Sekine53629/code-snippet-manager/issues) で報告
- [Discussions](https://github.com/Sekine53629/code-snippet-manager/discussions) で質問

---

**最終更新日**: 2025-10-15
**バージョン**: 1.0.0
**ステータス**: Phase 7 完了、Phase 8 進行中
