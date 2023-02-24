from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# Getting the words from my csv file.
with open("split_messages.csv", 'r') as file:
    text = file.readlines()
    text = text[0].replace("'", "").replace('"', "").replace("[", "").replace("]", "")


# Getting the stop words.
# A) In Spanish:
spanish_word_list = ["de", "un", "en", "que", "mi", "se", "n", "ni", "lo", "se", "una", "la", "y", "el", "ve", "hoy", "su", "es", "del", "día", "por", "los", "pero", "mas", "ya", "si", "esa", "solo", "ese", "con", "hola", "para", "hizo", "hasta", "o", "horas", "ayudar", "buenas", "puede", "noche",  "digital", "fue", "ayer", "noches", "puedan", "van", "agradezco", "atención", "atencion", "tardes", "al", "muy", "mis", "phone", "esta", "está", "aún", "aun", "desde", "caso", "este", "dice", "tu", "otra", "use", "las", "q", "favor", "pronta", "cuando", "tengo", "día", "días", "ha", "mal"]
# B) In English:
english_word_list = list(STOPWORDS)

stop_words = spanish_word_list + english_word_list

# Create and generate a word cloud image:
wordcloud = WordCloud(stopwords = stop_words).generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('') # Indicate the full path on where the image file should be saved. An example for Mac users could be: /Users/my_name/Documents/zendesk/wordcloud.png
#plt.show()
