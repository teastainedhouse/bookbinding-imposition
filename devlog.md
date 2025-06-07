*June 6th, 2025*
Posted to Reddit and got useful feedback! I will try to add:
- quarto, octavo, sextodecimo layouts 
  - fold lines for the above
- crop/trim marks
- keep GUI simplified
- support for EPUB files from Gutenburg.org (my own idea)


---

*Started May 28th, 2025*

Goal: open source imposition software for hobby bookbinders

Features for MVP:
- GUI
- select file (.pdf only)
  - ~select paper output size~
      - ~letter~
      - ~legal~
      - ~poster (24" x 36")~
- select signature size
    - ~only appears when "letter" or "legal" paper size is chosen~
- select output location

*Removed poster size because people who can afford a several thousand dollar large-format printer probably have 
better software than this anyway (and my dream of printing on ultra large paper and properly folding and cutting it 
to the grain was dashed when I realized that even second-hand large-format printers still go for over a thousand 
dollars, and also talasonline.com now sells letter sized paper that's short grain, so... yay, I guess.)*

*Removed paper selection size because when I was writing the feature list I didn't yet understand how the pypdf 
library draws mediaboxes. Now I realize that picking the size can just be handled directly by whatever software 
you're using to view and print the PDF. Neat.*
