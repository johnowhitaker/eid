Pachydentify

Pachydentify is released under the GPL, the full text of this licence is at .....

Classes in the code

Elephant:

Herd:
- this is simply a collection of elephants. Can load data from a spreadsheet,
  filter elephants...
- herd.filter({'feature 1': [values], 'feature 2':[...], ...})

EID_FORM:
- The main window, which loads the data...

E_INFO_DIALOG:
- When a picture of an elephant is clicked, a new window opens. Here, the user can
  zoom in on high res versions of the pictures associated with that elephant, and
  see extra notes about the elephant.

PhotoViewer:
- This is a separate class, making some features of QGraphicsView easier to use.
  Found on StackOverflow, by user ekhumoro, public domain?
