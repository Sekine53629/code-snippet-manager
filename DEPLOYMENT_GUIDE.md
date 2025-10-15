# 配布・デプロイメントガイド（Windows向け）

## 1. 対象環境

### 1.1 ターゲット環境
- **OS**: Windows 10/11（64bit）
- **必要環境**: なし（EXE単体で動作）
- **推奨**: Windows Defender以外のアンチウイルスソフト使用時は除外設定

### 1.2 配布形態
1. **スタンドアロン版**: EXE単体 + データフォルダ
2. **ネットワーク版**: EXE + 共有データベースサーバー接続

---

## 2. 開発環境セットアップ（Windows最適化）

### 2.1 推奨開発環境

```powershell
# Python 3.11推奨（Windows向けに最適化）
python --version  # Python 3.11.x

# プロジェクトディレクトリへ移動
cd code-snippet-manager

# 仮想環境作成（余計なライブラリを拾わないため必須）
python -m venv venv

# 仮想環境アクティベート（PowerShell）
.\venv\Scripts\Activate.ps1

# または（コマンドプロンプト）
venv\Scripts\activate.bat

# 依存パッケージインストール
pip install -r requirements.txt
```

### 2.2 requirements.txt（Windows最適化版）

```txt
# GUI - Windows Native最適化
PyQt6==6.6.1
PyQt6-Qt6==6.6.1

# データベース（SQLite - Windows互換性◎）
SQLAlchemy==2.0.23

# ホットキー（Windows専用）
keyboard==0.13.5  # 管理者権限不要
pynput==1.7.6     # フォールバック用

# クリップボード（Windows最適化）
pyperclip==1.8.2
pywin32==306      # Windows API直接利用

# シンタックスハイライト
Pygments==2.17.2

# その他ユーティリティ
python-dateutil==2.8.2
pydantic==2.5.2
pydantic-settings==2.1.0

# 検索（あいまい検索）
fuzzywuzzy==0.18.0
python-Levenshtein==0.23.0

# EXE化（配布用）
pyinstaller==6.3.0

# ネットワーク（データベース共有用）
requests==2.31.0

# 設定ファイル
toml==0.10.2

# テスト
pytest==7.4.3
pytest-qt==4.2.0
```

---

## 3. データベース設計（共有対応）

### 3.1 データベース配置パターン

#### パターン1: ローカル専用（デフォルト）
```
%APPDATA%\CodeSnippetManager\
├── database\
│   ├── local.db          # ユーザー個人のデータ
│   └── cache\
└── config\
    └── settings.json
```

#### パターン2: 本部配信データ参照
```
%APPDATA%\CodeSnippetManager\
├── database\
│   ├── local.db              # ユーザー個人
│   ├── shared.db (ReadOnly)  # 本部配信（読み取り専用）
│   └── cache\
└── config\
    └── settings.json
```

#### パターン3: ネットワーク共有
```
ローカル:
%APPDATA%\CodeSnippetManager\
├── database\
│   ├── local.db
│   └── cache\

ネットワーク:
\\server\share\CodeSnippetManager\
└── database\
    └── company_shared.db     # 全社共有
```

### 3.2 データベース設定

```json
// settings.json
{
  "database": {
    "mode": "hybrid",
    "local": {
      "path": "%APPDATA%/CodeSnippetManager/database/local.db",
      "writable": true
    },
    "shared": {
      "enabled": true,
      "path": "\\\\server\\share\\CodeSnippetManager\\database\\company_shared.db",
      "readonly": true,
      "auto_sync": true,
      "sync_interval": 3600
    },
    "priority": "local_first"
  }
}
```

### 3.3 データベース統合検索

