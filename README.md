*Started May 28th, 2025*

Goal: open source imposition software for hobby bookbinders

Features for MVP:
- GUI
- select file (.pdf only)
~~- select paper output size
  - letter
  - legal
  - poster (24" x 36")~~
- select signature size
~~  - only appears when "letter" or "legal" paper size is chosen~~
- select output location

*Removed poster size because people who can afford a several thousand dollar large-format printer probably have 
better software than this anyway (and my dream of printing on ultra large paper and properly folding and cutting it 
to the grain was dashed when I realized that even second-hand large-format printers still go for over a thousand 
dollars, and also talasonline.com now sells letter sized paper that's short grain, so... yay, I guess.)*
*Removed paper selection size because when I was writing the feature list I didn't yet understand how the pypdf 
library draws mediaboxes. Now I realize that picking the size can just be handled directly by whatever software 
you're using to view and print the PDF. Neat.*

## Credits
GIF by <a href="https://pixabay.com/users/ekkant-33254754/?utm_source=link-attribution&utm_medium=referral&utm_campaign=animation&utm_content=8826">Ekaterine Kantaria</a> from 
<a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=animation&utm_content=8826">Pixabay</a>