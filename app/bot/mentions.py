"""Utils to work with mentions."""

from typing import List, Union

from pybotx import IncomingMessage
from pybotx.models.message.mentions import MentionContact, MentionUser


def user_mentions_without_bot(
    message: IncomingMessage,
) -> List[Union[MentionUser, MentionContact]]:
    return [
        mention
        for mention in message.mentions
        if (
            isinstance(mention, (MentionUser, MentionContact))
            and mention.entity_id != message.bot.id
        )
    ]
