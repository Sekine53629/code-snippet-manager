"""
Fuzzy search utility for code snippet matching.

Provides fuzzy string matching to find snippets even with typos or
partial matches. Uses simple character-based scoring algorithm.
"""

from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher


def calculate_fuzzy_score(query: str, text: str, case_sensitive: bool = False) -> float:
    """
    Calculate fuzzy match score between query and text.

    Args:
        query: Search query string
        text: Text to match against
        case_sensitive: Whether to perform case-sensitive matching

    Returns:
        Score between 0.0 (no match) and 1.0 (perfect match)
    """
    if not query:
        return 1.0

    if not text:
        return 0.0

    # Normalize case if needed
    if not case_sensitive:
        query = query.lower()
        text = text.lower()

    # Exact match gets highest score
    if query == text:
        return 1.0

    # Check if query is substring
    if query in text:
        # Score based on how much of the text matches
        return 0.8 + (0.2 * len(query) / len(text))

    # Use SequenceMatcher for fuzzy matching
    matcher = SequenceMatcher(None, query, text)
    return matcher.ratio()


def calculate_snippet_score(query: str, snippet: Dict[str, Any]) -> float:
    """
    Calculate relevance score for a snippet against a query.

    Searches in name, code, description, and language fields.
    Different fields have different weights.

    Args:
        query: Search query string
        snippet: Snippet dictionary with name, code, description, language

    Returns:
        Combined relevance score (0.0 to 1.0)
    """
    if not query:
        return 1.0

    # Field weights (total = 1.0)
    WEIGHTS = {
        'name': 0.4,      # Name is most important
        'code': 0.3,      # Code content is important
        'description': 0.2,  # Description is helpful
        'language': 0.1,  # Language is least important
    }

    # Calculate scores for each field
    name_score = calculate_fuzzy_score(query, snippet.get('name', ''))
    code_score = calculate_fuzzy_score(query, snippet.get('code', ''))
    description_score = calculate_fuzzy_score(query, snippet.get('description', ''))
    language_score = calculate_fuzzy_score(query, snippet.get('language', ''))

    # Weighted combination
    total_score = (
        name_score * WEIGHTS['name'] +
        code_score * WEIGHTS['code'] +
        description_score * WEIGHTS['description'] +
        language_score * WEIGHTS['language']
    )

    return total_score


def fuzzy_search_snippets(
    query: str,
    snippets: List[Dict[str, Any]],
    threshold: float = 0.3,
    max_results: int = 50
) -> List[Tuple[Dict[str, Any], float]]:
    """
    Search snippets using fuzzy matching.

    Args:
        query: Search query string
        snippets: List of snippet dictionaries
        threshold: Minimum score to include in results (0.0 to 1.0)
        max_results: Maximum number of results to return

    Returns:
        List of (snippet, score) tuples, sorted by score descending
    """
    if not query:
        # Return all snippets with score 1.0
        return [(snippet, 1.0) for snippet in snippets[:max_results]]

    # Calculate scores for all snippets
    scored_snippets = []
    for snippet in snippets:
        score = calculate_snippet_score(query, snippet)
        if score >= threshold:
            scored_snippets.append((snippet, score))

    # Sort by score descending
    scored_snippets.sort(key=lambda x: x[1], reverse=True)

    # Return top results
    return scored_snippets[:max_results]


def calculate_tag_score(query: str, tag: Dict[str, Any]) -> float:
    """
    Calculate relevance score for a tag against a query.

    Args:
        query: Search query string
        tag: Tag dictionary with name, description

    Returns:
        Relevance score (0.0 to 1.0)
    """
    if not query:
        return 1.0

    # Tag name is more important than description
    name_score = calculate_fuzzy_score(query, tag.get('name', ''))
    description_score = calculate_fuzzy_score(query, tag.get('description', ''))

    # 70% name, 30% description
    return name_score * 0.7 + description_score * 0.3


def fuzzy_search_tags(
    query: str,
    tags: List[Dict[str, Any]],
    threshold: float = 0.3,
    max_results: int = 20
) -> List[Tuple[Dict[str, Any], float]]:
    """
    Search tags using fuzzy matching.

    Args:
        query: Search query string
        tags: List of tag dictionaries
        threshold: Minimum score to include in results (0.0 to 1.0)
        max_results: Maximum number of results to return

    Returns:
        List of (tag, score) tuples, sorted by score descending
    """
    if not query:
        return [(tag, 1.0) for tag in tags[:max_results]]

    # Calculate scores for all tags
    scored_tags = []
    for tag in tags:
        score = calculate_tag_score(query, tag)
        if score >= threshold:
            scored_tags.append((tag, score))

    # Sort by score descending
    scored_tags.sort(key=lambda x: x[1], reverse=True)

    # Return top results
    return scored_tags[:max_results]


def highlight_matches(query: str, text: str, case_sensitive: bool = False) -> List[Tuple[int, int]]:
    """
    Find positions of matching characters in text for highlighting.

    Args:
        query: Search query string
        text: Text to search in
        case_sensitive: Whether to perform case-sensitive matching

    Returns:
        List of (start, end) position tuples for matches
    """
    if not query or not text:
        return []

    # Normalize case if needed
    search_query = query if case_sensitive else query.lower()
    search_text = text if case_sensitive else text.lower()

    matches = []

    # Find all occurrences of query as substring
    start = 0
    while True:
        pos = search_text.find(search_query, start)
        if pos == -1:
            break
        matches.append((pos, pos + len(query)))
        start = pos + 1

    return matches
