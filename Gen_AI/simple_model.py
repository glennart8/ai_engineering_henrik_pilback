data = "Jag gillar att äta glass på sommaren"

words = data.split()

print(words)

training_pairs = []

# Loopa genom words-listan upp till det näst sista ordet
for i in range(len(words) - 1): # -1 för att undvika fel när loopen når sista ordet
    input_word = words[i]
    output_word = words[i+1]
    
    # Skapa paret som en tupel och lägg till
    training_pairs.append((input_word, output_word))
    
print(training_pairs)

model = {}

# uppackningsfunktion, tuple unpacking
for input_word, output_word in training_pairs:
    model[input_word] = output_word

print(model)

def generate_text(start_word):
    generated_text = [start_word]
    current_word = start_word
    
    # Om current_word (från början start_ordet) finns i dicten model
    while current_word in model:
        next_word = model[current_word] #Letar upp nyckeln "Jag" i första omgång, och tilldelar värdet till den nyckeln automatiskt
        generated_text.append(next_word)
        current_word = next_word
        
    return " ".join(generated_text)
        
generate_sentence = generate_text("Jag")
print(generate_sentence)
