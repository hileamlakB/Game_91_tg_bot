"""
This file contains a list of urls to funny animations that
congratulate winners
"""

url_lst = [
    "https://media.tenor.com/images/021a425021d63b351b10520c8e8bcbca/tenor.gif",
    "https://media.tenor.com/images/e2553e464adf2efcdd0893d99b21828b/tenor.gif",
    "https://media.tenor.com/images/1b4bf6745f4205d84bc18a9da6de0d1e/tenor.gif",
    "https://media.tenor.com/images/0d1ebecc9e56004c6c10fe794428d0aa/tenor.gif",
    "https://media.tenor.com/images/e13381edd672b236da8f97680123b9ba/tenor.gif",
    "https://media.tenor.com/images/50f91fd08804d0d1971340bb5b62b5ad/tenor.gif",
    "https://media.tenor.com/images/785b6f101e34c86b0049406855eb9503/tenor.gif",
    "https://media.tenor.com/images/d585b0eb04cefbae15169b158eebec83/tenor.gif",
    "https://media.tenor.com/images/d7cb771627c0a545dced4e6986d157b4/tenor.gif",
    "https://media.tenor.com/images/cbc67c4c943308ae6934fc42fc3f28a5/tenor.gif",
    "https://media.tenor.com/images/bf7d804e53f9983691fe48b175d312b2/tenor.gif",
    "https://media.tenor.com/images/01a454716d9e4aa6231f742b680abe9c/tenor.gif",
    "https://media.tenor.com/images/73b82cf4018024f37f104199ceb2e096/tenor.gif",
    "https://media.tenor.com/images/a1ddf01908733fbb45d19aa6f1826f5b/tenor.gif",
    "https://media.tenor.com/images/c0d224f5fd5e80c6dbf877f26dc1a739/tenor.gif",
    "https://media.tenor.com/images/e7e5f285eb1569ef4b0f81aef9949363/tenor.gif",
    "https://media.tenor.com/images/131549f489f6a6ab74254a7688d7455a/tenor.gif",
    "https://media.tenor.com/images/2d7ca9b9065c71d3d33a6a34cf8121d4/tenor.gif",
    "https://media.tenor.com/images/4785baa312cb745989e1ba8eedc49568/tenor.gif",
    "https://media1.tenor.com/images/ac86a2659730f38b5d22a10ac63d8039/tenor.gif",
    "https://media1.tenor.com/images/c7504b9fb03c95b3b5687d744687e11c/tenor.gif",
    "https://media1.tenor.com/images/4160d3e885c0d707ad6d72217c487dc3/tenor.gif",
    "https://media1.tenor.com/images/b6d83d66859b0cf095ef81120ef98e1f/tenor.gif",
]


def get_anim_url():
    global url_lst
    import random
    return random.choice(url_lst)
