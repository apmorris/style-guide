import os
import re
import urllib

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from pandas import DataFrame


def _remove_links_figures_md(text):
    text = re.sub(r"\[.\]\(\S*\)", "", text)
    return re.sub(r"\!\[.*\]\(\S*\)", "", text).strip(" \n")


def _remove_extra_space_after_newline_md(text):
    return re.sub(r"\n ", "\n", text)


def _md(text, **options):
    return MarkdownConverter(**options).convert_soup(
        BeautifulSoup(text, features="lxml")
    )


class StyleGuide:
    def __init__(self):

        self.capi_key = os.environ.get("CAPI_KEY", "test")

    def get_capi_search_results(
        self,
        search_term="Guardian and Observer style guide",
        search_fields=["headline"],
        show_fields=["headline", "body"],
    ):
        url = f'https://content.guardianapis.com/search?q="{urllib.parse.quote(search_term)}"&query-fields={",".join(search_fields)}&show-fields={",".join(show_fields)}&page-size=50&api-key={self.capi_key}'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            raise

        return response.json()

    def get_style_guide_body(self):
        results = self.get_capi_search_results()
        results_dict = [
            {
                "path": res["id"],
                "headline": res["fields"]["headline"],
                "body": res["fields"]["body"],
            }
            for res in results["response"]["results"]
        ]

        style_guide_df = DataFrame(results_dict)
        style_guide_df["body_md"] = (
            style_guide_df["body"]
            .apply(_md)
            .apply(_remove_links_figures_md)
            .apply(_remove_extra_space_after_newline_md)
        )

        return style_guide_df.sort_values(by="headline", ascending=True)

    def create_markdown_style_guide(self, dataframe):
        dataframe["body_md_formatted"] = dataframe.apply(
            lambda row: f'# {row["headline"]}\n\n{row["body_md"]}\n\n', axis=1
        )
        output = dataframe[["body_md_formatted"]].apply("".join, axis=0).iloc[0]

        return output


if __name__ == "__main__":

    sg = StyleGuide()
    results = sg.get_capi_search_results()
    style_df = sg.get_style_guide_body()
    output = sg.create_markdown_style_guide(style_df)

    with open("style_guide.md", "w") as f:
        f.write(output)
