EMOJI_MAP = {
    # word:emoji
    ':smile:': '😄',
    ':laugh:': '😂',
    ':grin:': '😀',
    ':joy:': '😂',
    ':wink:': '😉',
    ':cool:': '😎',
    ':love:': '😍',
    ':heart:': '❤️',
    ':fire:': '🔥',
    ':thumbsup:': '👍',
    ':thumbsdown:': '👎',
    ':clap:': '👏',
    ':pray:': '🙏',
    ':100:': '💯',
    ':star:': '⭐',
    ':check:': '✅',
    ':cross:': '❌',
    ':wave:': '👋',
    ':point_right:': '👉',
    ':point_left:': '👈',
    ':point_up:': '👆',
    ':point_down:': '👇',
    ':ok_hand:': '👌',
    ':peace:': '✌️',
    ':sad:': '😢',
    ':cry:': '😭',
    ':angry:': '😠',
    ':rage:': '😡',
    ':disappointed:': '😞',
    ':worried:': '😟',
    ':party:': '🎉',
    ':tada:': '🎊',
    ':balloon:': '🎈',
    ':gift:': '🎁',
    ':cake:': '🎂',
    ':confetti:': '🎊',

    ':rocket:': '🚀',
    ':crown:': '👑',
    ':gem:': '💎',
    ':boom:': '💥',
    ':lightning:': '⚡',
    ':shield:': '🛡️',
    ':sword:': '⚔️',
    ':sun:': '☀️',
    ':moon:': '🌙',
    ':rainbow:': '🌈',
    ':tree:': '🌳',
    ':flower:': '🌸',
    ':rose:': '🌹',
    ':thinking:': '🤔',
    ':eyes:': '👀',
    ':skull:': '💀',
    ':ghost:': '👻',
    ':alien:': '👽',
    ':robot:': '🤖',
    ':ninja:': '🥷',
    ':admin:': '👮', #for admin
    ':ban_hammer:': '🔨',
    ':warning:': '⚠️',
    ':stop:': '🛑',
    ':gamepad:': '🎮',
    ':computer:': '💻',
    ':phone:': '📱',
    ':wifi:': '📶',
    ':battery:': '🔋',
}

def convert_emojis(text):
    """Convert emoji shortcodes to actual emojis"""
    for shortcode, emoji in EMOJI_MAP.items():
        text = text.replace(shortcode, emoji)
    return text

def get_emoji_list():
    """Return a formatted list of available emojis"""
    categories = {
        'Happy': [':smile:', ':laugh:', ':grin:', ':wink:', ':cool:', ':love:'],
        'Reactions': [':heart:', ':fire:', ':thumbsup:', ':clap:', ':100:', ':star:'],
        'Gestures': [':wave:', ':point_right:', ':ok_hand:', ':peace:'],
        'Sad': [':sad:', ':cry:', ':angry:', ':disappointed:'],
        'Fun': [':party:', ':tada:', ':gift:', ':cake:'],
        'Objects': [':rocket:', ':crown:', ':diamond:', ':boom:', ':lightning:'],
        'Admin': [':admin:', ':ban_hammer:', ':warning:', ':stop:']
    }
    
    emoji_help = "📝 Available Emojis:\n"
    for category, emojis in categories.items():
        emoji_help += f"\n{category}: "
        emoji_help += " ".join([f"{code} {EMOJI_MAP[code]}" for code in emojis if code in EMOJI_MAP])
    
    emoji_help += "\n\nJust type the code in your message! Example: 'hello :wave: :smile:'"
    return emoji_help

def search_emoji(keyword):
    """Search for emojis by keyword"""
    results = []
    keyword = keyword.lower()
    
    for shortcode, emoji in EMOJI_MAP.items():
        if keyword in shortcode.lower():
            results.append(f"{shortcode} {emoji}")
    
    return results if results else ["No emojis found for that keyword 😔"]