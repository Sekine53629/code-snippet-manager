# 技術設計書

## 1. アーキテクチャ概要

### 1.1 設計パターン

**MVC（Model-View-Controller）パターン**を採用

```
┌─────────────────────────────────────────┐
│              Application                │
├─────────────────────────────────────────┤
│  View (PyQt6)                           │
│  ├─ GadgetWindow (半透明ウィンドウ)      │
│  ├─ TreeWidget (階層ツリー)             │
│  ├─ SearchBar (検索バー)                │
│  └─ PreviewPanel (プレビューパネル)      │
├─────────────────────────────────────────┤
│  Controller                             │
│  ├─ SnippetController (スニペット管理)  │
│  ├─ SearchController (検索処理)         │
│  ├─ HotkeyController (ホットキー管理)   │
│  └─ AnimationController (アニメーション) │
├─────────────────────────────────────────┤
│  Model (SQLAlchemy)                     │
│  ├─ Tag (タグモデル)                    │
│  ├─ Snippet (スニペットモデル)          │
│  ├─ Session (セッションモデル)          │
│  └─ Settings (設定モデル)               │
├─────────────────────────────────────────┤
│  Database (SQLite)                      │
│  └─ snippets.db                         │
└─────────────────────────────────────────┘
```

### 1.2 ディレクトリ構造（詳細）

```
code-snippet-manager/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py          # DB接続・初期化
│   │   ├── tag.py               # Tagモデル
│   │   ├── snippet.py           # Snippetモデル
│   │   ├── session.py           # Sessionモデル
│   │   └── settings.py          # Settingsモデル
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── gadget_window.py     # メインガジェットウィンドウ
│   │   ├── tree_widget.py       # 階層ツリーウィジェット
│   │   ├── search_bar.py        # 検索バー
│   │   ├── preview_panel.py     # プレビューパネル
│   │   ├── editor_dialog.py     # 編集ダイアログ
│   │   └── settings_dialog.py   # 設定ダイアログ
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── snippet_controller.py    # スニペット管理
│   │   ├── search_controller.py     # 検索処理
│   │   ├── hotkey_controller.py     # ホットキー管理
│   │   ├── animation_controller.py  # アニメーション制御
│   │   └── session_controller.py    # セッション管理
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── clipboard.py         # クリップボード操作
│   │   ├── auto_insert.py       # 自動挿入
│   │   ├── syntax_highlighter.py # シンタックスハイライト
│   │   ├── fuzzy_search.py      # あいまい検索
│   │   └── logger.py            # ロギング
│   │
│   └── config/
│       ├── __init__.py
│       ├── config.py            # 設定クラス
│       └── default_snippets.py  # デフォルトスニペット
│
├── data/
│   └── snippets.db              # SQLiteデータベース
│
├── config/
│   ├── settings.json            # ユーザー設定
│   └── themes/                  # テーマファイル
│       ├── dark.json
│       ├── light.json
│       └── custom.json
│
├── assets/
│   ├── icons/                   # アイコン
│   └── fonts/                   # フォント
│
├── tests/
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_utils.py
│
├── docs/
│   ├── API.md                   # API ドキュメント
│   └── USER_MANUAL.md           # ユーザーマニュアル
│
├── main.py                      # エントリーポイント
├── requirements.txt
├── REQUIREMENTS.md
├── UI_UX_DESIGN.md
├── TECHNICAL_DESIGN.md          # このファイル
└── README.md
```

---

## 2. データベース設計（詳細）

### 2.1 ER図

```
┌──────────────┐         ┌──────────────┐
│   tags       │1      ∞ │  snippets    │
│──────────────│◄────────│──────────────│
│ id (PK)      │         │ id (PK)      │
│ name         │         │ tag_id (FK)  │
│ parent_id(FK)│         │ name         │
│ type         │         │ code         │
│ icon         │         │ language     │
│ color        │         │ ...          │
│ ...          │         └──────────────┘
└──────────────┘
       ▲
       │ self-reference
       │
       └───────┐
               │
         ┌──────────────┐
         │  sessions    │
         │──────────────│
         │ id (PK)      │
         │ name         │
         │ last_tag_id  │
         │ ...          │
         └──────────────┘
```

