import pandas as pd
from typing import Dict, List, Optional


def extract_articles_to_dataframe(
    articles: List[Optional[Dict[str, Optional[str]]]],
) -> pd.DataFrame:
    """
    Extracts articles into a pandas DataFrame.

    :param articles: List of dictionaries containing article data.
    :return: A pandas DataFrame with the article data.
    """

    # print(pd.DataFrame.from_dict(articles, orient="index"))
    # Filter out None values from articles
    articles = [article for article in articles if article is not None]

    # Convert list of dictionaries to DataFrame
    return pd.DataFrame(articles)
