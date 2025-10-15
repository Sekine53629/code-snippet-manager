"""SQLAlchemy database models."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Tag(Base):
    """Hierarchical tag model for organizing snippets.

    Tags can be:
    - 'folder': Container only (e.g., 'Python', 'JavaScript')
    - 'snippet': Leaf node with code (e.g., specific function)
    - 'both': Can contain children AND have code
    """
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('tags.id'), nullable=True)
    type = Column(String(20), nullable=False, default='folder')  # 'folder', 'snippet', 'both'
    icon = Column(String(50), default='📁')
    color = Column(String(7), default='#64B5F6')
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = relationship('Tag', remote_side=[id], backref='children')
    snippets = relationship('TagSnippet', back_populates='tag', cascade='all, delete-orphan')

    # Indexes for performance
    __table_args__ = (
        Index('idx_tag_parent_id', 'parent_id'),
        Index('idx_tag_name', 'name'),
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', type='{self.type}')>"

    @property
    def full_path(self) -> str:
        """Get the full hierarchical path of this tag."""
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return ' > '.join(path)


class Snippet(Base):
    """Code snippet model.

    Stores actual code content with metadata like language,
    description, and usage statistics.
    """
    __tablename__ = 'snippets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    language = Column(String(50), nullable=True)  # 'python', 'javascript', etc.

    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)

    # Metadata
    source = Column(String(20), default='local')  # 'local' or 'shared' (headquarters)
    is_favorite = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tags = relationship('TagSnippet', back_populates='snippet', cascade='all, delete-orphan')

    # Indexes
    __table_args__ = (
        Index('idx_snippet_language', 'language'),
        Index('idx_snippet_name', 'name'),
        Index('idx_snippet_usage', 'usage_count'),
    )

    def __repr__(self):
        return f"<Snippet(id={self.id}, name='{self.name}', language='{self.language}')>"

    def increment_usage(self):
        """Increment usage counter and update last_used timestamp."""
        self.usage_count += 1
        self.last_used = datetime.utcnow()


class TagSnippet(Base):
    """Many-to-many relationship between Tags and Snippets.

    A snippet can belong to multiple tags, and a tag can contain
    multiple snippets.
    """
    __tablename__ = 'tag_snippets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tag = relationship('Tag', back_populates='snippets')
    snippet = relationship('Snippet', back_populates='tags')

    # Indexes
    __table_args__ = (
        Index('idx_tagsnippet_tag_id', 'tag_id'),
        Index('idx_tagsnippet_snippet_id', 'snippet_id'),
    )

    def __repr__(self):
        return f"<TagSnippet(tag_id={self.tag_id}, snippet_id={self.snippet_id})>"


class Session(Base):
    """User session model for remembering UI state.

    Stores the last viewed hierarchy position, expanded folders,
    scroll position, etc. for seamless UX.
    """
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Last state
    last_tag_id = Column(Integer, ForeignKey('tags.id'), nullable=True)
    last_snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=True)

    # UI state (stored as JSON-like string)
    expanded_tags = Column(Text, nullable=True)  # Comma-separated tag IDs
    scroll_position = Column(Integer, default=0)

    # Window state
    window_width = Column(Integer, default=350)
    window_position = Column(String(10), default='right')  # 'right' or 'left'

    last_accessed = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Session(id={self.id}, last_tag_id={self.last_tag_id})>"


class SearchIndex(Base):
    """Full-text search index for snippets.

    Uses FTS5 for efficient searching across snippet names,
    descriptions, and code content.
    """
    __tablename__ = 'search_index'

    id = Column(Integer, primary_key=True, autoincrement=True)
    snippet_id = Column(Integer, ForeignKey('snippets.id'), nullable=False)

    # Searchable content
    content = Column(Text, nullable=False)  # Combined: name + description + code

    # Metadata for filtering
    language = Column(String(50), nullable=True)
    tags = Column(Text, nullable=True)  # Comma-separated tag names

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Indexes
    __table_args__ = (
        Index('idx_searchindex_snippet_id', 'snippet_id'),
        Index('idx_searchindex_language', 'language'),
    )

    def __repr__(self):
        return f"<SearchIndex(snippet_id={self.snippet_id})>"
