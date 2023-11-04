from random import choice
import string


class ToonString(str):

    class ToonCharMap():
        ascii_chars: dict[str, list[str]]
        special_chars = {
                'i': '1', 'e': '3', 'o': '0', 'u': 'v'
        }
        def __init__(self) -> None:
            self.ascii_chars = {
                ascii: [ascii.lower(), ascii.upper()]
                for ascii in string.ascii_letters
            }
            for k, v in self.special_chars.items():
                 self.ascii_chars[k] += v

    char_map = ToonCharMap()

    def toonify(self, c: str):
        """ Every character will be randomized from a mapping
        """
        if self.char_map.ascii_chars.get(c):
            return choice(self.char_map.ascii_chars.get(c))
        return c

    def __str__(self):
        return "".join([self.toonify(c) for c in self])
    

if __name__ == "__main__":
    toon_str = ToonString("This is in toon characterz!")
    print(toon_str)