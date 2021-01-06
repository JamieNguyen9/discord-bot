import random

carl_links = [
    "https://i1.sndcdn.com/artworks-000650881924-x9k0sw-t500x500.jpg",
    "https://media1.tenor.com/images/0810e079c392ba3d483ba81f4edeef97/tenor.gif?itemid=17987376",
    "https://media.tenor.com/images/2bfbf4df86550fc5d3ed4b6e74ac7e75/tenor.gif",
    "https://66.media.tumblr.com/f5e7ff72672d00b61f6ee864a5c00c18/tumblr_ppeqbhi97d1wynsudo1_400.png",
    "https://media0.giphy.com/media/fZaAP3pmkgPio/giphy.gif"
]

def get_carl():
    index = random.randint(0, len(carl_links) - 1)
    return carl_links[index]
