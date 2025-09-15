import random

# Vår träningsdata med upprepade ord
data = "Jag gillar att äta glass på sommaren. Jag gillar att dricka kaffe på morgonen."

words = data.split()

# Skapa träningspar av ord - TUPLE
training_pairs = []
for i in range(len(words) - 1):
    input_word = words[i]
    output_word = words[i+1]
    training_pairs.append((input_word, output_word))
    
model = {}

# Loopa igenom träningsparen för att träna modellen
for input_word, output_word in training_pairs:
    if input_word not in model:
        # Skapa en ny nyckel med ordet och sätt värdet till en ny lista som JUST NU bara innehåller output-ordet
        model[input_word] = [output_word]
    else: 
        # Om inputordet redan finns i modellen, lägg till outputordet i den befintliga listan
        model[input_word].append(output_word)

print(model)

def generate_text(start_word):
    generated_text = [start_word]
    current_word = start_word
    
    while current_word in model:
        # Hämta listan med möjliga nästa ord
        next_word_options = model[current_word]
        
        # Om det finns några alternativ, välj ett slumpmässigt ord
        if next_word_options:
            next_word = random.choice(next_word_options)
            generated_text.append(next_word)
            current_word = next_word
        else:            
            break
            
    return " ".join(generated_text)

generated_sentence = generate_text("Jag")
print(generated_sentence)