```python
class MultiDatabaseManager:
    def __init__(self, config):
        # ローカルDB（読み書き可能）
        self.local_db = create_engine(f'sqlite:///{config.local.path}')

        # 共有DB（読み取り専用）
        if config.shared.enabled:
            self.shared_db = create_engine(
                f'sqlite:///{config.shared.path}',
                connect_args={'mode': 'ro'}  # 読み取り専用
            )

    def search_snippets(self, query):
        """複数DBから検索（ローカル優先）"""
        results = []

        # ローカルから検索
        local_results = self.search_in_db(self.local_db, query)
        results.extend(local_results)

        # 共有DBから検索（重複除外）
        if self.shared_db:
            shared_results = self.search_in_db(self.shared_db, query)
            results.extend(shared_results)

        return self.deduplicate(results)
```

---

## 4. 本部配信システム

### 4.1 配信方法

#### 方法1: ファイル共有
```
\\server\share\CodeSnippetManager\
├── database\
│   └── company_shared.db     # 本部が更新
├── updates\
│   ├── version.json          # バージョン情報
│   └── changelog.txt
└── templates\
    └── project_templates.json # プロジェクトテンプレート
```

#### 方法2: HTTPサーバー（REST API）
```
https://company-server.com/snippet-api/
├── GET  /snippets            # スニペット一覧取得
├── GET  /snippets/{id}       # 個別取得
├── GET  /tags                # タグ階層取得
└── GET  /updates/check       # 更新確認
```

### 4.2 自動同期機能

```python
class SyncController:
    def __init__(self, config):
        self.config = config
        self.last_sync = None

    def check_updates(self):
        """本部配信データの更新確認"""
        if self.config.shared.enabled:
            remote_version = self.get_remote_version()
            local_version = self.get_local_version()

            if remote_version > local_version:
                return True
        return False

    def sync_shared_database(self):
        """共有DBの同期"""
        try:
            # 共有DBファイルをコピー（読み取り専用）
            src = self.config.shared.path
            dst = self.config.shared.cache_path

            shutil.copy2(src, dst)
            self.set_readonly(dst)

            self.last_sync = datetime.now()
            return True
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return False
```

### 4.3 差分更新システム

```python
class DeltaUpdate:
    """差分更新（効率的なデータ配信）"""

    def create_delta(self, old_db, new_db):
        """変更分のみを抽出"""
        delta = {
            "added": [],
            "modified": [],
            "deleted": []
        }

        # 新規追加
        new_snippets = self.get_snippets_after(new_db, last_sync_time)
        delta["added"].extend(new_snippets)

        return delta

    def apply_delta(self, local_db, delta):
        """差分を適用"""
        session = Session(local_db)

        for snippet_data in delta["added"]:
            snippet = Snippet(**snippet_data)
            session.add(snippet)

        session.commit()
```

---

## 5. EXE化（PyInstaller）

### 5.1 PyInstaller設定

```python
# build_config.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),           # アイコン等
        ('config', 'config'),           # デフォルト設定
        ('data/templates', 'templates') # テンプレート
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'sqlalchemy.dialects.sqlite',
        'pydantic',
        'keyboard',
        'pyperclip'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # 不要なライブラリを除外
        'numpy',
        'pandas',
        'PIL',
        'tkinter'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodeSnippetManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,              # UPXで圧縮
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,         # コンソール非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'  # アイコン
)
```

### 5.2 ビルドスクリプト

```powershell
# build.ps1
# 仮想環境アクティベート
.\venv\Scripts\Activate.ps1

# ビルド前のクリーンアップ
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue

# PyInstallerでビルド
pyinstaller build_config.spec

# バージョン情報を埋め込み（オプション）
$versionInfo = @"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'YourCompany'),
            StringStruct(u'FileDescription', u'Code Snippet Manager'),
            StringStruct(u'FileVersion', u'1.0.0.0'),
            StringStruct(u'ProductName', u'CodeSnippetManager'),
            StringStruct(u'ProductVersion', u'1.0.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"@

# 配布用ZIPを作成
Compress-Archive -Path "dist\CodeSnippetManager.exe", "data", "config", "README.txt" -DestinationPath "CodeSnippetManager_v1.0.0.zip"

Write-Host "Build completed! Output: dist/CodeSnippetManager.exe"
```

