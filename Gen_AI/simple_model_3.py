import random

## DENNA MODELL SKA TA HÄNSYN TILL 2 FÖREGÅENDE ORD I STÄLLET FÖR ENDAST 1

# Vår träningsdata med upprepade ord
data = "Jag gillar att äta glass på sommaren. Jag gillar att dricka kaffe på morgonen."

words = data.split()

# Skapa träningspar av ord - TUPLE
training_pairs = []
for i in range(len(words) - 2):
    input_tuple = (words[i], words[i+1])
    output_word = words[i+2]
    
    training_pairs.append((input_tuple, output_word))

# print(training_pairs)    
model = {}

# Loopa igenom träningsparen för att träna modellen
for input_tuple, output_word in training_pairs:
    if input_tuple not in model:
        # Skapa en ny nyckel med ordet och sätt värdet till en ny lista som JUST NU bara innehåller output-ordet
        model[input_tuple] = [output_word]
    else: 
        # Om inputordet redan finns i modellen, lägg till outputordet i den befintliga listan
        model[input_tuple].append(output_word)

print(model)

def generate_text(start_words_tuple):
    generated_text = list(start_words_tuple)  # Börja med att lägga till båda orden
    current_words = start_words_tuple
    
    while current_words in model:
        next_word_options = model[current_words]
        
        if next_word_options:
            next_word = random.choice(next_word_options)
            generated_text.append(next_word)
            
            # Skapa en ny tuple med de två senaste orden
            current_words = (current_words[1], next_word)
        else:            
            break
            
    return " ".join(generated_text)

generated_sentence = generate_text(("Jag", "gillar"))
print(generated_sentence)