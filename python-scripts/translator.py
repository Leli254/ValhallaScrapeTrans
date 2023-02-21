from bs4 import BeautifulSoup
from googletrans import Translator

# Load the HTML file
with open('your file/path', 'r') as f:
    html = f.read()

# Parse the HTML and extract the text
soup = BeautifulSoup(html, 'html.parser')
for tag in soup.find_all():
    if tag.string:
        # Translate the text to Hindi
        translator = Translator()
        translated_text = translator.translate(tag.string, dest='hi').text

        # Replace the original text with the translated text
        tag.string.replace_with(translated_text)

# Save the modified HTML to a file
with open('your.html', 'w') as f:
    f.write(str(soup))

print("Translation complete! The translated HTML has been saved to 'your.html'")

