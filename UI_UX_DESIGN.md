# UI/UX 設計書（改訂版）

## コンセプト

**「必要な時だけ、美しく、スムーズに」**

- 半透明のガジェット風UI
- 画面右端に固定配置
- スムーズなアニメーション
- 前回の階層を記憶
- 無限に入れ子可能な階層タグシステム

---

## 1. 階層タグシステム

### 1.1 柔軟な階層構造

従来の「言語→ライブラリ→カテゴリ」という固定階層ではなく、**ユーザーが自由に階層を定義**できるシステム。

#### 構造例

```
タグ階層の例1（言語ベース）:
Python
  └─ データサイエンス
      ├─ NumPy
      │   ├─ 配列操作
      │   ├─ 数学関数
      │   └─ ファイルI/O
      ├─ Pandas
      │   ├─ DataFrame操作
      │   │   ├─ フィルタリング
      │   │   ├─ 集計
      │   │   └─ 結合
      │   └─ 時系列データ
      └─ Matplotlib
          ├─ 基本プロット
          └─ カスタマイズ

タグ階層の例2（用途ベース）:
ファイル操作
  ├─ 読み込み
  │   ├─ CSV
  │   ├─ JSON
  │   └─ Excel
  ├─ 書き込み
  └─ パス操作

タグ階層の例3（プロジェクトベース）:
プロジェクトA
  ├─ API呼び出し
  ├─ データベース
  └─ フロントエンド
```

### 1.2 タグの特性

#### タグの種類
1. **階層タグ（フォルダ）**: 子要素を持てる
2. **コードタグ（スニペット）**: 実際のコード
3. **複合タグ**: 両方の性質を持つ（コードを持ちつつ子要素も持つ）

#### タグのプロパティ
- **名前**: タグの表示名
- **アイコン**: カスタムアイコン（絵文字も可）
- **色**: タグの色（カテゴリ識別用）
- **ショートカット**: 1キー起動（例: `p` でPython）
- **説明**: タグの説明文
- **親タグ**: 親階層（nullの場合はルート）

---

## 2. ガジェット風UI設計

### 2.1 配置とサイズ

```
画面レイアウト（右端配置の場合）:
┌─────────────────────────────────────┐
│                                     │
│    メインデスクトップ領域            │
│                                     │
│                                     │
│                              ┌─────┐│
│                              │     ││
│                              │ ガ  ││ ← 右端固定
│                              │ ジ  ││
│                              │ ェ  ││
│                              │ ッ  ││
│                              │ ト  ││
│                              │     ││
│                              └─────┘│
└─────────────────────────────────────┘

画面レイアウト（左端配置の場合）:
┌─────────────────────────────────────┐
│                                     │
│    メインデスクトップ領域            │
│                                     │
│                                     │
│ ┌─────┐                             │
││     │                             │
││ ガ  │ ← 左端固定                   │
││ ジ  │                             │
││ ェ  │                             │
││ ッ  │                             │
││ ト  │                             │
││     │                             │
│ └─────┘                             │
└─────────────────────────────────────┘
```

#### デフォルトサイズ
- **幅**: 350px（カスタマイズ可能：250〜500px）
- **高さ**: 画面の80%（カスタマイズ可能：50〜100%）
- **位置**:
  - 右端配置（デフォルト）: 画面右端から10px
  - 左端配置: 画面左端から10px
  - 設定で切り替え可能
- **常に最前面**: 他のウィンドウの上に表示

### 2.2 外観デザイン

#### 通常状態（待機中）
```
┌──────────────────────┐
│ 🔍                  │ ← 検索アイコンのみ
│                      │
│    半透明背景         │
│   （opacity: 0.3）   │
│                      │
│                      │
└──────────────────────┘
```

#### アクティブ状態（使用中）
```
┌──────────────────────────────┐
│ 🔍 [検索ボックス]        [×] │
├──────────────────────────────┤
│ > Python                  📁  │
│   > NumPy               ⭐📁 │ ← お気に入り
│     > 配列操作            📁  │
│       ○ np.array()       📄  │ ← スニペット
│       ○ np.zeros()       📄  │
│       ○ np.ones()        📄  │
│ > JavaScript              📁  │
│   > React                 📁  │
├──────────────────────────────┤
│ [プレビュー]                  │
│ import numpy as np           │
│ arr = np.array([1, 2, 3])    │
├──────────────────────────────┤
│ Enter:挿入 Ctrl+C:コピー      │
└──────────────────────────────┘
```

#### 半透明状態（非アクティブ）
- **opacity**: 0.3（ゆっくり3秒かけてフェードアウト）
- **幅**: 60px（最小化）
- **アイコンのみ表示**

### 2.3 カラースキーム

