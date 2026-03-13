#!/usr/bin/env python3
"""
Generate sample corpus for hybrid search evaluation.
Creates 300+ documents on AI/ML/search topics.
"""

import os
import random
from pathlib import Path

# Sample content templates
TOPICS = {
    "machine_learning": [
        "Machine learning algorithms transform data into predictions.",
        "Supervised learning uses labeled data to train models.",
        "Unsupervised learning finds patterns in unlabeled data.",
        "Neural networks consist of interconnected nodes called neurons.",
        "Deep learning uses multiple layers of neural networks.",
        "Gradient descent optimizes model parameters during training.",
        "Overfitting occurs when a model learns noise instead of patterns.",
        "Cross-validation helps evaluate model performance on unseen data.",
        "Feature engineering creates meaningful input features for models.",
        "Regularization prevents overfitting by adding penalty terms.",
    ],
    "artificial_intelligence": [
        "Artificial intelligence enables machines to perform human-like tasks.",
        "Natural language processing helps computers understand human language.",
        "Computer vision allows machines to interpret visual information.",
        "Expert systems use knowledge bases to solve complex problems.",
        "Robotics combines AI with mechanical engineering.",
        "Machine reasoning enables logical thinking and problem solving.",
        "Knowledge representation organizes information for AI systems.",
        "Planning algorithms help AI systems achieve goals.",
        "Speech recognition converts audio signals to text.",
        "Image recognition identifies objects and patterns in images.",
    ],
    "search_engines": [
        "Search engines index web pages to provide relevant results.",
        "Web crawling discovers and downloads web pages.",
        "Page ranking algorithms determine result relevance.",
        "Query processing analyzes user search intent.",
        "Information retrieval finds relevant documents from collections.",
        "Relevance ranking orders results by importance.",
        "Search optimization improves visibility in results.",
        "Query expansion adds related terms to improve results.",
        "Personalization tailors results to individual users.",
        "Search analytics measure performance and user behavior.",
    ],
    "data_science": [
        "Data science combines statistics, programming, and domain expertise.",
        "Data cleaning prepares raw data for analysis.",
        "Exploratory data analysis uncovers patterns and insights.",
        "Statistical modeling predicts outcomes from data.",
        "Data visualization communicates findings effectively.",
        "Big data technologies handle large-scale datasets.",
        "Predictive analytics forecasts future trends.",
        "A/B testing compares different approaches statistically.",
        "Data mining discovers hidden patterns in large datasets.",
        "Business intelligence transforms data into actionable insights.",
    ],
    "natural_language_processing": [
        "Tokenization breaks text into meaningful units.",
        "Part-of-speech tagging identifies word types.",
        "Named entity recognition finds proper nouns.",
        "Sentiment analysis determines emotional tone.",
        "Text classification categorizes documents by topic.",
        "Machine translation converts between languages.",
        "Question answering systems respond to queries.",
        "Text summarization creates concise versions of documents.",
        "Language models predict word sequences.",
        "Chatbots provide conversational interfaces.",
    ]
}

def generate_document(topic, doc_id):
    """Generate a single document with random content."""
    topic_sentences = TOPICS[topic]
    num_sentences = random.randint(3, 8)

    # Select random sentences and combine
    selected_sentences = random.sample(topic_sentences, min(num_sentences, len(topic_sentences)))
    content = " ".join(selected_sentences)

    # Add some variation
    variations = [
        f"This article discusses {topic.replace('_', ' ')} in detail.",
        f"Understanding {topic.replace('_', ' ')} is crucial for modern applications.",
        f"The field of {topic.replace('_', ' ')} continues to evolve rapidly.",
        f"Recent advances in {topic.replace('_', ' ')} have opened new possibilities.",
    ]

    intro = random.choice(variations)
    content = f"{intro} {content}"

    return content

def main():
    """Generate sample corpus."""
    raw_dir = Path("data/raw")
    raw_dir.mkdir(exist_ok=True)

    # Generate 350 documents across topics
    topics = list(TOPICS.keys())
    docs_per_topic = 70  # 70 * 5 topics = 350 docs

    doc_id = 1
    for topic in topics:
        for i in range(docs_per_topic):
            content = generate_document(topic, doc_id)

            # Create filename
            filename = "03d"

            # Write to file
            filepath = raw_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            doc_id += 1

    print(f"Generated {doc_id-1} sample documents in {raw_dir}")

if __name__ == "__main__":
    main()