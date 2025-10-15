"""Database manager with support for local and shared databases."""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from models.models import Base, Tag, Snippet, TagSnippet, Session as UserSession, SearchIndex
from utils.config import Config, expand_path


class DatabaseManager:
    """Manages local and shared database connections.

    Supports:
    - Local database (read-write): User's personal snippets
    - Shared database (read-only): Headquarters-distributed snippets
    - Hybrid mode: Search across both databases
    """

    def __init__(self, config: Config):
        """Initialize database manager.

        Args:
            config: Application configuration.
        """
        self.config = config
        self.local_engine = None
        self.shared_engine = None
        self.LocalSession = None
        self.SharedSession = None

        self._setup_databases()

    def _setup_databases(self):
        """Set up database engines and session makers."""
        # Local database (always enabled, read-write)
        local_path = expand_path(self.config.database.local.path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        self.local_engine = create_engine(
            f'sqlite:///{local_path}',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
            echo=False  # Set to True for SQL debugging
        )

        # Enable foreign keys for SQLite
        @event.listens_for(self.local_engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        self.LocalSession = sessionmaker(bind=self.local_engine)

        # Create tables if they don't exist
        Base.metadata.create_all(self.local_engine)

        # Shared database (optional, read-only)
        if self.config.database.shared.enabled and self.config.database.shared.path:
            shared_path = expand_path(self.config.database.shared.path)

            if shared_path.exists():
                try:
                    self.shared_engine = create_engine(
                        f'sqlite:///{shared_path}',
                        connect_args={
                            'check_same_thread': False,
                            'uri': True,
                            'mode': 'ro'  # Read-only mode
                        },
                        poolclass=StaticPool,
                        echo=False
                    )
                    self.SharedSession = sessionmaker(bind=self.shared_engine)
                    print(f"✓ Shared database connected: {shared_path}")
                except Exception as e:
                    print(f"⚠ Warning: Could not connect to shared database: {e}")
                    self.shared_engine = None
            else:
                print(f"⚠ Warning: Shared database not found: {shared_path}")

    @contextmanager
    def get_local_session(self) -> Session:
        """Get a local database session (context manager).

        Yields:
            Session: SQLAlchemy session for local database.
        """
        session = self.LocalSession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def get_shared_session(self) -> Optional[Session]:
        """Get a shared database session (context manager).

        Yields:
            Session: SQLAlchemy session for shared database, or None if not available.
        """
        if not self.SharedSession:
            yield None
            return

        session = self.SharedSession()
        try:
            yield session
        finally:
            session.close()

    def get_all_tags(self, include_shared: bool = True) -> List[Dict[str, Any]]:
        """Get all tags from local and optionally shared database.

        Args:
            include_shared: Whether to include tags from shared database.

        Returns:
            List[Dict]: Combined list of tags as dictionaries.
        """
        tags = []

        # Local tags
        with self.get_local_session() as session:
            local_tags = session.query(Tag).order_by(Tag.order, Tag.name).all()
            for tag in local_tags:
                # Build path
                path = [tag.name]
                current = tag.parent
                while current:
                    path.insert(0, current.name)
                    current = current.parent
                full_path = ' > '.join(path)

                tags.append({
                    'id': tag.id,
                    'name': tag.name,
                    'parent_id': tag.parent_id,
                    'type': tag.type,
                    'icon': tag.icon,
                    'color': tag.color,
                    'description': tag.description,
                    'full_path': full_path,
                    'source': 'local'
                })

        # Shared tags (if enabled)
        if include_shared and self.config.database.mode in ['shared', 'hybrid']:
            with self.get_shared_session() as session:
                if session:
                    shared_tags = session.query(Tag).order_by(Tag.order, Tag.name).all()
                    for tag in shared_tags:
                        # Build path
                        path = [tag.name]
                        current = tag.parent
                        while current:
                            path.insert(0, current.name)
                            current = current.parent
                        full_path = ' > '.join(path)

                        tags.append({
                            'id': tag.id,
                            'name': tag.name,
                            'parent_id': tag.parent_id,
                            'type': tag.type,
                            'icon': tag.icon,
                            'color': tag.color,
                            'description': tag.description,
                            'full_path': full_path,
                            'source': 'shared'
                        })

        return tags

    def get_snippets_by_tag(self, tag_id: int, include_shared: bool = True) -> List[Dict[str, Any]]:
        """Get all snippets for a specific tag.

        Args:
            tag_id: Tag ID to filter by.
            include_shared: Whether to include snippets from shared database.

        Returns:
            List[Dict]: List of snippets as dictionaries.
        """
        snippets = []

        # Local snippets
        with self.get_local_session() as session:
            local_snippets = (
                session.query(Snippet)
                .join(TagSnippet)
                .filter(TagSnippet.tag_id == tag_id)
                .order_by(Snippet.name)
                .all()
            )
            for snippet in local_snippets:
                snippets.append({
                    'id': snippet.id,
                    'name': snippet.name,
                    'code': snippet.code,
                    'description': snippet.description,
                    'language': snippet.language,
                    'usage_count': snippet.usage_count,
                    'last_used': snippet.last_used,
                    'source': 'local'
                })

        # Shared snippets (if enabled)
        if include_shared and self.config.database.mode in ['shared', 'hybrid']:
            with self.get_shared_session() as session:
                if session:
                    shared_snippets = (
                        session.query(Snippet)
                        .join(TagSnippet)
                        .filter(TagSnippet.tag_id == tag_id)
                        .order_by(Snippet.name)
                        .all()
                    )
                    for snippet in shared_snippets:
                        snippets.append({
                            'id': snippet.id,
                            'name': snippet.name,
                            'code': snippet.code,
                            'description': snippet.description,
                            'language': snippet.language,
                            'usage_count': snippet.usage_count,
                            'last_used': snippet.last_used,
                            'source': 'shared'
                        })

        return snippets

    def get_all_snippets(self, include_shared: bool = True) -> List[Dict[str, Any]]:
        """Get all snippets from all tags.

        Args:
            include_shared: Whether to include snippets from shared database.

        Returns:
            List[Dict]: List of all snippets as dictionaries.
        """
        snippets = []

        # Local snippets
        with self.get_local_session() as session:
            local_snippets = session.query(Snippet).order_by(Snippet.name).all()
            for snippet in local_snippets:
                snippets.append({
                    'id': snippet.id,
                    'name': snippet.name,
                    'code': snippet.code,
                    'description': snippet.description,
                    'language': snippet.language,
                    'usage_count': snippet.usage_count,
                    'last_used': snippet.last_used,
                    'source': 'local'
                })

        # Shared snippets (if enabled)
        if include_shared and self.config.database.mode in ['shared', 'hybrid']:
            with self.get_shared_session() as session:
                if session:
                    shared_snippets = session.query(Snippet).order_by(Snippet.name).all()
                    for snippet in shared_snippets:
                        snippets.append({
                            'id': snippet.id,
                            'name': snippet.name,
                            'code': snippet.code,
                            'description': snippet.description,
                            'language': snippet.language,
                            'usage_count': snippet.usage_count,
                            'last_used': snippet.last_used,
                            'source': 'shared'
                        })

        return snippets

    def search_snippets(self, query: str, language: Optional[str] = None,
                       include_shared: bool = True) -> List[Dict[str, Any]]:
        """Search snippets by text query.

        Args:
            query: Search query string.
            language: Optional language filter.
            include_shared: Whether to include snippets from shared database.

        Returns:
            List[Dict]: Matching snippets as dictionaries.
        """
        results = []

        # Search local database
        with self.get_local_session() as session:
            q = session.query(Snippet).filter(
                (Snippet.name.ilike(f'%{query}%')) |
                (Snippet.description.ilike(f'%{query}%'))
            )
            if language:
                q = q.filter(Snippet.language == language)

            local_results = q.order_by(Snippet.usage_count.desc()).all()
            for snippet in local_results:
                results.append({
                    'id': snippet.id,
                    'name': snippet.name,
                    'code': snippet.code,
                    'description': snippet.description,
                    'language': snippet.language,
                    'usage_count': snippet.usage_count,
                    'last_used': snippet.last_used,
                    'source': 'local'
                })

        # Search shared database
        if include_shared and self.config.database.mode in ['shared', 'hybrid']:
            with self.get_shared_session() as session:
                if session:
                    q = session.query(Snippet).filter(
                        (Snippet.name.ilike(f'%{query}%')) |
                        (Snippet.description.ilike(f'%{query}%'))
                    )
                    if language:
                        q = q.filter(Snippet.language == language)

                    shared_results = q.order_by(Snippet.usage_count.desc()).all()
                    for snippet in shared_results:
                        results.append({
                            'id': snippet.id,
                            'name': snippet.name,
                            'code': snippet.code,
                            'description': snippet.description,
                            'language': snippet.language,
                            'usage_count': snippet.usage_count,
                            'last_used': snippet.last_used,
                            'source': 'shared'
                        })

        return results

    def add_snippet(self, name: str, code: str, language: Optional[str] = None,
                   description: Optional[str] = None, tag_ids: Optional[List[int]] = None) -> Snippet:
        """Add a new snippet to local database.

        Args:
            name: Snippet name.
            code: Snippet code content.
            language: Programming language.
            description: Optional description.
            tag_ids: Optional list of tag IDs to associate with.

        Returns:
            Snippet: Created snippet object.
        """
        with self.get_local_session() as session:
            snippet = Snippet(
                name=name,
                code=code,
                language=language,
                description=description,
                source='local'
            )
            session.add(snippet)
            session.flush()  # Get the ID

            # Associate with tags
            if tag_ids:
                for tag_id in tag_ids:
                    tag_snippet = TagSnippet(tag_id=tag_id, snippet_id=snippet.id)
                    session.add(tag_snippet)

            session.commit()
            return snippet

    def update_snippet(self, snippet_id: int, **kwargs) -> bool:
        """Update a snippet in local database.

        Args:
            snippet_id: Snippet ID to update.
            **kwargs: Fields to update (name, code, description, language).

        Returns:
            bool: True if successful, False if snippet not found or is shared.
        """
        with self.get_local_session() as session:
            snippet = session.query(Snippet).filter(Snippet.id == snippet_id).first()

            if not snippet:
                return False

            if snippet.source == 'shared':
                print("⚠ Cannot modify shared snippets")
                return False

            # Update fields
            for key, value in kwargs.items():
                if hasattr(snippet, key):
                    setattr(snippet, key, value)

            session.commit()
            return True

    def delete_snippet(self, snippet_id: int) -> bool:
        """Delete a snippet from local database.

        Args:
            snippet_id: Snippet ID to delete.

        Returns:
            bool: True if successful, False if snippet not found or is shared.
        """
        with self.get_local_session() as session:
            snippet = session.query(Snippet).filter(Snippet.id == snippet_id).first()

            if not snippet:
                return False

            if snippet.source == 'shared':
                print("⚠ Cannot delete shared snippets")
                return False

            session.delete(snippet)
            session.commit()
            return True

    def toggle_favorite(self, snippet_id: int) -> bool:
        """Toggle favorite status of a snippet.

        Args:
            snippet_id: Snippet ID to toggle.

        Returns:
            bool: New favorite status (True if now favorite, False if not).
        """
        with self.get_local_session() as session:
            snippet = session.query(Snippet).filter(Snippet.id == snippet_id).first()

            if not snippet:
                return False

            # Toggle favorite status
            snippet.is_favorite = not snippet.is_favorite
            session.commit()
            return snippet.is_favorite

    def get_favorite_snippets(self) -> List[Dict[str, Any]]:
        """Get all favorite snippets.

        Returns:
            List[Dict]: List of favorite snippets as dictionaries.
        """
        favorites = []

        with self.get_local_session() as session:
            fav_snippets = (
                session.query(Snippet)
                .filter(Snippet.is_favorite == True)
                .order_by(Snippet.usage_count.desc(), Snippet.name)
                .all()
            )

            for snippet in fav_snippets:
                favorites.append({
                    'id': snippet.id,
                    'name': snippet.name,
                    'code': snippet.code,
                    'description': snippet.description,
                    'language': snippet.language,
                    'usage_count': snippet.usage_count,
                    'last_used': snippet.last_used,
                    'is_favorite': snippet.is_favorite,
                    'source': snippet.source
                })

        return favorites

    def get_or_create_tag(self, name: str, parent_id: Optional[int] = None,
                         tag_type: str = 'folder') -> int:
        """Get existing tag or create new one.

        Args:
            name: Tag name.
            parent_id: Optional parent tag ID.
            tag_type: Tag type ('folder', 'snippet', 'both').

        Returns:
            int: Tag ID (existing or newly created).
        """
        with self.get_local_session() as session:
            # Try to find existing tag
            tag = session.query(Tag).filter(
                Tag.name == name,
                Tag.parent_id == parent_id
            ).first()

            if tag:
                return tag.id

            # Create new tag
            tag = Tag(name=name, parent_id=parent_id, type=tag_type)
            session.add(tag)
            session.flush()  # Get the ID
            tag_id = tag.id
            session.commit()
            return tag_id

    def close(self):
        """Close all database connections."""
        if self.local_engine:
            self.local_engine.dispose()
        if self.shared_engine:
            self.shared_engine.dispose()
