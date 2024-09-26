import random
import threading

def train_markov_chain(text):
    transition_table = {}
    words = text.split()
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        if current_word not in transition_table:
            transition_table[current_word] = {}
        if next_word not in transition_table[current_word]:
            transition_table[current_word][next_word] = 0
        transition_table[current_word][next_word] += 1
    return transition_table

def generate_text(transition_table, start_word, length):
    generated_text = [start_word]
    current_word = start_word
    for _ in range(length):
        next_word = get_next_word(transition_table, current_word)
        generated_text.append(next_word)
        current_word = next_word
    return " ".join(generated_text)

def get_next_word(transition_table, current_word):
    possible_words = transition_table.get(current_word, {})
    total_weight = sum(possible_words.values())
    if total_weight == 0:
        return random.choice(list(transition_table.keys()))
    else:
        random_value = random.uniform(0, total_weight)
        cumulative_weight = 0
        for next_word, weight in possible_words.items():
            cumulative_weight += weight
            if cumulative_weight >= random_value:
                return next_word

# Get input filename from user
input_filename = "cano.txt"

#input("Enter the filename of the source text: ")

# Read the text from the file
with open(input_filename, "r", encoding="latin-1") as file:
    text = file.read()

# Create a Markov chain object and train it
transition_table = train_markov_chain(text)

# Get the desired length of the generated text from the user
text_length = int(input("Enter the desired length of the generated text: "))

# Generate text using multithreading
num_threads = 4
threads = []
for _ in range(num_threads):
    start_word = random.choice(list(transition_table.keys()))
    thread = threading.Thread(target=generate_text, args=(transition_table, start_word, text_length))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Output the generated text
start_word = random.choice(list(transition_table.keys()))
print(generate_text(transition_table, start_word, text_length))