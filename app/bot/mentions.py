"""Utils to work with mentions."""

from typing import List

from pybotx import IncomingMessage, Mention, MentionTypes


def user_mentions_without_bot(message: IncomingMessage) -> List[Mention]:
    return [
        mention
        for mention in message.mentions
        if (
            mention.type in {MentionTypes.CONTACT, MentionTypes.USER}
            and mention.entity_id != message.bot.id
        )
    ]
