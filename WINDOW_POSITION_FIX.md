# ウィンドウ位置とマウス操作の修正

## 実施日
2025-10-17

## 修正内容

### 1. ウィンドウの初期位置を上部に変更

**問題**:
- ウィンドウが画面の垂直中央に配置されていた
- 他のアプリやシステム機能（ドック、メニューバーのポップアップ等）の邪魔になる可能性があった

**修正**:
- ウィンドウの初期位置を画面上部に変更
- メニューバーを避けるために50pxのオフセットを追加
- `offset_y` 設定値でさらに調整可能

**修正箇所**: `src/views/gadget_window.py:103-105`

```python
# Before
y = (screen.height() - self.height()) // 2 + self.config.appearance.offset_y

# After
# Position at top of screen with offset
# Offset from top to avoid menu bar (typically 25-30px on macOS)
y = 50 + self.config.appearance.offset_y
```

---

### 2. マウス操作の優先度を修正

**問題**:
- ウィンドウ上でスクロール操作（二本指スワイプ等）したとき、下にあるウィンドウが反応してしまう
- レイヤー最上位のウィンドウにカーソルがあっても、操作が下のウィンドウに伝播していた

**修正**:
以下の対応を実施：

#### 2.1 ウィンドウ全体の設定強化

**追加設定**:
- `setMouseTracking(True)` - マウストラッキングを有効化
- `setFocusPolicy(Qt.FocusPolicy.StrongFocus)` - フォーカスポリシーを強化
- `setAttribute(Qt.WidgetAttribute.WA_Hover, True)` - ホバーイベントを有効化

**修正箇所**: `src/views/gadget_window.py:82-89`

```python
# Enable mouse tracking to capture all mouse events
self.setMouseTracking(True)

# Set focus policy to accept focus and capture input
self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

# Enable hover events to ensure window receives mouse events
self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
```

#### 2.2 子ウィジェットの設定

全ての主要ウィジェット（TreeWidget, TextEdit, LineEdit）にマウストラッキングを追加：

**TreeWidget**: `src/views/gadget_window.py:280-282`
```python
self.tree.setMouseTracking(True)
self.tree.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
```

**TextEdit (Preview)**: `src/views/gadget_window.py:290-292`
```python
self.preview.setMouseTracking(True)
self.preview.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
```

**LineEdit (Search)**: `src/views/gadget_window.py:250-252`
```python
self.search_input.setMouseTracking(True)
self.search_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
```

#### 2.3 イベントハンドラーの追加

**enterEvent** - マウスがウィンドウに入った時
```python
def enterEvent(self, event):
    """Handle mouse enter event - activate window to capture input."""
    super().enterEvent(event)
    # Activate window when mouse enters to ensure input is captured
    self.activateWindow()
    self.raise_()
```

**wheelEvent** - スクロール操作
```python
def wheelEvent(self, event):
    """Handle wheel event - ensure scrolling works within window."""
    # Accept the event to prevent it from propagating to windows below
    event.accept()

    # Find the widget under the cursor and forward to it
    widget = self.childAt(event.position().toPoint())
    # ... (詳細は実装参照)
```

**mousePressEvent** - マウスクリック
```python
def mousePressEvent(self, event):
    """Handle mouse press event - ensure window handles clicks."""
    event.accept()
    # Activate window on click
    self.activateWindow()
    self.raise_()
    super().mousePressEvent(event)
```

**focusInEvent** - フォーカス取得
```python
def focusInEvent(self, event):
    """Handle focus in event."""
    super().focusInEvent(event)
    # Ensure window stays on top when focused
    if self.is_always_on_top:
        self.raise_()
```

**修正箇所**: `src/views/gadget_window.py:1039-1093`

---

## 動作原理

### イベント伝播の防止

1. **enterEvent**: マウスがウィンドウに入った瞬間にウィンドウをアクティブ化
2. **wheelEvent**: スクロールイベントを `accept()` して下のウィンドウへの伝播を防止
3. **mousePressEvent**: クリックイベントを `accept()` して確実にウィンドウがアクティブに
4. **focusInEvent**: フォーカス取得時に最前面に維持

### ホイールイベントの正確な転送

ウィンドウがホイールイベントを受け取った後、以下の処理を行う：

1. イベント位置にある子ウィジェットを検索
2. QTreeWidget または QTextEdit を見つけるまで親を辿る
3. 見つかったウィジェットに新しいホイールイベントを作成して転送
4. 見つからない場合は親クラスの処理に委譲（それでもイベントは accept 済み）

これにより、スクロール可能なウィジェット内では正常にスクロールが動作し、かつイベントが下のウィンドウに伝播しない。

---

## テスト方法

### 1. ウィンドウ位置の確認

```bash
python main.py
```

- ウィンドウが画面上部に表示されることを確認
- メニューバーやノッチの下に表示されることを確認
- 他のアプリのUIと重ならないことを確認

### 2. マウス操作の確認

#### テスト A: スクロール操作
1. Code Snippet Manager のウィンドウを表示
2. 下に別のアプリ（ブラウザやエディタ等）を表示
3. Code Snippet Manager のウィンドウ上で二本指スワイプ（スクロール）
4. **期待結果**: Code Snippet Manager 内がスクロールし、下のアプリは反応しない

#### テスト B: クリック操作
1. Code Snippet Manager のウィンドウを表示
2. ウィンドウ上の任意の場所をクリック
3. **期待結果**: ウィンドウがアクティブになり、下のアプリには影響しない

#### テスト C: ホバー操作
1. Code Snippet Manager のウィンドウを表示
2. マウスカーソルをウィンドウ上に移動（クリックせず）
3. **期待結果**: ウィンドウが自動的にアクティブになる

#### テスト D: 最小化時の動作
1. ウィンドウを最小化
2. 下のアプリを操作
3. **期待結果**: 最小化時は下のアプリが正常に操作できる

---

## 設定ファイルでの調整

`config.toml` の `[appearance]` セクションで位置を微調整可能：

```toml
[appearance]
offset_x = 10      # 水平位置のオフセット
offset_y = 0       # 垂直位置のオフセット（50pxベースに追加）
```

例えば、さらに下に移動したい場合：
```toml
offset_y = 100  # 50 + 100 = 150px from top
```

---

## 既知の制限事項

### macOS システムの制限

- macOS のセキュリティ設定により、一部のシステムウィンドウ（Notification Center, Control Center等）は常に最前面に表示される
- アプリケーションがアクティブでない場合、一部のマウスイベントがシステムに優先される可能性がある

### 対処法

ほとんどのケースで問題ないが、もし下のウィンドウが反応する場合：
1. ウィンドウ上で一度クリックしてアクティブ化
2. ホットキー（Ctrl 2回押し）で再表示してアクティブ化

---

## まとめ

この修正により：

✅ **ウィンドウ位置**: 画面上部に配置、他のUIと干渉しない
✅ **マウス優先度**: ウィンドウ上のマウス操作が確実にキャプチャされる
✅ **スクロール動作**: ウィンドウ内で正常に動作し、下のアプリに影響しない
✅ **Always on Top**: 最上位レイヤーでの操作が優先される

ユーザー体験が大幅に改善され、他のアプリと共存しながらスムーズに使用できるようになりました。
