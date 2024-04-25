from ..common import RESERVED_WORDS


class Node:
    def __init__(
        self,
        name,
        description="",
        tags=[],
        visibility="**/*",
    ):
        # Gives this component
        self.name = name
        # lets us describe, in human terms, what this does
        self.description = description
        # allows to append whatever sorts of tags we want to this component
        self.tags = tags
        # allows us to limit those that can see this part of the network.
        self.visibility = visibility

        self._resolved = True

        # Lets validate here. This will only do the validation for this
        # class level. TODO: double check this.
        Node.validate(self)

    def get_resolved(self):
        return self._resolved

    def validate(self):
        if self.name in RESERVED_WORDS:
            self.error(
                f"""Cannot use '{self.name}' as your component name.
                See the list of reserved Orca words: {RESERVED_WORDS}"""
            )

    def overview(self):
        return f"""
        name: {self.name}
        description: {self.description}
        tags: {self.tags}
        """

    def error(self, message):
        raise BaseException(
            f"""
        Bad {self.__class__.__name__}: {message}.
        {self.overview()}
        """
        )
