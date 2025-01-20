from duckduckgo_search import DDGS
from typing import Optional

class WebSearch:
    """
    A utility class to perform various types of web searches using the DuckDuckGo Search API.
    """
    
    @staticmethod
    def web_search_text(query: str, max_results: Optional[int] = 5) -> list[dict[str, str]]:
        """
        Performs a web search for textual content based on the provided query.
        
        Args:
            query (str): The search query.
            max_results (Optional[int]): Maximum number of results to retrieve. Default is 5.
        
        Returns:
            list[dict[str, str]]: A list of dictionaries containing search result details, 
            such as title, URL, and snippet.
        """
        results = DDGS().text(keywords=query, max_results=max_results)
        return results
    
    @staticmethod
    def web_search_images(query: str, max_results: Optional[int] = 5) -> list[dict[str, str]]:
        """
        Performs a web search for images based on the provided query.
        
        Args:
            query (str): The search query.
            max_results (Optional[int]): Maximum number of results to retrieve. Default is 5.
        
        Returns:
            list[dict[str, str]]: A list of dictionaries containing image result details, 
            such as image URL and associated metadata.
        """
        results = DDGS().images(keywords=query, max_results=max_results)
        return results
    
    @staticmethod
    def web_search_videos(query: str, max_results: Optional[int] = 5) -> list[dict[str, str]]:
        """
        Performs a web search for videos based on the provided query.
        
        Args:
            query (str): The search query.
            max_results (Optional[int]): Maximum number of results to retrieve. Default is 5.
        
        Returns:
            list[dict[str, str]]: A list of dictionaries containing video result details, 
            such as video title, URL, and description.
        """
        results = DDGS().videos(keywords=query, max_results=max_results)
        return results
    
    @staticmethod
    def web_search_news(query: str, max_results: Optional[int] = 5) -> list[dict[str, str]]:
        """
        Performs a web search for news articles based on the provided query.
        
        Args:
            query (str): The search query.
            max_results (Optional[int]): Maximum number of results to retrieve. Default is 5.
        
        Returns:
            list[dict[str, str]]: A list of dictionaries containing news result details, 
            such as headline, URL, and summary.
        """
        results = DDGS().news(keywords=query, max_results=max_results)
        return results
