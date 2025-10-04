"""Sample articles for offline testing.

This module defines a small dataset of news articles across five categories:
Greece, Netherlands, Data Science, AI and Finance.  When network access is not
available, the pipeline can load these articles instead of fetching from
external RSS feeds.  The publication times are generated relative to the
current UTC time so that recency scoring behaves sensibly when the pipeline is
run.
"""

from datetime import datetime, timedelta
from typing import List, Dict
from .datatypes import Article


def _now() -> datetime:
    return datetime.utcnow()


def _rel(hours: float) -> datetime:
    """Utility to produce a timestamp relative to now.

    Negative values produce times in the past.
    """
    return _now() + timedelta(hours=hours)


def load_sample_articles() -> List[Article]:
    """Return a list of sample articles covering multiple categories.

    Each article is constructed with a headline, link, description, publisher,
    category and a publication time relative to when this function is called.
    """
    articles: List[Article] = []

    # Greece
    articles.extend([
        Article(
            title="Greek parliament passes budget for 2025",
            link="https://news.example.com/greece/budget-2025",
            description="The Greek parliament has approved the 2025 budget, focusing on investment and social spending.",
            published=_rel(-2),
            publisher="Kathimerini",
            category="Greece",
        ),
        Article(
            title="Wildfires hit Greek islands again",
            link="https://news.example.com/greece/wildfires-islands",
            description="Several islands in Greece are battling wildfires as high temperatures and strong winds persist.",
            published=_rel(-10),
            publisher="Ekathimerini",
            category="Greece",
        ),
        Article(
            title="Greece's tourism numbers reach record high",
            link="https://news.example.com/greece/tourism-record",
            description="Tourism arrivals in Greece have surged, recording the highest numbers seen in the last decade.",
            published=_rel(-20),
            publisher="ERT",
            category="Greece",
        ),
        Article(
            title="Greece and Turkey discuss maritime dispute",
            link="https://news.example.com/greece/turkey-maritime-dispute",
            description="Greek and Turkish officials met to de‑escalate tensions over contested maritime borders in the Aegean Sea.",
            published=_rel(-5),
            publisher="AMNA",
            category="Greece",
        ),
        Article(
            title="Greek stock market leaps after EU funds release",
            link="https://news.example.com/greece/market-leap",
            description="Athens stock exchange rallied after the European Union released structural funds to Greece.",
            published=_rel(-8),
            publisher="Capital.gr",
            category="Greece",
        ),
    ])

    # Netherlands
    articles.extend([
        Article(
            title="Dutch government announces tax reform",
            link="https://news.example.com/netherlands/tax-reform",
            description="The Dutch government unveiled a sweeping tax reform aimed at simplifying the tax code and stimulating growth.",
            published=_rel(-3),
            publisher="NOS",
            category="Netherlands",
        ),
        Article(
            title="Amsterdam housing crisis intensifies",
            link="https://news.example.com/netherlands/housing-crisis",
            description="Housing shortages and rising rent prices are exacerbating the housing crisis in Amsterdam.",
            published=_rel(-12),
            publisher="NRC",
            category="Netherlands",
        ),
        Article(
            title="Netherlands leads in electric vehicle adoption",
            link="https://news.example.com/netherlands/ev-adoption",
            description="New data shows the Netherlands has one of the highest per‑capita rates of electric vehicle ownership in Europe.",
            published=_rel(-18),
            publisher="de Volkskrant",
            category="Netherlands",
        ),
        Article(
            title="Dutch scientists discover new particle",
            link="https://news.example.com/netherlands/science-discovery",
            description="Researchers at a Dutch university claim to have discovered a previously unknown subatomic particle.",
            published=_rel(-6),
            publisher="RTL Nieuws",
            category="Netherlands",
        ),
        Article(
            title="Floods in Rotterdam prompt emergency response",
            link="https://news.example.com/netherlands/floods-rotterdam",
            description="Heavy rains have caused flooding in parts of Rotterdam, leading authorities to declare a state of emergency.",
            published=_rel(-15),
            publisher="Trouw",
            category="Netherlands",
        ),
    ])

    # Data Science
    articles.extend([
        Article(
            title="New open source dataset released by Kaggle",
            link="https://news.example.com/datascience/kaggle-dataset",
            description="Kaggle has released a large open source dataset for machine learning practitioners, featuring millions of records.",
            published=_rel(-4),
            publisher="O'Reilly Radar",
            category="Data Science",
        ),
        Article(
            title="Researchers propose novel data balancing method",
            link="https://news.example.com/datascience/balancing-method",
            description="A new technique for balancing imbalanced datasets has been proposed by data scientists, promising improved model accuracy.",
            published=_rel(-9),
            publisher="ACM Communications",
            category="Data Science",
        ),
        Article(
            title="Company uses data science to reduce carbon footprint",
            link="https://news.example.com/datascience/carbon-footprint",
            description="An international corporation reports a 20% drop in emissions after leveraging data science to optimise logistics.",
            published=_rel(-14),
            publisher="Nature News",
            category="Data Science",
        ),
        Article(
            title="Top 10 Data Science trends for 2025",
            link="https://news.example.com/datascience/trends-2025",
            description="Experts discuss the most significant trends set to shape data science in 2025, including causal inference and generative models.",
            published=_rel(-1),
            publisher="MIT Tech Review",
            category="Data Science",
        ),
        Article(
            title="Conference on Responsible AI emphasises fairness metrics",
            link="https://news.example.com/datascience/responsible-ai",
            description="At a major data science conference, speakers stressed the importance of fairness and transparency in AI models.",
            published=_rel(-22),
            publisher="Papers with Code",
            category="Data Science",
        ),
    ])

    # AI
    articles.extend([
        Article(
            title="OpenAI releases GPT‑5",
            link="https://news.example.com/ai/openai-gpt5",
            description="OpenAI has announced the release of GPT‑5, the latest version of its large language model, touting significant improvements.",
            published=_rel(-3.5),
            publisher="OpenAI Blog",
            category="AI",
        ),
        Article(
            title="Researchers debate AI safety regulations",
            link="https://news.example.com/ai/ai-safety-regulations",
            description="Leading AI experts gathered to debate the need for stricter regulations to ensure the safe development of artificial intelligence.",
            published=_rel(-11),
            publisher="DeepMind Blog",
            category="AI",
        ),
        Article(
            title="AI system achieves state‑of‑the‑art on summarisation",
            link="https://news.example.com/ai/ai-summarisation",
            description="A new AI system has achieved state‑of‑the‑art performance on summarisation benchmarks, outpacing existing models.",
            published=_rel(-7),
            publisher="Anthropic Blog",
            category="AI",
        ),
        Article(
            title="Anthropic announces new AI assistant",
            link="https://news.example.com/ai/anthropic-assistant",
            description="Anthropic has unveiled a new AI assistant designed to offer more personalised and safe interactions.",
            published=_rel(-18),
            publisher="Anthropic Blog",
            category="AI",
        ),
        Article(
            title="EU proposes AI Act enforcement guidelines",
            link="https://news.example.com/ai/eu-ai-act",
            description="The European Union has proposed guidelines for enforcing the upcoming AI Act, addressing transparency and accountability.",
            published=_rel(-16),
            publisher="EU Commission",
            category="AI",
        ),
    ])

    # Finance
    articles.extend([
        Article(
            title="European Central Bank raises interest rates",
            link="https://news.example.com/finance/ecb-rates",
            description="The ECB has increased interest rates by 0.25 percentage points in response to rising inflation.",
            published=_rel(-2.5),
            publisher="Reuters",
            category="Finance",
        ),
        Article(
            title="NASDAQ hits record high",
            link="https://news.example.com/finance/nasdaq-record",
            description="Technology shares surged on Monday, pushing the NASDAQ composite to an all‑time high.",
            published=_rel(-8.5),
            publisher="CNBC",
            category="Finance",
        ),
        Article(
            title="Bitcoin surpasses $100k",
            link="https://news.example.com/finance/bitcoin-100k",
            description="Bitcoin's price crossed the $100,000 mark for the first time, buoyed by institutional interest and ETF approvals.",
            published=_rel(-6.5),
            publisher="CryptoTimes",
            category="Finance",
        ),
        Article(
            title="Economic slowdown predicted in Asia",
            link="https://news.example.com/finance/asia-slowdown",
            description="Analysts warn that several Asian economies may face a slowdown due to geopolitical tensions and supply chain issues.",
            published=_rel(-12.5),
            publisher="Bloomberg",
            category="Finance",
        ),
        Article(
            title="Startups raise billions in fintech funding",
            link="https://news.example.com/finance/fintech-funding",
            description="Fintech startups worldwide raised more than $5 billion in venture capital funding in the last quarter.",
            published=_rel(-21),
            publisher="TechCrunch",
            category="Finance",
        ),
    ])

    return articles