#### ダークモード（デフォルト）
```css
背景: rgba(30, 30, 30, 0.85)
テキスト: #E0E0E0
アクセント: #64B5F6
選択項目: rgba(100, 181, 246, 0.2)
境界線: rgba(255, 255, 255, 0.1)
```

#### ライトモード
```css
背景: rgba(250, 250, 250, 0.90)
テキスト: #333333
アクセント: #2196F3
選択項目: rgba(33, 150, 243, 0.1)
境界線: rgba(0, 0, 0, 0.1)
```

#### カスタムテーマ
- **Monokai**
- **Solarized**
- **Dracula**
- **Nord**
- ユーザー定義

---

## 3. アニメーション仕様

### 3.1 起動アニメーション

```
状態遷移:
待機状態（opacity: 0.3, width: 60px）
    ↓ Ctrl ダブルタップ
フェードイン（200ms）
    ↓
スライド展開（300ms, ease-out）
    ↓
完全表示（opacity: 0.95, width: 350px）
```

#### イージング関数
```python
# スムーズな加速・減速
ease_in_out_cubic = lambda t: 4*t**3 if t < 0.5 else 1-(-2*t+2)**3/2
```

### 3.2 非アクティブ化アニメーション

```
完全表示
    ↓ 3秒間操作なし
スライド縮小（300ms, ease-in）
    ↓
フェードアウト（500ms）
    ↓
待機状態（opacity: 0.3, width: 60px）
```

### 3.3 階層展開アニメーション

```
フォルダクリック
    ↓
子要素がスライドダウン（150ms）
    ↓
アイコンが回転（90度、100ms）
```

---

## 4. 操作方法

### 4.1 ホットキー

#### 起動
- **Ctrl ダブルタップ**: ガジェットを展開
- **Ctrl + Shift + Space**: 代替起動方法
- **カスタマイズ可能**: 設定で任意のキーに変更

#### ナビゲーション
- **↑ / ↓**: 項目の選択
- **→**: フォルダを展開
- **←**: フォルダを閉じる / 親階層に戻る
- **Enter**: スニペットを挿入
- **Ctrl + C**: クリップボードにコピー
- **Ctrl + E**: スニペットを編集
- **Esc**: ガジェットを閉じる

#### 検索
- **文字入力**: インクリメンタルサーチ開始
- **Ctrl + F**: 検索ボックスにフォーカス
- **Ctrl + Backspace**: 検索クリア

#### ショートカットキー（1キー起動）
- **p**: Python階層にジャンプ
- **j**: JavaScript階層にジャンプ
- **数字キー**: お気に入り1〜9にジャンプ
- **カスタマイズ可能**

### 4.2 マウス操作

- **クリック**: 項目選択 / フォルダ展開
- **ダブルクリック**: スニペット挿入
- **右クリック**: コンテキストメニュー
- **ドラッグ**: 項目の並び替え
- **ホイール**: スクロール

### 4.3 コンテキストメニュー

```
右クリックメニュー:
├─ 挿入 (Enter)
├─ コピー (Ctrl+C)
├─ 編集 (Ctrl+E)
├─ 複製
├─ お気に入りに追加 / 削除
├─ タグを追加
├─ 移動
├─ 削除
└─ プロパティ
```

---

## 5. 階層記憶機能

### 5.1 前回位置の記憶

```python
# 使用例
session_state = {
    "last_category": "Python > NumPy > 配列操作",
    "last_selected": "np.array()",
    "expanded_folders": ["Python", "NumPy"],
    "scroll_position": 120
}
```

#### 記憶される情報
- **最後に開いていた階層**
- **最後に選択していた項目**
- **展開されていたフォルダ**
- **スクロール位置**
- **検索履歴**

### 5.2 セッション管理

```
起動時:
1. 前回のセッション状態を読み込み
2. 同じ階層で開く
3. 前回選択項目をハイライト

終了時:
1. 現在の状態を保存
2. セッションファイルに書き込み
```

### 5.3 複数セッション

```
プロジェクトごとにセッションを切り替え:
- デフォルトセッション
- プロジェクトAセッション
- プロジェクトBセッション
```

---

## 6. データ構造（改訂版）

### 6.1 タグテーブル

```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,  -- 親タグID（NULLの場合はルート）
    type TEXT NOT NULL,  -- 'folder', 'snippet', 'both'
    icon TEXT,  -- 絵文字またはアイコン名
    color TEXT,  -- HEX色コード
    shortcut_key TEXT,  -- 1キーショートカット
    description TEXT,
    order_index INTEGER DEFAULT 0,  -- 表示順
    favorite BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

### 6.2 スニペットテーブル

```sql
CREATE TABLE snippets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,  -- 所属タグ
    name TEXT NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    language TEXT,  -- プログラミング言語
    usage_count INTEGER DEFAULT 0,
    last_used DATETIME,
    favorite BOOLEAN DEFAULT 0,
    variables TEXT,  -- プレースホルダー定義（JSON）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

