import numpy as np
import matplotlib.pyplot as plt
import re
import string
import os
import nltk
nltk.download('vader_lexicon')

poem_text="""Thine own heart intertwined with mine, 
under the nacreous clouds, at the shrine.
Oh, your ebony eyes so fine,
have the lords crossed their line?

We rode by the crashing waves at twilight,
on swift hooves and smiles bright.
I wouldnt know, you'd fade into the light,
and turn me to a playwright.

Reminiscing the beautiful days,
as the pines swayed away.
Your joyous soul and warm embrace,
thou bloomed in eternal ways.

Your sweet hand parting mine,
as you graze hands with beings divine.
What I would call a heinous crime!

With our souls tethered,
little did i know, it would be our last ride together."""


from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_poem(text):
    words = re.findall(r'\b\w+\b', text.lower())
    lines = [line for line in text.strip().split('\n') if line.strip()]
    char_count = len(text)
    
    features = {}

    clean_text_chars = ''.join(filter(str.isalpha, text.upper()))
    if clean_text_chars:
        numerical_data = [ord(char) for char in clean_text_chars]
        features['textual_variety'] = np.std(numerical_data)
    else:
        features['textual_variety'] = 0.0

    if words:
        features['lexical_density'] = len(set(words)) / len(words)
    else:
        features['lexical_density'] = 0.0

    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    features['sentiment_compound'] = sentiment_scores['compound']
    features['positivity'] = sentiment_scores['pos']

    if words:
        features['avg_word_length'] = sum(len(w) for w in words) / len(words)
    else:
        features['avg_word_length'] = 0.0
        
    if lines:
        features['avg_line_length'] = len(words) / len(lines)
    else:
        features['avg_line_length'] = 0.0
        
    punc_count = sum(1 for char in text if char in string.punctuation)
    if char_count > 0:
        features['punctuation_density'] = punc_count / char_count
    else:
        features['punctuation_density'] = 0.0

    unique_words = set(words)
    light_words = {"sun", "light", "bright", "star", "gold", "white", "day", "exulting", "won", "shining"}
    dark_words = {"dark", "night", "black", "shadow", "cold", "dead", "grim", "fearful", "bleeding", "fallen"}
    light_score = len(unique_words.intersection(light_words))
    dark_score = len(unique_words.intersection(dark_words))
    total_thematic_words = light_score + dark_score
    if total_thematic_words > 0:
        features['light_dark_ratio'] = (light_score - dark_score) / total_thematic_words
    else:
        features['light_dark_ratio'] = 0.0

    return features

NUM_FRAMES = 120  
OUTPUT_FOLDER = "fractal_animation" 


poem_features = analyze_poem(poem_text)
print("--- Poem Analysis Results ---")
for key, value in poem_features.items():
    print(f"  - {key:<22}: {value:.4f}")
print("-" * 35)


base_real = -0.76
base_imag = 0.12

c_center_real = base_real + (poem_features['sentiment_compound'] * 0.1)
c_center_imag = base_imag + (poem_features['lexical_density'] - 0.8) * 0.2
c_center = complex(c_center_real, c_center_imag)


path_radius = 0.05 + (poem_features['avg_word_length'] - 4.0) * 0.02


rotation_speed = 1.0 + poem_features['light_dark_ratio'] * 0.5

print(f"\n🌀 Animation Path Defined:")
print(f"  - Path Center: {c_center:.4f}")
print(f"  - Path Radius: {path_radius:.4f}")
print(f"  - Rotation Speed: {rotation_speed:.4f}x")


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


width, height = 800, 800
max_iter = 500
x_min, x_max, y_min, y_max = -2.0, 2.0, -2.0, 2.0


for frame in range(NUM_FRAMES):
    angle = (2 * np.pi * frame / NUM_FRAMES) * rotation_speed
    c = c_center + path_radius * np.exp(1j * angle)
    
    
    x, y = np.ogrid[x_min:x_max:width*1j, y_min:y_max:height*1j]
    z = x + y * 1j
    image = np.zeros(z.shape)
    
    for i in range(max_iter):
        mask = np.abs(z) < 2.0
        if not mask.any(): break
        z[mask] = z[mask]**2 + c
        image[mask] = i + 1
        
   
    plt.figure(figsize=(10, 10))
    cmap = plt.get_cmap('gnuplot2')
    cmap.set_under(color='black')
    
    plt.imshow(image, cmap=cmap, extent=[x_min, x_max, y_min, y_max], interpolation='bilinear', vmin=1)
    plt.axis('off')
    
    
    plt.title(f'c = {c.real:.4f} + {c.imag:.4f}i', color='white')
    
    filename = os.path.join(OUTPUT_FOLDER, f'frame_{frame:03d}.png')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

    print(f"Saved {filename}")

print(f"\n Animation frames saved in '{OUTPUT_FOLDER}' folder.")

