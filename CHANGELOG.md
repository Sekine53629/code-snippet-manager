# Changelog

All notable changes to Code Snippet Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-15

### 🎉 Initial Release

First stable release of Code Snippet Manager - a programmer-focused code snippet management application.

### Added

#### Phase 1: Foundation
- Database models (Tag, Snippet, TagSnippet, Session, SearchIndex)
- Configuration management system (Pydantic, type-safe)
- Multi-database manager (local + shared read-only DB)
- CRUD operations (Create, Read, Update, Delete)
- Search and filter functionality
- Test suite (9/9 tests passing)

#### Phase 2: Basic UI
- Semi-transparent gadget-style main window
- Hierarchical tag tree display with icons and colors
- Snippet preview panel with code display
- Incremental search functionality
- Clipboard copy support
- Snippet count display per tag
- Tree-embedded snippet display
- Context menu (right-click)
- Usage tracking
- Snippet creation/edit/delete dialogs
- Multi-tag selection
- Input validation
- Test suite (13/13 tests passing)

#### Phase 3: Core Features
- Fuzzy search (typo-tolerant search)
- Clipboard operations utility
- Auto-insert functionality (active window detection)
- Cross-platform support (macOS, Windows, Linux)
- Test suite (6/6 tests passing)

#### Phase 4: Advanced Features
- Hotkey system (Ctrl double-tap detection)
- Animation controller
  - Fade in/out
  - Expand/collapse
  - Edge docking animations
- Test suite (6/6 tests passing)

#### Phase 5: UI/UX Improvements
- Syntax highlighting (Pygments integration, 48 themes)
- Real-time Qt-integrated highlighter
- Settings dialog (3 tabs: Appearance, Behavior, Database)
- Dark/Light theme support
- Test suite (5/5 tests passing)

#### Phase 6: Extended Features
- Import/Export (JSON, Markdown formats)
- Backup/Restore functionality
- Statistics dialog (usage visualization)
- Favorite snippets functionality
- Test suite (5/5 tests passing)

#### Phase 7: Integration & Testing
- Main application entry point
- Full component integration
- Hotkey integration
- Theme system
- Integration test suite (6/6 tests passing)
- Module structure improvements (absolute imports)

#### Phase 8: Documentation & Distribution
- Comprehensive README.md
- PyInstaller build configuration
- Build scripts for executable generation
- CHANGELOG.md (this file)

### Technical Stack

- **Language**: Python 3.9+
- **GUI**: PyQt6
- **Database**: SQLite3 + SQLAlchemy
- **Configuration**: Pydantic
- **Clipboard**: pyperclip
- **Syntax Highlighting**: Pygments
- **Fuzzy Search**: difflib + fuzzywuzzy
- **Build**: PyInstaller

### Test Coverage

- **Total Tests**: 50+ tests across all phases
- **Integration Tests**: 6/6 passing
- **Coverage**: 73% (11/15 components, non-GUI fully tested)

### Known Limitations

- GUI components require manual testing
- Hotkey functionality requires accessibility permissions on macOS
- Auto-insert may require elevated privileges on some systems

---

## [Unreleased]

### Planned Features

- Snippet templates
- Code snippet snippets with variable placeholders
- Drag & drop support
- Keyboard shortcuts customization
- Cloud sync support
- Plugin system
- Multiple language support (i18n)

### Future Enhancements

- Performance optimizations for large databases (1000+ snippets)
- Advanced search filters (date, usage count, etc.)
- Snippet sharing via URL
- Browser extension integration
- Mobile app companion

---

## Version History

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality (backwards-compatible)
- **PATCH** version: Bug fixes (backwards-compatible)

### Release Process

1. All tests must pass
2. Update CHANGELOG.md
3. Update version in main.py
4. Create git tag: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`
6. Build executables
7. Create GitHub release

---

## Migration Guide

### From v0.x to v1.0.0

This is the first stable release. If you were using development versions:

1. **Backup your data**:
   ```bash
   cp data/snippets.db data/snippets.db.backup
   ```

2. **Update configuration**:
   - Old config format is no longer supported
   - Delete old `config/settings.json`
   - New config will be auto-generated on first run

3. **Re-import snippets** (if needed):
   - Export from old version: Settings → Export → JSON
   - Import to new version: Settings → Import → Select file

---

## Contributors

- **Sekine53629** - Initial development and implementation

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: 2025-10-15
