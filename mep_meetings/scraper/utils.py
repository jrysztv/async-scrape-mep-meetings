import pandas as pd
from typing import Dict, List, Optional


def extract_articles_to_dataframe(
    articles: List[Optional[Dict[str, List[Optional[str]]]]],
) -> pd.DataFrame:
    """
    Extracts articles into a pandas DataFrame.

    :param articles: List of dictionaries containing article data.
    :return: A pandas DataFrame with the article data.
    """
    if not articles:
        return pd.DataFrame()

    # Filter out None values from articles
    articles = [article for article in articles if article is not None]

    if not articles:
        return pd.DataFrame()

    # Initialize flattened_articles with all possible keys
    all_keys = set()
    for article in articles:
        all_keys.update(article.keys())

    flattened_articles = {key: [] for key in all_keys}

    for article in articles:
        for key in all_keys:
            values = article.get(key, [])
            flattened_articles[key].extend(values)

    return pd.DataFrame(flattened_articles)