### 2.2 テーブル定義（SQLAlchemy）

#### tags テーブル

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Tag(Base):
    __tablename__ = 'tags'

    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 基本情報
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('tags.id'), nullable=True)
    type = Column(String(20), nullable=False)  # 'folder', 'snippet', 'both'

    # 表示設定
    icon = Column(String(50), default='📁')
    color = Column(String(7), default='#64B5F6')  # HEX color
    shortcut_key = Column(String(1), nullable=True, unique=True)

    # メタデータ
    description = Column(String(500), default='')
    order_index = Column(Integer, default=0)
    favorite = Column(Boolean, default=False)

    # タイムスタンプ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーション
    children = relationship('Tag', backref=backref('parent', remote_side=[id]))
    snippets = relationship('Snippet', back_populates='tag', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', type='{self.type}')>"
```

#### snippets テーブル

```python
class Snippet(Base):
    __tablename__ = 'snippets'

    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 外部キー
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

    # 基本情報
    name = Column(String(255), nullable=False)
    description = Column(Text, default='')
    code = Column(Text, nullable=False)
    language = Column(String(50), default='text')

    # 変数・プレースホルダー（JSON形式）
    # 例: {"variables": [{"name": "var1", "default": "value1"}]}
    variables = Column(Text, nullable=True)

    # 統計情報
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)
    favorite = Column(Boolean, default=False)

    # タイムスタンプ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーション
    tag = relationship('Tag', back_populates='snippets')

    def __repr__(self):
        return f"<Snippet(id={self.id}, name='{self.name}', language='{self.language}')>"
```

#### sessions テーブル

```python
class Session(Base):
    __tablename__ = 'sessions'

    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)

    # セッション名
    name = Column(String(100), nullable=False, unique=True)

    # 状態保存
    last_tag_id = Column(Integer, ForeignKey('tags.id'), nullable=True)
    last_snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=True)
    expanded_tags = Column(Text, nullable=True)  # JSON配列: [1, 3, 5]
    scroll_position = Column(Integer, default=0)
    search_history = Column(Text, nullable=True)  # JSON配列

    # タイムスタンプ
    last_used = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Session(name='{self.name}')>"
```

#### settings テーブル

```python
class Settings(Base):
    __tablename__ = 'settings'

    # 主キー
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 設定キー・バリュー
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=False)

    # タイムスタンプ
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Settings(key='{self.key}', value='{self.value[:20]}...')>"
```

### 2.3 インデックス設計

```sql
-- パフォーマンス最適化用インデックス
CREATE INDEX idx_tags_parent_id ON tags(parent_id);
CREATE INDEX idx_tags_favorite ON tags(favorite);
CREATE INDEX idx_snippets_tag_id ON snippets(tag_id);
CREATE INDEX idx_snippets_language ON snippets(language);
CREATE INDEX idx_snippets_favorite ON snippets(favorite);
CREATE INDEX idx_snippets_usage_count ON snippets(usage_count DESC);
CREATE INDEX idx_settings_key ON settings(key);

-- 全文検索用インデックス（FTS5）
CREATE VIRTUAL TABLE snippets_fts USING fts5(
    snippet_id,
    name,
    description,
    code,
    content='snippets',
    content_rowid='id'
);
```

---

## 3. コンポーネント設計

### 3.1 GadgetWindow（メインウィンドウ）

#### 責務
- 半透明ウィンドウの管理
- 画面位置の制御（左右切り替え）
- アニメーション制御
- 子ウィジェットの配置

#### 主要メソッド

```python
class GadgetWindow(QWidget):
    def __init__(self, config: Config):
        """初期化"""
        super().__init__()
        self.config = config
        self.state = 'minimized'
        self.setup_ui()
        self.setup_position()

    def setup_ui(self):
        """UI初期化"""
        # ウィンドウフラグ設定
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        # 半透明設定
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(self.config.appearance.opacity_inactive)

    def setup_position(self):
        """画面位置の設定"""
        screen = QApplication.primaryScreen().geometry()

        if self.config.appearance.position == 'right':
            # 右端配置
            x = screen.width() - self.width() - self.config.appearance.offset_x
        else:
            # 左端配置
            x = self.config.appearance.offset_x

        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def expand(self):
        """展開アニメーション"""
        self.animation_controller.animate_expand(
            target_width=self.config.appearance.width,
            target_opacity=self.config.appearance.opacity_active,
            duration=self.config.appearance.animation_speed
        )
        self.state = 'expanded'

    def minimize(self):
        """最小化アニメーション"""
        self.animation_controller.animate_minimize(
            target_width=60,
            target_opacity=self.config.appearance.opacity_inactive,
            duration=self.config.appearance.animation_speed
        )
        self.state = 'minimized'
