
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

        if self.name in RESERVED_WORDS:
            self.error(
                f"""Cannot use '{self.name}' as your component name.
                See the list of reserved Orca words: {RESERVED_WORDS}"""
            )

    def validate(self):
        return

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