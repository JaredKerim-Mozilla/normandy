import random
import string

from normandy.base.color import Color


class Genome(random.Random):
    """A seedable source that provides arbitrarily sized chunks of randomness."""
    def __init__(self, seed=None):
        super().__init__(seed)

        # Colors taken from the Solarized color scheme (http://ethanschoonover.com/solarized)
        self.colors = [
            Color((0x00, 0x2b, 0x36)),
            Color((0x07, 0x36, 0x42)),
            Color((0x58, 0x6e, 0x75)),
            Color((0x65, 0x7b, 0x83)),
            Color((0x83, 0x94, 0x96)),
            Color((0x93, 0xa1, 0xa1)),
            Color((0xee, 0xe8, 0xd5)),
            Color((0xfd, 0xf6, 0xe3)),
            Color((0xff, 0xcf, 0x00)),  # alternate yellow color
            Color((0xcb, 0x4b, 0x16)),
            Color((0xdc, 0x32, 0x2f)),
            Color((0xd3, 0x36, 0x82)),
            Color((0x6c, 0x71, 0xc4)),
            Color((0x26, 0x8b, 0xd2)),
            Color((0x2a, 0xa1, 0x98)),
            Color((0x85, 0x99, 0x00)),
        ]

    def weighted_choice(self, options):
        """
        Choose a random object from an array by weight.
        `options` should be objects with at least a `weight` key.
        """
        sum_weights = sum(o['weight'] for o in options)

        choice = self.randrange(sum_weights)
        for option in options:
            choice -= option['weight']
            if choice <= 0:
                return option
        raise Exception('No choices chosen.')

    def letter(self):
        """Generates a random capital letter."""
        return string.ascii_letters[self.randint(26, 52)]

    def emoji(self):
        """Generates a random emoji."""
        emojis = ["😄", "😃", "😀", "😊", "😉", "😍", "😘", "😚", "😗", "😙", "😜", "😝", "😛",
                  "😳", "😁", "😔", "😌", "😒", "😞", "😣", "😢", "😂", "😭", "😪", "😥", "😰",
                  "😅", "😓", "😨", "😱", "😠", "😡", "😤", "😖", "😆", "😋", "😷", "😎", "😴",
                  "😵", "😲", "😟", "😦", "😧", "😈", "👿", "😮", "😬", "😐", "😯", "😶", "😇",
                  "😏", "😑", "👼", "😺", "😻", "😽", "😼", "🙀", "😿", "😹", "😾", "👹", "👺",
                  "🙈", "🙉", "🙊", "💀", "👽", "💩", "🔥", "✨", "🌟", "💫", "💥", "💦", "💧",
                  "💤", "👂", "👀", "👃", "👅", "👄", "👍", "👎", "👌", "👊", "✊", "👋", "✋",
                  "👐", "👆", "🙌", "🙏", "👏", "💪", "💃", "🎩", "👑", "👒", "👟", "👞", "👡",
                  "👠", "👢", "💼", "👜", "👝", "👛", "👓", "🎀", "🌂", "💄", "💛", "💙", "💜",
                  "💚", "💔", "💗", "💓", "💕", "💖", "💞", "💘", "💌", "💋", "💍", "💎", "👣",
                  "🐶", "🐺", "🐱", "🐭", "🐹", "🐰", "🐸", "🐯", "🐨", "🐻", "🐷", "🐽", "🐮",
                  "🐗", "🐵", "🐒", "🐴", "🐑", "🐘", "🐼", "🐧", "🐦", "🐤", "🐥", "🐣", "🐔",
                  "🐍", "🐢", "🐛", "🐝", "🐜", "🐞", "🐌", "🐙", "🐚", "🐠", "🐟", "🐬", "🐳",
                  "🐋", "🐄", "🐏", "🐀", "🐃", "🐅", "🐇", "🐉", "🐎", "🐐", "🐓", "🐕", "🐖",
                  "🐁", "🐂", "🐲", "🐡", "🐊", "🐫", "🐪", "🐆", "🐈", "🐩", "🐾", "💐", "🌸",
                  "🌷", "🍀", "🌹", "🌻", "🌺", "🍁", "🍃", "🍂", "🌿", "🌾", "🍄", "🌵", "🌴",
                  "🌲", "🌳", "🌰", "🌱", "🌼", "🌐", "🌞", "🌝", "🌚", "🌜", "🌛", "🌙", "🌍",
                  "🌎", "🌏", "⭐", "⛅", "⛄", "🌀", "💝", "🎒", "🎓", "🎏", "🎃", "👻", "🎄",
                  "🎁", "🎋", "🎉", "🎈", "🔮", "🎥", "📷", "📹", "📼", "💿", "📀", "💽", "💾",
                  "💻", "📱", "📞", "📟", "📠", "📡", "📺", "📻", "🔊", "🔔", "📢", "⏳", "⏰",
                  "🔓", "🔒", "🔏", "🔐", "🔑", "🔎", "💡", "🔦", "🔆", "🔅", "🔌", "🔋", "🔍",
                  "🛁", "🚿", "🚽", "🔧", "🔨", "🚪", "💣", "🔫", "🔪", "💊", "💉", "💰", "💸",
                  "📨", "📬", "📌", "📎", "📕", "📓", "📚", "📖", "🔬", "🔭", "🎨", "🎬", "🎤",
                  "🎵", "🎹", "🎻", "🎺", "🎷", "🎸", "👾", "🎮", "🃏", "🎲", "🎯", "🏈", "🏀",
                  "⚽", "🎾", "🎱", "🏉", "🎳", "⛳", "🚴", "🏁", "🏇", "🏆", "🎿", "🏂", "🏄",
                  "🎣", "🍵", "🍶", "🍼", "🍺", "🍻", "🍸", "🍹", "🍷", "🍴", "🍕", "🍔", "🍟",
                  "🍗", "🍤", "🍞", "🍩", "🍮", "🍦", "🍨", "🍧", "🎂", "🍰", "🍪", "🍫", "🍬",
                  "🍭", "🍯", "🍎", "🍏", "🍊", "🍋", "🍒", "🍇", "🍉", "🍓", "🍑", "🍌", "🍐",
                  "🍍", "🍆", "🍅", "🌽", "🏠", "🏡", "⛵", "🚤", "🚣", "🚀", "🚁", "🚂", "🚎",
                  "🚌", "🚍", "🚙", "🚘", "🚗", "🚕", "🚖", "🚛", "🚚", "🚨", "🚓", "🚔", "🚒",
                  "🚑", "🚐", "🚲", "🚜", "💈", "🚦", "🚧", "🏮", "🎰", "🗿", "🎪", "🎭", "📍",
                  "🚩", "💯"]
        return self.choice(emojis)

    def color(self):
        """Generates a random color."""
        return self.choice(self.colors)