```

### 3.2 TreeWidget（階層ツリー）

#### 責務
- タグとスニペットの階層表示
- ドラッグ&ドロップによる並び替え
- 展開・折りたたみの管理

#### 主要メソッド

```python
class HierarchyTreeWidget(QTreeWidget):
    item_selected = pyqtSignal(object)  # Tag or Snippet

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()

    def load_data(self, parent_tag_id=None):
        """データベースから階層データをロード"""
        tags = self.db.query(Tag).filter_by(parent_id=parent_tag_id).all()

        for tag in tags:
            item = QTreeWidgetItem([tag.name])
            item.setIcon(0, QIcon(tag.icon))
            item.setData(0, Qt.UserRole, tag)

            # 子要素を再帰的にロード
            if tag.type in ['folder', 'both']:
                self.load_data(tag.id)

    def on_item_clicked(self, item, column):
        """項目クリック時の処理"""
        data = item.data(0, Qt.UserRole)
        self.item_selected.emit(data)
```

### 3.3 SearchController（検索コントローラ）

#### 責務
- インクリメンタルサーチ
- あいまい検索（Fuzzy Search）
- 検索履歴の管理

#### 主要メソッド

```python
class SearchController:
    def __init__(self, db_session):
        self.db = db_session
        self.search_history = []

    def search_incremental(self, query: str) -> List[Snippet]:
        """インクリメンタルサーチ"""
        # 部分一致検索
        results = self.db.query(Snippet).filter(
            or_(
                Snippet.name.like(f'%{query}%'),
                Snippet.description.like(f'%{query}%'),
                Snippet.code.like(f'%{query}%')
            )
        ).limit(50).all()

        return results

    def search_fuzzy(self, query: str, threshold: int = 70) -> List[Snippet]:
        """あいまい検索"""
        from fuzzywuzzy import fuzz

        all_snippets = self.db.query(Snippet).all()
        results = []

        for snippet in all_snippets:
            # 名前との類似度
            ratio = fuzz.partial_ratio(query.lower(), snippet.name.lower())
            if ratio >= threshold:
                results.append((snippet, ratio))

        # スコア順にソート
        results.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in results[:50]]
```

### 3.4 HotkeyController（ホットキーコントローラ）

#### 責務
- グローバルホットキーの監視
- Ctrlダブルタップの検出
- カスタムホットキーの管理

#### 主要メソッド

```python
from pynput import keyboard
import time

class HotkeyController:
    def __init__(self, callback):
        self.callback = callback
        self.last_ctrl_press = 0
        self.double_tap_threshold = 0.3  # 300ms

    def start(self):
        """ホットキー監視開始"""
        listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        listener.start()

    def on_key_press(self, key):
        """キー押下時の処理"""
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            current_time = time.time()

            # Ctrlダブルタップの検出
            if current_time - self.last_ctrl_press < self.double_tap_threshold:
                self.callback()  # ガジェットを起動

            self.last_ctrl_press = current_time
```

### 3.5 AnimationController（アニメーションコントローラ）

#### 責務
- スムーズなアニメーション制御
- イージング関数の適用

#### 主要メソッド

```python
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

