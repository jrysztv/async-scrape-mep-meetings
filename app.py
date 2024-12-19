# %%
from mep_meetings.scraper.scraper import EuroparlMeetingFetcher
from mep_meetings.scraper.utils import extract_articles_to_dataframe
import streamlit as st
import asyncio
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide")


async def scrape_meetings(url: str, pages: int):
    fetcher = EuroparlMeetingFetcher(url)
    await fetcher.run_async(pages=pages)
    return fetcher.articles


def convert_df_to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    return output.getvalue()


st.title("MEP Meetings Scraper")

# Create two columns
col1, col2 = st.columns([1, 3])

with col1:
    url = st.text_input(
        "Enter the URL of the past meetings page of the MEP:",
        value="https://www.europarl.europa.eu/meps/en/256864/ANDRAS+TIVADAR_KULJA/meetings/past?meetingType=PAST&memberId=156789&termId=10&page=1&pageSize=10",
    )
    pages = st.number_input(
        'How many times would you have to click "Load more"?',
        min_value=1,
        max_value=100,
        value=50,
    )
    scrape_button = st.button("Scrape Meetings")

if scrape_button and url:
    with st.spinner("Scraping..."):
        articles = asyncio.run(scrape_meetings(url, pages))
        df = extract_articles_to_dataframe(articles)
        st.success("Scraping completed!")

        with col2:
            st.dataframe(
                df,
                column_order=[
                    "Title",
                    "Date",
                    "Place",
                    "Meeting with",
                    "Capacity",
                    "Code of associated committee or delegation",
                    "page_number",
                ],
            )

            excel_data = convert_df_to_excel(df)
        with col1:
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="mep_meetings.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