### 6.3 セッションテーブル

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    last_tag_id INTEGER,  -- 最後に開いていたタグ
    last_snippet_id INTEGER,  -- 最後に選択していたスニペット
    expanded_tags TEXT,  -- 展開されていたタグのID（JSON配列）
    scroll_position INTEGER DEFAULT 0,
    search_history TEXT,  -- 検索履歴（JSON配列）
    last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (last_tag_id) REFERENCES tags(id),
    FOREIGN KEY (last_snippet_id) REFERENCES snippets(id)
);
```

---

## 7. 実装例（疑似コード）

### 7.1 ガジェットウィンドウ

```python
class GadgetWindow:
    def __init__(self):
        self.state = "minimized"  # minimized, expanded
        self.opacity = 0.3
        self.width = 60
        self.animation_duration = 300  # ms

    def on_hotkey_trigger(self):
        """Ctrl ダブルタップで起動"""
        if self.state == "minimized":
            self.expand_with_animation()
        else:
            self.minimize_with_animation()

    def expand_with_animation(self):
        """展開アニメーション"""
        self.animate(
            target_opacity=0.95,
            target_width=350,
            duration=self.animation_duration,
            easing='ease_out'
        )
        self.state = "expanded"
        self.restore_last_session()

    def minimize_with_animation(self):
        """最小化アニメーション"""
        self.animate(
            target_opacity=0.3,
            target_width=60,
            duration=self.animation_duration,
            easing='ease_in'
        )
        self.state = "minimized"
        self.save_session()

    def auto_minimize_after_idle(self, idle_seconds=3):
        """3秒間操作がなければ自動的に最小化"""
        if self.get_idle_time() > idle_seconds:
            self.minimize_with_animation()
```

### 7.2 階層ナビゲーション

```python
class HierarchyNavigator:
    def __init__(self, tree_data):
        self.tree = tree_data
        self.current_path = []  # ["Python", "NumPy", "配列操作"]
        self.expanded_nodes = set()

    def navigate_down(self):
        """↓キーで次の項目へ"""
        self.selected_index = (self.selected_index + 1) % len(self.visible_items)
        self.update_preview()

    def navigate_right(self):
        """→キーでフォルダを展開"""
        if self.current_item.is_folder:
            self.expand_folder(self.current_item)
            self.current_path.append(self.current_item.name)

    def navigate_left(self):
        """←キーで親階層に戻る"""
        if self.current_path:
            self.current_path.pop()
            self.collapse_folder(self.current_item)

    def remember_position(self):
        """現在位置を記憶"""
        return {
            "path": self.current_path.copy(),
            "expanded": list(self.expanded_nodes),
            "selected": self.current_item.id
        }

    def restore_position(self, saved_position):
        """保存された位置に復元"""
        self.current_path = saved_position["path"]
        self.expanded_nodes = set(saved_position["expanded"])
        self.select_item_by_id(saved_position["selected"])
```

---

## 8. 設定項目

### 8.1 外観設定

```json
{
  "appearance": {
    "theme": "dark",
    "position": "right",
    "offset_x": 10,
    "opacity_active": 0.95,
    "opacity_inactive": 0.3,
    "width": 350,
    "width_min": 250,
    "width_max": 500,
    "height_percent": 80,
    "height_min": 50,
    "height_max": 100,
    "font_family": "Consolas",
    "font_size": 12,
    "animation_speed": 300
  }
}
```

#### 位置設定の詳細
- **position**: "right" | "left"
  - "right": 画面右端に配置（デフォルト）
  - "left": 画面左端に配置
- **offset_x**: 画面端からの距離（ピクセル）
- **offset_y**: 画面上端からの距離（ピクセル、デフォルト: 自動センタリング）

### 8.2 動作設定

```json
{
  "behavior": {
    "hotkey": "ctrl+ctrl",
    "auto_minimize_delay": 3,
    "remember_last_position": true,
    "auto_insert_enabled": true,
    "search_mode": "incremental",
    "shortcut_keys_enabled": true
  }
}
```

---

## 9. 将来の拡張機能

### 9.1 AIアシスト
- スニペットの自動分類提案
- 類似スニペットの検出
- コード補完

### 9.2 クラウド連携
- Google Drive同期
- GitHub Gist統合
- チーム共有機能

### 9.3 プラグインシステム
- カスタムテーマ
- 外部ツール連携
- APIアクセス

---

**作成日**: 2025-10-15
**バージョン**: 2.0（改訂版）