### 5.3 サイズ最適化

```powershell
# 最適化のコツ

# 1. UPXで圧縮（30-50%削減）
upx --best --lzma dist\CodeSnippetManager.exe

# 2. 不要なDLLを除外
# build_config.spec の excludes に追加

# 3. PyQt6の最適化
# 必要なモジュールのみインポート
from PyQt6.QtWidgets import QApplication  # OK
from PyQt6 import *  # NG（サイズ増加）

# 期待サイズ: 20-30MB（最適化後）
```

---

## 6. インストーラー作成

### 6.1 Inno Setup設定

```iss
; installer.iss
[Setup]
AppName=Code Snippet Manager
AppVersion=1.0.0
DefaultDirName={autopf}\CodeSnippetManager
DefaultGroupName=Code Snippet Manager
OutputDir=installer
OutputBaseFilename=CodeSnippetManager_Setup
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\CodeSnippetManager.exe

[Files]
Source: "dist\CodeSnippetManager.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs ignoreversion
Source: "config\*"; DestDir: "{app}\config"; Flags: recursesubdirs ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Code Snippet Manager"; Filename: "{app}\CodeSnippetManager.exe"
Name: "{autodesktop}\Code Snippet Manager"; Filename: "{app}\CodeSnippetManager.exe"

[Run]
Filename: "{app}\CodeSnippetManager.exe"; Description: "Launch Code Snippet Manager"; Flags: postinstall nowait skipifsilent

[Registry]
; スタートアップ登録（オプション）
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "CodeSnippetManager"; ValueData: "{app}\CodeSnippetManager.exe"; Flags: uninsdeletevalue

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // 既存インストールチェック
end;
```

### 6.2 配布パッケージ構成

```
CodeSnippetManager_v1.0.0\
├── CodeSnippetManager.exe       # メインプログラム
├── data\
│   └── templates\
│       └── default_snippets.db  # サンプルスニペット
├── config\
│   └── default_settings.json    # デフォルト設定
├── README.txt
├── LICENSE.txt
└── CHANGELOG.txt
```

---

## 7. 配布後のデータベース挿入

### 7.1 管理者用ツール

```python
# admin_tool.py（本部用）
"""本部がスニペットを配信するためのツール"""

class AdminTool:
    def __init__(self):
        self.db = Database('company_shared.db')

    def add_snippet(self, tag_path, name, code, description):
        """スニペットを追加"""
        tag = self.get_or_create_tag_path(tag_path)

        snippet = Snippet(
            tag_id=tag.id,
            name=name,
            code=code,
            description=description,
            created_by='admin'
        )

        self.db.session.add(snippet)
        self.db.session.commit()

        print(f"✓ Added: {name}")

    def import_from_json(self, json_file):
        """JSONからバルクインポート"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data['snippets']:
            self.add_snippet(
                tag_path=item['path'],
                name=item['name'],
                code=item['code'],
                description=item.get('description', '')
            )

# 使用例
if __name__ == '__main__':
    admin = AdminTool()
    admin.import_from_json('new_snippets.json')
```

### 7.2 配信JSONフォーマット

```json
{
  "version": "1.0.0",
  "release_date": "2025-10-15",
  "snippets": [
    {
      "path": "会社共通/Python/データ処理",
      "name": "CSVファイル読み込み",
      "language": "python",
      "code": "import pandas as pd\ndf = pd.read_csv('data.csv', encoding='cp932')",
      "description": "日本語CSVを読み込む標準コード",
      "tags": ["csv", "pandas", "日本語"],
      "priority": "high"
    },
    {
      "path": "会社共通/SQL/よく使うクエリ",
      "name": "月次売上集計",
      "language": "sql",
      "code": "SELECT\n  DATE_FORMAT(order_date, '%Y-%m') AS month,\n  SUM(amount) AS total\nFROM orders\nGROUP BY month",
      "description": "月別の売上を集計",
      "tags": ["sql", "集計"],
      "priority": "normal"
    }
  ]
}
```

