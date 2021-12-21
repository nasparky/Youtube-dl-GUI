# Additional functions used for the program
import os
import string

filePath = os.path.join(os.getcwd(), "Exports")

# Return a valid filename according to the OS
def changeName(filename):
  newFileName = ""
  schars = string.punctuation
  for ch in filename:
    if ch in schars:
      ch = "_"
    newFileName += ch
  return newFileName

# Create a new directory for all exports
def createDir():
  try:
    if not os.path.isdir(filePath):
      os.mkdir(filePath)
      return "Successfully created new directory."
    return "Directory already created, continuing..."
  except OSError as e:
    return e

# Calculate a missing proportion
def calcMissingProp(a1, a2, b1):
  return int((b1 * a2) / a1)

def getHTMLLink(screen, link):
  return f'''
    <!DOCTYPE html>
    <html>
      <body style="background-color: #000000">
        <iframe width={screen[0]} height={screen[1]} src={link} title="YouTube video player" frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen>
        </iframe>
      </body>
    </html>
  '''

def getEmbededLink(link):
  linkAddressAcceptance = ["https://youtu.be/", "https://www.youtube.com/watch?v="]
  for i in range(len(linkAddressAcceptance)):
    if linkAddressAcceptance[i] in link:
      uniqueStr = link.replace(linkAddressAcceptance[i], "")
      newLink = "https://www.youtube.com/embed/" + uniqueStr
      return newLink