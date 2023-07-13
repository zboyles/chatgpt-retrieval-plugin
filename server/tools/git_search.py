from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple
import tempfile
import asyncio


# from langchain.tools.playwright import Playwright

from git import Repo

test_url = "https://github.com/solidjs/solid-start"
default_vector: Tuple[str, str] = ("https://github.com/junegunn/fzf/blob/master/doc/fzf.txt", "fzf.txt")

# List[repo_url, page_name]
vector_db: List[Tuple[str, str]] = [default_vector]
error_db: List[Tuple[str, str]] = []

class GitSearch(ABC):
    
    async def list(self, include_files: Optional[bool] = False) -> List[str] | List[Tuple[str, str]]:
        """
        Lists all git repositories that were indexed.
        
        Returns:
            A list of git repository URLs.
            
        Args:
            include_files (Optional[bool]): Whether to include the files in the returned list.
        """
        if include_files:
            return [(url[0], url[1]) for url in vector_db]
        return [url[0] for url in vector_db]
    
    async def add(self, urls: str | List[str], filter: Optional[str] = None) -> int:
        """
        Indexes the files from one or more git repositories after applying an optional filter.
        
        Args:
            urls (str | List[str]): The URL of the git repository to add.
            filter (Optional[str]): An optional filter to apply to any repository URLs to be indexed.
        """
        if isinstance(urls, str):
            urls = [urls]

        print(f"{len(urls)} URLs: {urls}")
        total_files = 0
        for url in urls:
            print(f"URL: {url}")
            if not url or url.isspace():
                print(f"URL is empty or whitespace: {url}")
                error_db.append((url, "URL is empty or whitespace."))
        
            with tempfile.TemporaryDirectory() as tmp:
                print(f"Created temporary directory: {tmp}")
                try:
                    repo = Repo.clone_from(url, to_path=tmp)
                    tmprepo = Path(tmp)
                    print(f"is_dir: {tmprepo.is_dir()}; is_file: {tmprepo.is_file()};")
                    i = 0
                    if tmprepo.is_dir():
                        for _file in tmprepo.rglob(filter or "*/*"):
                            vector_db.append((url, _file.name))
                            i += 1
                    print(f"Found {i} files in {url}")
                    total_files += i
                except Exception as e:
                    print(e)
                    error_db.append((url, str(e)))
                    continue
        print(f"Total files: {total_files}")
        return total_files


    async def reset_db(self) -> bool:
        """
        Resets the database of git repositories.
        """
        try:
            vector_db.clear()
            vector_db.append(default_vector)
            error_db.clear()
        except Exception as e:
            print(e)
            return False
        return True

    
    # async def remove(self, urls: str | List[str]):
    #     """
    #     Removes a git repository from the list of repositories to search.
        
    #     Args:
    #         urls (str | List[str]): The URL of the git repository to remove.
    #     """
    #     if isinstance(urls, str):
    #         urls = [urls]
        
    #     for url in urls:
    #         if not url or url.isspace:
    #             vector_db.remove(url)
    
    # async def search(self, query: str, limit: int = 10):
    #     """
    #     Searches all git repositories for files matching the given query.
        
    #     Args:
    #         query (str): The query to search for in the repository.
    #         limit (int): The maximum number of files to return.
        
    #     Returns:
    #         A list of file names matching the query, up to the given limit.
    #     """
    #     if not query or query.isspace():
    #         return []
        
    #     results = []
        
    #     for url in vector_db:
    #         results.append(await GitSearch.git_search(url, query, limit))
        
    #     return results
    
    # async def git_search(self, url: str, query: Optional[str], limit: int = 10):
    #     """
    #     Clones a git repository from the given URL and searches for files matching the given query.
        
    #     Args:
    #         url (str): The URL of the git repository to clone.
    #         query (Optional[str]): The query to search for in the repository. If None, all files will be searched.
    #         limit (int): The maximum number of files to return.
        
    #     Returns:
    #         A list of file names matching the query, up to the given limit.
    #     """
    #     if not url or url.isspace():
    #         return []
        
    #     if not query or query.isspace():
    #         return []
        
    #     with tempfile.TemporaryDirectory as tmp:
    #         print(f"Created temporary directory: {tmp}")
    #         repo = Repo.clone_from(url, tmp)
    #         tmprepo = Path(tmp)
    #         files = tmprepo.glob(query or "*/*")
    #         file_names = [Path(_file).name for _file in enumerate(files)]
    #         count = len(list(file_names))
    #         print(f"Found {count} file_names")
    #         count = len(list(files))
    #         print(f"Found {count} files in {url}")
    #         print(f"Deleting temporary directory: {tmp}")
    #         return file_names[:limit]

    

