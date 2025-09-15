import random

## DENNA MODELL SKA TA HÄNSYN TILL 2 FÖREGÅENDE ORD I STÄLLET FÖR ENDAST 1

# Vår träningsdata med upprepade ord
text = """
En solig dag gick en katt och en hund på en promenad. 
Hunden sprang fort och jagade sin svans. 
Katten smög tyst bakom buskar och jagade en fjäril. 
Båda djuren var lyckliga över att få vara ute och njuta av det fina vädret. 
Hunden lekte med en boll medan katten solade sig i solen.
"""

text2 = """
Artificiell intelligens, AI, är datorprogram som kan utföra uppgifter som normalt kräver mänsklig intelligens,
såsom problemlösning, mönsterigenkänning, beslutsfattande och språköversättning.
AI kan indelas i smal AI och generell AI. Smal AI, Narrow AI, är konstruerad och tränad för att utföra en specifik uppgift.
Generell AI, AGI, är ett hypotetiskt system som har intellektuella förmågor som kan jämföras med en människa.
Generell AI är än så länge ett forskningsområde. En av de mest lovande och snabbast växande grenarna inom AI är maskininlärning.
Maskininlärning är en metod där datorer lär sig från data istället för att vara explicit programmerade.
Maskininlärning kan i sin tur delas in i underkategorier såsom djupinlärning,
där ett artificiellt neuralt nätverk tränas på stora datamängder för att kunna känna igen mönster.
"""

cleaned_text = text2.replace(".", "").lower()

cleaned_text_words = cleaned_text.split()

# print(cleaned_text_words)

# Skapa träningspar av ord - TUPLE
training_pairs = []
for i in range(len(cleaned_text_words) - 2):
    input_tuple = (cleaned_text_words[i], cleaned_text_words[i+1])
    output_word = cleaned_text_words[i+2]
    
    training_pairs.append((input_tuple, output_word))

# print(training_pairs)  


# --- MODEL ---  
model = {}

# Loopa igenom träningsparen för att träna modellen
for input_tuple, output_word in training_pairs:
    if input_tuple not in model:
        # Skapa en ny nyckel med ordet och sätt värdet till en ny lista som JUST NU bara innehåller output-ordet
        model[input_tuple] = [output_word]
    else: 
        # Om inputordet redan finns i modellen, lägg till outputordet i den befintliga listan
        model[input_tuple].append(output_word)

# print(model)

def generate_text(start_words_tuple):
    generated_text = list(start_words_tuple) 
    current_words = start_words_tuple
    
    while current_words in model:
        next_word_options = model[current_words]
        
        if next_word_options:
            next_word = random.choice(next_word_options)
            generated_text.append(next_word)
            
            current_words = (current_words[1], next_word)
        else:            
            break
            
    return " ".join(generated_text)

generated_sentence = generate_text(('maskininlärning', 'är'))
print(generated_sentence)