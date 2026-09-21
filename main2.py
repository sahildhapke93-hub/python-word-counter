
import re
from collections import Counter

def analyze_text(text):
    """Analyze input text and return a dictionary of statistical metrics."""
    if not text.strip():
        return None


    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)

    char_count_with_spaces = len(text)
    char_count_no_spaces = len(re.sub(r'\s+', '', text))

    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = len(sentences) if sentences else (1 if word_count > 0 else 0)

    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    paragraph_count = len(paragraphs)

    avg_word_length = (sum(len(w) for w in words) / word_count) if word_count > 0 else 0

    word_counts = Counter(w.lower() for w in words)
    top_words = word_counts.most_common(3)

    return {
        "words": word_count,
        "chars_with_spaces": char_count_with_spaces,
        "chars_no_spaces": char_count_no_spaces,
        "sentences": sentence_count,
        "paragraphs": paragraph_count,
        "avg_word_length": avg_word_length,
        "top_words": top_words
    }

def get_user_text():
    """Collect multi-line text input from the user."""
    print("\n  👉 Enter or paste your text below.")
    print("     (Press ENTER twice or type 'END' on a new line to finish):")
    print("  " + "-" * 44)

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
            if len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
                break
        except EOFError:
            break

    return "\n".join(lines).strip()

def display_report(stats):
    """Print a clean, formatted analysis report."""
    print("\n" + "=" * 48)
    print("         📊 TEXT ANALYSIS REPORT 📊         ")
    print("=" * 48)

    if not stats:
        print("  ⚠️  No text was provided to analyze.\n")
        return

    print(f"  • Total Words:             {stats['words']}")
    print(f"  • Total Characters (w/):   {stats['chars_with_spaces']}")
    print(f"  • Total Characters (w/o):  {stats['chars_no_spaces']}")
    print(f"  • Total Sentences:         {stats['sentences']}")
    print(f"  • Total Paragraphs:        {stats['paragraphs']}")
    print(f"  • Average Word Length:     {stats['avg_word_length']:.2f} chars")

    if stats['top_words']:
        print("\n  🔥 Most Frequent Words:")
        for word, count in stats['top_words']:
            print(f"     - '{word}': {count} time(s)")

    print("=" * 48 + "\n")

def main():
    print("=" * 48)
    print("        📝 WORD & TEXT COUNTER TOOL 📝      ")
    print("             Course Code: CM25048           ")
    print("=" * 48)

    user_text = get_user_text()
    stats = analyze_text(user_text)
    display_report(stats)

if __name__ == "__main__":
    main()
