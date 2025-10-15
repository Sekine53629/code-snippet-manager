# GUI使用ガイド

**Phase 2: 基本GUI実装完了** - 2025-10-15

## 起動方法

### 1. 初回セットアップ

```bash
# 仮想環境の作成とパッケージインストール（初回のみ）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. サンプルデータの準備（初回のみ）

```bash
# サンプルデータを投入
python main.py
```

### 3. GUIアプリケーションの起動

```bash
# 仮想環境を有効化
source venv/bin/activate  # Windows: venv\Scripts\activate

# GUIモードで起動
python gui_main.py
```

---

## 機能説明

### 📁 階層ツリー表示

- **タグの階層構造**を左側のツリービューに表示
- **アイコンと色**でカテゴリを視覚的に識別
- クリックでタグ選択、スニペットのプレビュー表示

### 🔍 検索機能

- 検索ボックスにキーワードを入力
- スニペット名・説明でリアルタイム検索
- 検索結果件数をステータスバーに表示

### 📋 スニペットのコピー

- **シングルクリック**: プレビュー表示
- **ダブルクリック**: クリップボードにコピー
- ステータスバーに「✓ Copied to clipboard!」と表示

### 🎨 UI/UX特徴

#### ガジェット風デザイン
- **半透明背景** (opacity: 0.95)
- **ダークテーマ** (#1E1E1E ベース)
- **画面端固定** (デフォルト: 右端)
- **フレームレス** (タイトルバーなし)

#### 配置設定
設定ファイルで左右の配置を変更可能：

```json
{
  "appearance": {
    "position": "right",  // "right" または "left"
    "offset_x": 10,
    "opacity_active": 0.95,
    "opacity_inactive": 0.3
  }
}
```

### 🎮 操作方法

| 操作 | 機能 |
|------|------|
| タグをクリック | スニペットをプレビュー表示 |
| タグをダブルクリック | スニペットをクリップボードにコピー |
| 検索ボックスに入力 | インクリメンタルサーチ |
| `—` ボタン | ウィンドウを最小化（未実装） |
| `×` ボタン | アプリケーションを終了 |

---

## 実装済み機能 (Phase 2.1)

### ✅ GadgetWindow

- [x] 半透明ウィンドウ
- [x] 画面端固定配置（右/左選択可能）
- [x] フレームレスデザイン
- [x] 常に最前面表示
- [x] フェードイン・アウトアニメーション
- [x] カスタムヘッダー（タイトル + 最小化/閉じるボタン）

### ✅ TreeWidget

- [x] 階層タグの表示
- [x] アイコン・色の表示
- [x] 親子関係の可視化
- [x] 全展開表示
- [x] アイテム選択時のプレビュー

### ✅ 検索機能

- [x] 検索入力フィールド
- [x] リアルタイム検索（textChanged）
- [x] 結果件数表示

### ✅ プレビューパネル

- [x] コード表示エリア
- [x] モノスペースフォント
- [x] 読み取り専用モード
- [x] ダークテーマ対応

### ✅ クリップボード連携

- [x] ダブルクリックでコピー
- [x] ステータス表示

---

## 未実装機能 (Phase 2.2以降)

### ⏳ アニメーション

- [ ] ウィンドウの展開・最小化アニメーション
- [ ] スムーズな透明度変化
- [ ] イージング関数の適用

### ⏳ スニペット管理

- [ ] 新規作成ダイアログ
- [ ] 編集機能
- [ ] 削除機能
- [ ] タグの作成・編集

### ⏳ 高度な検索

- [ ] あいまい検索（Fuzzy）
- [ ] 言語フィルター
- [ ] タグフィルター

### ⏳ ホットキー

- [ ] Ctrlダブルタップで起動
- [ ] カスタムホットキー設定

### ⏳ セッション記憶

- [ ] 最後に選択していたタグを記憶
- [ ] 展開状態の保存
- [ ] ウィンドウサイズ・位置の保存

---

## トラブルシューティング

### GUIが起動しない

**エラー**: `ModuleNotFoundError: No module named 'PyQt6'`

**解決方法**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### データが表示されない

**エラー**: `⚠️  No data found`

**解決方法**:
```bash
# サンプルデータを投入
python main.py
```

### ウィンドウが画面外に表示される

**解決方法**:
設定ファイル（`~/.config/CodeSnippetManager/config.json`）を削除して再起動

```bash
rm ~/.config/CodeSnippetManager/config.json
python gui_main.py
```

---

## 技術仕様

### アーキテクチャ

```
gui_main.py
    ↓
GadgetWindow (QMainWindow)
    ├── Header (タイトル + コントロールボタン)
    ├── SearchBar (QLineEdit)
    ├── ContentArea (QSplitter)
    │   ├── TreeWidget (QTreeWidget) - タグ階層
    │   └── PreviewPanel (QTextEdit) - コードプレビュー
    └── Footer (ステータス + アクションボタン)
```

### データフロー

```
DatabaseManager
    ↓ get_all_tags()
GadgetWindow._load_data()
    ↓ _build_tree()
QTreeWidget
    ↓ itemClicked
_on_item_clicked()
    ↓ get_snippets_by_tag()
PreviewPanel (コード表示)
```

### スタイリング

- **Qt Style Sheets** によるカスタムスタイル
- **カラースキーム**: Material Design ダークテーマ
  - Background: `#1E1E1E`
  - Text: `#FFFFFF`
  - Accent: `#64B5F6` (Blue)
  - Borders: `#444444`

---

## 次のステップ

### Phase 2.2 - ツリーウィジェット改善

1. **ツリーアイテムの詳細化**
   - スニペット数の表示
   - 最終更新日時の表示
   - 使用頻度のバッジ

2. **ドラッグ&ドロップ**
   - タグの移動
   - 階層の再編成

### Phase 2.3 - ダイアログ実装

1. **新規スニペットダイアログ**
   - 名前、言語、コード、説明入力
   - タグ選択
   - シンタックスハイライト付きエディタ

2. **タグ管理ダイアログ**
   - タグの作成・編集・削除
   - アイコン・色の選択

### Phase 3 - コア機能

1. **ホットキーシステム**
   - グローバルホットキー登録
   - Ctrlダブルタップ検出

2. **自動挿入機能**
   - アクティブウィンドウへのコード挿入
   - プレースホルダー置換

---

**作成日**: 2025-10-15
**バージョン**: Phase 2.1
**担当**: Claude (Anthropic)
