#BasicCode
def word_counter():
    print("--- WORD COUNTER ---")
    text = input("Enter your text:\n")
    
    if not text.strip():
        print("Empty text entered!")
        return


    char_count = len(text)

    words = text.lower().split()
    total_words = len(words)


    unique_words = set(words)
    unique_words_count = len(unique_words)


    freq = {}
    for w in words:

        w = w.strip(".,!?;:")
        freq[w] = freq.get(w, 0) + 1


    print("\n--- RESULTS ---")
    print("Total Characters :", char_count)
    print("Total Words      :", total_words)
    print("Unique Words     :", unique_words_count)
    print("\nWord Frequencies:")
    for word, count in freq.items():
        print(f"  {word}: {count}")

if __name__ == "__main__":
    word_counter()