### 7.3 自動配信システム

```python
class AutoDeployment:
    """自動配信システム"""

    def deploy_to_network_share(self, db_file, target_path):
        """ネットワーク共有に配信"""
        try:
            # バックアップ作成
            if os.path.exists(target_path):
                backup_path = f"{target_path}.backup"
                shutil.copy2(target_path, backup_path)

            # 新しいDBをコピー
            shutil.copy2(db_file, target_path)

            # 読み取り専用に設定
            os.chmod(target_path, 0o444)

            # version.jsonを更新
            version_info = {
                "version": "1.0.1",
                "date": datetime.now().isoformat(),
                "changelog": "新しいスニペット追加"
            }
            with open(os.path.join(os.path.dirname(target_path), 'version.json'), 'w') as f:
                json.dump(version_info, f, indent=2)

            print("✓ Deployment successful")
            return True

        except Exception as e:
            print(f"✗ Deployment failed: {e}")
            return False
```

---

## 8. 設定の柔軟性

### 8.1 設定UI

```python
class DatabaseSettingsDialog(QDialog):
    """データベース設定ダイアログ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # ローカルDB設定
        local_group = QGroupBox("ローカルデータベース")
        local_layout = QVBoxLayout()

        self.local_path = QLineEdit()
        self.local_browse = QPushButton("参照...")
        self.local_browse.clicked.connect(self.browse_local_path)

        local_layout.addWidget(QLabel("保存場所:"))
        local_layout.addWidget(self.local_path)
        local_layout.addWidget(self.local_browse)
        local_group.setLayout(local_layout)

        # 共有DB設定
        shared_group = QGroupBox("共有データベース（本部配信）")
        shared_layout = QVBoxLayout()

        self.shared_enabled = QCheckBox("共有データベースを使用する")
        self.shared_path = QLineEdit()
        self.shared_path.setPlaceholderText(r"\\server\share\CodeSnippetManager\database\shared.db")
        self.shared_browse = QPushButton("参照...")

        shared_layout.addWidget(self.shared_enabled)
        shared_layout.addWidget(QLabel("共有DB場所:"))
        shared_layout.addWidget(self.shared_path)
        shared_layout.addWidget(self.shared_browse)
        shared_group.setLayout(shared_layout)

        # 同期設定
        sync_group = QGroupBox("同期設定")
        sync_layout = QVBoxLayout()

        self.auto_sync = QCheckBox("起動時に自動同期")
        self.sync_interval = QSpinBox()
        self.sync_interval.setRange(10, 3600)
        self.sync_interval.setValue(300)
        self.sync_interval.setSuffix(" 分")

        sync_layout.addWidget(self.auto_sync)
        sync_layout.addWidget(QLabel("同期間隔:"))
        sync_layout.addWidget(self.sync_interval)
        sync_group.setLayout(sync_layout)

        layout.addWidget(local_group)
        layout.addWidget(shared_group)
        layout.addWidget(sync_group)

        # ボタン
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
```

---

## 9. チェックリスト

### 開発環境
- [ ] Python 3.11インストール
- [ ] 仮想環境作成
- [ ] requirements.txtからインストール
- [ ] PyQt6動作確認

### ビルド準備
- [ ] PyInstallerインストール
- [ ] build_config.spec作成
- [ ] アイコンファイル準備
- [ ] 不要なライブラリ除外設定

### テスト
- [ ] EXE単体で動作確認
- [ ] Windows 10/11で動作確認
- [ ] ネットワーク共有接続テスト
- [ ] 複数ユーザーでの動作確認

### 配布準備
- [ ] インストーラー作成
- [ ] README作成
- [ ] ライセンスファイル
- [ ] 動作マニュアル

---

**作成日**: 2025-10-15
**バージョン**: 1.0（Windows最適化版）