class AnimationController:
    def __init__(self, widget: QWidget):
        self.widget = widget

    def animate_expand(self, target_width, target_opacity, duration):
        """展開アニメーション"""
        # 幅のアニメーション
        width_anim = QPropertyAnimation(self.widget, b"minimumWidth")
        width_anim.setDuration(duration)
        width_anim.setStartValue(self.widget.width())
        width_anim.setEndValue(target_width)
        width_anim.setEasingCurve(QEasingCurve.OutCubic)

        # 透明度のアニメーション
        opacity_anim = QPropertyAnimation(self.widget, b"windowOpacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setStartValue(self.widget.windowOpacity())
        opacity_anim.setEndValue(target_opacity)

        # 同時実行
        width_anim.start()
        opacity_anim.start()
```

---

## 4. 設定管理システム

### 4.1 設定クラス（Pydantic）

```python
from pydantic import BaseModel, Field
from typing import Literal

class AppearanceConfig(BaseModel):
    theme: Literal['dark', 'light', 'custom'] = 'dark'
    position: Literal['left', 'right'] = 'right'
    offset_x: int = Field(default=10, ge=0, le=100)
    opacity_active: float = Field(default=0.95, ge=0.1, le=1.0)
    opacity_inactive: float = Field(default=0.3, ge=0.1, le=1.0)
    width: int = Field(default=350, ge=250, le=500)
    height_percent: int = Field(default=80, ge=50, le=100)
    font_family: str = 'Consolas'
    font_size: int = Field(default=12, ge=8, le=24)
    animation_speed: int = Field(default=300, ge=100, le=1000)

class BehaviorConfig(BaseModel):
    hotkey: str = 'ctrl+ctrl'
    auto_minimize_delay: int = Field(default=3, ge=1, le=10)
    remember_last_position: bool = True
    auto_insert_enabled: bool = True
    search_mode: Literal['incremental', 'fuzzy', 'both'] = 'both'
    shortcut_keys_enabled: bool = True

class Config(BaseModel):
    appearance: AppearanceConfig = AppearanceConfig()
    behavior: BehaviorConfig = BehaviorConfig()

    def save(self, path: str = './config/settings.json'):
        """設定をファイルに保存"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str = './config/settings.json'):
        """設定をファイルから読み込み"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
```

---

## 5. パフォーマンス最適化

### 5.1 データベースクエリ最適化

```python
# 悪い例：N+1問題
for tag in tags:
    snippets = session.query(Snippet).filter_by(tag_id=tag.id).all()

# 良い例：Eager Loading
tags = session.query(Tag).options(
    joinedload(Tag.snippets)
).all()
```

### 5.2 検索パフォーマンス

```python
# FTS5を使用した全文検索
cursor.execute("""
    SELECT snippet_id, name, description
    FROM snippets_fts
    WHERE snippets_fts MATCH ?
    ORDER BY rank
    LIMIT 50
""", (query,))
```

### 5.3 UIレンダリング最適化

```python
# 仮想スクロール（大量データ対応）
class VirtualTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setUniformRowHeights(True)  # 高速化
        self.setAnimated(False)  # アニメーション無効化
```

---

## 6. セキュリティ考慮事項

### 6.1 コード実行のサンドボックス化

```python
# 危険なコードの実行を防ぐ
def safe_execute_snippet(code: str):
    # 危険な文字列をチェック
    dangerous_patterns = [
        'os.system', 'subprocess', 'eval', 'exec',
        '__import__', 'open('
    ]

    for pattern in dangerous_patterns:
        if pattern in code:
            raise SecurityError(f"Dangerous code detected: {pattern}")
```

### 6.2 データベース暗号化（オプション）

```python
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

class Snippet(Base):
    # センシティブなコードを暗号化
    code = Column(EncryptedType(Text, key='encryption_key', engine=AesEngine))
```

---

## 7. テスト戦略

### 7.1 ユニットテスト

```python
# tests/test_models.py
def test_create_tag():
    tag = Tag(name='Python', type='folder')
    assert tag.name == 'Python'
    assert tag.type == 'folder'

# tests/test_search_controller.py
def test_search_incremental():
    controller = SearchController(db_session)
    results = controller.search_incremental('numpy')
    assert len(results) > 0
    assert 'numpy' in results[0].name.lower()
```

### 7.2 統合テスト

```python
@pytest.mark.qt
def test_gadget_window_expand(qtbot):
    window = GadgetWindow(config)
    qtbot.addWidget(window)

    window.expand()
    qtbot.wait(500)  # アニメーション待機

    assert window.state == 'expanded'
    assert window.windowOpacity() == 0.95
```

---

**作成日**: 2025-10-15
**バージョン**: 1.0
